#!/usr/bin/env python3
"""Exporta e importa las texturas (.srd + .srdv) de los .SPC de Danganronpa V3 (interfaz en flash/).

Formato SRD portado de V3Lib (https://github.com/redssu/Harmony-Tools, dependencies/V3Lib/Srd).

Al importar, la textura se guarda como ARGB8888 sin comprimir (formato 0x01), que el juego acepta
para cualquier textura: solo cambia el formato en el bloque $TXR, se reescribe texture.srdv con
los pixeles nuevos (alineado a 128 bytes, como el original) y se actualizan offset y tamano en el
bloque $RSI de cada textura. Ancho, alto y diseno (.sfl) no cambian, asi que el PNG editado debe
tener las mismas dimensiones que el original.

Uso:
    drv3srd.py info <archivo.spc>...
        Lista las texturas de cada SPC (nombre, tamano, formato).
    drv3srd.py exportar <archivo.spc> <carpeta>
        Exporta todas las texturas del SPC como PNG.
    drv3srd.py importar <archivo.spc> <carpeta_png> <salida.spc>
        Reemplaza las texturas que tengan un PNG con el mismo nombre en la carpeta.
"""
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bc7  # noqa: E402
import drv3text  # noqa: E402

FORMATOS = {0x01: "ARGB8888", 0x02: "BGR565", 0x05: "BGRA4444", 0x0F: "DXT1", 0x11: "DXT5",
            0x14: "BC5", 0x16: "BC4", 0x1A: "Indexed8", 0x1C: "BC7"}
ARGB8888 = 0x01
EN_SRDV = 0x40000000
ALINEACION = 128


# ---------------------------------------------------------------------------
# SRD
# ---------------------------------------------------------------------------
def _pad(n, a=16):
    return (a - n % a) % a


def leer_bloques(buf, pos=0, fin=None):
    """[(tipo, datos, hijos, posicion_de_datos)]"""
    fin = len(buf) if fin is None else fin
    bloques = []
    while pos + 16 <= fin:
        tipo = buf[pos:pos + 4].decode("ascii", "replace")
        largo, sublargo, _ = struct.unpack_from(">iii", buf, pos + 4)
        pos += 16
        pos_datos = pos
        datos = buf[pos:pos + largo]
        pos += largo + _pad(largo)
        hijos = leer_bloques(buf, pos, pos + sublargo)
        pos += sublargo + _pad(sublargo)
        bloques.append((tipo, datos, hijos, pos_datos))
    return bloques


def _todos(bloques):
    for b in bloques:
        yield b
        yield from _todos(b[2])


def leer_rsi(datos):
    _, _, _, fallback_count, count, fallback_size, size, _, str_off = struct.unpack_from("<BBBBhhhhi", datos, 0)
    n = count or fallback_count
    tam = (size or fallback_size or 16) // 4
    recursos = [struct.unpack_from(f"<{tam}i", datos, 0x10 + i * tam * 4) for i in range(n)]
    nombres = [s.decode("shift-jis", "replace") for s in datos[str_off:].split(b"\0") if s]
    return recursos, nombres


class Textura:
    def __init__(self, nombre, ancho, alto, fmt, swizzle, datos, offset, pos_txr, pos_rsi):
        self.nombre, self.ancho, self.alto, self.fmt, self.swizzle = nombre, ancho, alto, fmt, swizzle
        self.datos, self.offset, self.pos_txr, self.pos_rsi = datos, offset, pos_txr, pos_rsi

    def rgba(self):
        return decodificar(self.ancho, self.alto, self.fmt, self.datos)


def texturas(srd, srdv):
    salida = []
    for tipo, datos, hijos, pos in leer_bloques(srd):
        if tipo != "$TXR" or not hijos or hijos[0][0] != "$RSI":
            continue
        _, swizzle, ancho, alto, _, fmt = struct.unpack_from("<iHHHHB", datos, 0)
        recursos, nombres = leer_rsi(hijos[0][1])
        if (recursos[0][0] & ~0x1FFFFFFF) != EN_SRDV or srdv is None:
            continue
        offset, tam = recursos[0][0] & 0x1FFFFFFF, recursos[0][1]
        salida.append(Textura(nombres[0] if nombres else "?", ancho, alto, fmt, swizzle,
                              srdv[offset:offset + tam], offset, pos, hijos[0][3]))
    return salida


def texturas_de_spc(ruta):
    """{nombre_srd: [Textura]} para cada par .srd/.srdv del SPC."""
    archivos = {s.name: s.decompressed() for s in drv3text.SpcFile(ruta).subfiles}
    return {n: texturas(d, archivos.get(n + "v")) for n, d in archivos.items() if n.lower().endswith(".srd")}


def reemplazar(srd, srdv, nuevas):
    """Devuelve (srd, srdv) con las texturas de `nuevas` ({nombre: rgba}) en ARGB8888."""
    lista = texturas(srd, srdv)
    # Solo se reconstruye el srdv si todo lo que referencia son texturas simples (como en flash/)
    referencias = sum(1 for tipo, datos, _, _ in _todos(leer_bloques(srd)) if tipo == "$RSI"
                      for r in leer_rsi(datos)[0] if (r[0] & ~0x1FFFFFFF) == EN_SRDV)
    if referencias != len(lista):
        raise ValueError("el .srdv contiene datos que no son texturas simples; no se puede reconstruir")

    srd = bytearray(srd)
    nuevo_srdv = bytearray()
    for t in sorted(lista, key=lambda t: t.offset):
        if t.nombre in nuevas:
            datos = codificar_argb8888(nuevas[t.nombre])
            struct.pack_into("<B", srd, t.pos_txr + 12, ARGB8888)
        else:
            datos = t.datos
        nuevo_srdv += bytes(_pad(len(nuevo_srdv), ALINEACION))
        struct.pack_into("<ii", srd, t.pos_rsi + 0x10, EN_SRDV | len(nuevo_srdv), len(datos))
        nuevo_srdv += datos
    return bytes(srd), bytes(nuevo_srdv)


# ---------------------------------------------------------------------------
# Decodificadores (devuelven RGBA de ancho x alto)
# ---------------------------------------------------------------------------
def _565(c):
    r, g, b = (c >> 11) & 31, (c >> 5) & 63, c & 31
    return (r << 3 | r >> 2, g << 2 | g >> 4, b << 3 | b >> 2)


def _bloque_color(d, o, dxt1):
    c0, c1, bits = struct.unpack_from("<HHI", d, o)
    a, b = _565(c0), _565(c1)
    if c0 > c1 or not dxt1:
        p = [a + (255,), b + (255,),
             tuple((2 * x + y) // 3 for x, y in zip(a, b)) + (255,),
             tuple((x + 2 * y) // 3 for x, y in zip(a, b)) + (255,)]
    else:
        p = [a + (255,), b + (255,), tuple((x + y) // 2 for x, y in zip(a, b)) + (255,), (0, 0, 0, 0)]
    return [p[(bits >> (2 * i)) & 3] for i in range(16)]


def _bloque_alfa(d, o):
    a0, a1 = d[o], d[o + 1]
    bits = int.from_bytes(d[o + 2:o + 8], "little")
    if a0 > a1:
        tabla = [a0, a1] + [((7 - i) * a0 + i * a1) // 7 for i in range(1, 7)]
    else:
        tabla = [a0, a1] + [((5 - i) * a0 + i * a1) // 5 for i in range(1, 5)] + [0, 255]
    return [tabla[(bits >> (3 * i)) & 7] for i in range(16)]


def _bloques(ancho, alto, d, tam_bloque, decodificar_bloque):
    out = bytearray(ancho * alto * 4)
    bw = (ancho + 3) // 4
    for by in range((alto + 3) // 4):
        for bx in range(bw):
            o = (by * bw + bx) * tam_bloque
            if o + tam_bloque > len(d):
                continue
            px = decodificar_bloque(d, o)
            for i in range(16):
                x, y = bx * 4 + i % 4, by * 4 + i // 4
                if x < ancho and y < alto:
                    out[(y * ancho + x) * 4:(y * ancho + x) * 4 + 4] = bytes(px[i])
    return out


def decodificar(ancho, alto, fmt, d):
    if fmt == 0x0F:
        return _bloques(ancho, alto, d, 8, lambda d, o: _bloque_color(d, o, True))
    if fmt == 0x11:
        def dxt5(d, o):
            alfa = _bloque_alfa(d, o)
            return [c[:3] + (alfa[i],) for i, c in enumerate(_bloque_color(d, o + 8, False))]
        return _bloques(ancho, alto, d, 16, dxt5)
    if fmt == 0x1C:
        return _bloques(ancho, alto, d, 16, lambda d, o: bc7.bloque(d[o:o + 16]))
    if fmt == ARGB8888:
        out = bytearray(ancho * alto * 4)
        out[0::4], out[1::4], out[2::4], out[3::4] = d[2::4][:ancho * alto], d[1::4][:ancho * alto], \
            d[0::4][:ancho * alto], d[3::4][:ancho * alto]
        return out
    raise NotImplementedError(FORMATOS.get(fmt, hex(fmt)))


def codificar_argb8888(rgba):
    """RGBA -> bytes en el orden que usa el juego para ARGB8888 (B, G, R, A)."""
    out = bytearray(len(rgba))
    out[0::4], out[1::4], out[2::4], out[3::4] = rgba[2::4], rgba[1::4], rgba[0::4], rgba[3::4]
    return bytes(out)


# ---------------------------------------------------------------------------
# PNG
# ---------------------------------------------------------------------------
def _chunk(tipo, datos):
    return struct.pack(">I", len(datos)) + tipo + datos + struct.pack(">I", zlib.crc32(tipo + datos))


def guardar_png(ruta, ancho, alto, rgba):
    filas = b"".join(b"\0" + bytes(rgba[y * ancho * 4:(y + 1) * ancho * 4]) for y in range(alto))
    with open(ruta, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", struct.pack(">IIBBBBB", ancho, alto, 8, 6, 0, 0, 0))
                + _chunk(b"IDAT", zlib.compress(filas, 6)) + _chunk(b"IEND", b""))


def leer_png(ruta):
    """Lee un PNG de 8 bits (escala de grises, RGB, RGBA o con paleta) y devuelve (ancho, alto, rgba)."""
    with open(ruta, "rb") as f:
        buf = f.read()
    if buf[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{ruta}: no es un PNG")
    pos, idat, paleta, trns = 8, bytearray(), None, None
    while pos < len(buf):
        largo = struct.unpack_from(">I", buf, pos)[0]
        tipo, datos = buf[pos + 4:pos + 8], buf[pos + 8:pos + 8 + largo]
        pos += 12 + largo
        if tipo == b"IHDR":
            ancho, alto, prof, color, _, _, entrelazado = struct.unpack(">IIBBBBB", datos)
        elif tipo == b"PLTE":
            paleta = datos
        elif tipo == b"tRNS":
            trns = datos
        elif tipo == b"IDAT":
            idat += datos
    if prof != 8 or entrelazado:
        raise ValueError(f"{ruta}: solo se admiten PNG de 8 bits por canal sin entrelazar")
    canales = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[color]
    crudo = zlib.decompress(bytes(idat))
    bpp, fila = canales, ancho * canales
    out = bytearray(alto * fila)
    anterior = bytearray(fila)
    p = 0
    for y in range(alto):
        filtro, linea = crudo[p], bytearray(crudo[p + 1:p + 1 + fila])
        p += 1 + fila
        for i in range(fila):
            a = linea[i - bpp] if i >= bpp else 0
            b = anterior[i]
            c = anterior[i - bpp] if i >= bpp else 0
            if filtro == 1:
                linea[i] = (linea[i] + a) & 255
            elif filtro == 2:
                linea[i] = (linea[i] + b) & 255
            elif filtro == 3:
                linea[i] = (linea[i] + (a + b) // 2) & 255
            elif filtro == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                linea[i] = (linea[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        out[y * fila:(y + 1) * fila] = linea
        anterior = linea
    rgba = bytearray(ancho * alto * 4)
    for i in range(ancho * alto):
        if color == 6:
            rgba[i * 4:i * 4 + 4] = out[i * 4:i * 4 + 4]
        elif color == 2:
            rgba[i * 4:i * 4 + 4] = out[i * 3:i * 3 + 3] + b"\xff"
        elif color == 0:
            rgba[i * 4:i * 4 + 4] = bytes((out[i],) * 3 + (255,))
        elif color == 4:
            rgba[i * 4:i * 4 + 4] = bytes((out[i * 2],) * 3 + (out[i * 2 + 1],))
        else:
            k = out[i]
            alfa = trns[k] if trns is not None and k < len(trns) else 255
            rgba[i * 4:i * 4 + 4] = paleta[k * 3:k * 3 + 3] + bytes((alfa,))
    return ancho, alto, bytes(rgba)


# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------
def exportar(ruta_spc, carpeta):
    os.makedirs(carpeta, exist_ok=True)
    grupos = texturas_de_spc(ruta_spc)
    for srd, lista in grupos.items():
        destino = carpeta if len(grupos) == 1 else os.path.join(carpeta, os.path.splitext(srd)[0])
        os.makedirs(destino, exist_ok=True)
        for t in lista:
            try:
                rgba = t.rgba()
            except NotImplementedError as e:
                print(f"[omitida] {t.nombre}: formato {e}")
                continue
            ruta = os.path.join(destino, os.path.splitext(t.nombre)[0] + ".png")
            guardar_png(ruta, t.ancho, t.alto, rgba)
            print(ruta)


def importar(ruta_spc, carpeta, salida):
    spc = drv3text.SpcFile(ruta_spc)
    archivos = {s.name: s for s in spc.subfiles}
    usados = set()
    for nombre_srd in [n for n in archivos if n.lower().endswith(".srd")]:
        srd = archivos[nombre_srd].decompressed()
        srdv_sub = archivos.get(nombre_srd + "v")
        if srdv_sub is None:
            continue
        lista = texturas(srd, srdv_sub.decompressed())
        nuevas = {}
        for base in (carpeta, os.path.join(carpeta, os.path.splitext(nombre_srd)[0])):
            for t in lista:
                png = os.path.join(base, os.path.splitext(t.nombre)[0] + ".png")
                if t.nombre in nuevas or not os.path.isfile(png):
                    continue
                ancho, alto, rgba = leer_png(png)
                if (ancho, alto) != (t.ancho, t.alto):
                    raise ValueError(f"{png}: mide {ancho}x{alto}, pero la textura original mide {t.ancho}x{t.alto}")
                nuevas[t.nombre] = rgba
                usados.add(os.path.abspath(png))
        if not nuevas:
            continue
        nuevo_srd, nuevo_srdv = reemplazar(srd, srdv_sub.decompressed(), nuevas)
        for sub, datos in ((archivos[nombre_srd], nuevo_srd), (srdv_sub, nuevo_srdv)):
            sub.data = drv3text.compress_rapido(datos)
            sub.compression, sub.original_size = 2, len(datos)
            if sub.decompressed() != datos:
                raise RuntimeError(f"la recompresion de {sub.name} no coincide")
        for n in sorted(nuevas):
            print(f"  -> {n}")
    sin_usar = [os.path.join(r, f) for r, _, fs in os.walk(carpeta) for f in fs
                if f.lower().endswith(".png") and os.path.abspath(os.path.join(r, f)) not in usados]
    for png in sin_usar:
        print(f"[!] {png} no corresponde a ninguna textura del SPC")
    if not usados:
        print("No se reemplazo ninguna textura.")
        return 1
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    with open(salida, "wb") as f:
        f.write(spc.to_bytes())
    print(f"Guardado: {salida} ({len(usados)} texturas)")
    return 0


def main(argv):
    if len(argv) >= 3 and argv[1] == "info":
        for ruta in argv[2:]:
            for srd, lista in texturas_de_spc(ruta).items():
                for t in lista:
                    print(f"{os.path.basename(ruta)}\t{srd}\t{t.nombre}\t{t.ancho}x{t.alto}\t"
                          f"{FORMATOS.get(t.fmt, hex(t.fmt))}\tswizzle={t.swizzle}\t{len(t.datos)}")
        return 0
    if len(argv) == 4 and argv[1] in ("exportar", "png"):
        exportar(argv[2], argv[3])
        return 0
    if len(argv) == 5 and argv[1] == "importar":
        return importar(argv[2], argv[3], argv[4])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
