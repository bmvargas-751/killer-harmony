#!/usr/bin/env python3
"""Rehace rotulos de interfaz (texturas con texto) en espanol usando tipografias libres.

A diferencia de rotulos.py (que recorta las letras del propio juego), aqui el texto se dibuja con
una fuente parecida a la original y se imita el rotulo: se mide la caja del texto original, su color
y si tiene brillo, y el texto nuevo se coloca en la misma caja con el mismo aspecto. Sirve para los
estilos de los que el juego no trae todas las letras (titulos de capitulo, inicio de fases, cut-ins...).

Necesita Pillow (pip install pillow). Las fuentes se descargan la primera vez a tools/rotulos/fuentes/
(lista en tools/rotulos/fuentes.json; todas con licencia libre OFL o Apache).

Receta (JSON en tools/rotulos/):
    {
      "descripcion": "...",
      "spc": "flash/event/chapter_1_US.spc",          # relativo a data/win
      "estilo": {...},                                # opciones comunes (ver OPCIONES)
      "textos": {
        "<textura sin .png>": "TEXTO",                # o bien {"texto": "TEXTO", <opciones>}
        ...
      }
    }
Varias recetas pueden compartir estilos con "estilos": {"nombre": {...}} y "usar": "nombre".

Uso:
    rotulos_fuente.py <receta.json>... --juego <data/win del juego> --salida <carpeta> [--png <previas>]
Ejemplo:
    rotulos_fuente.py tools/rotulos/capitulos/*.json --juego ".../data/win" --salida latest/win --png /tmp/previas
"""
import json
import math
import os
import sys
import tempfile
import urllib.request

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drv3srd  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA_FUENTES = os.path.join(AQUI, "rotulos", "fuentes")

OPCIONES = {
    "fuente": None,          # nombre en fuentes.json
    "peso": None,            # eje wght para fuentes variables
    "espaciado": 0.1,        # espacio extra entre letras, en fraccion del tamano de letra
    "condensar": 1.0,        # escala horizontal de las letras (<1 = mas angostas)
    "interlineado": 1.15,    # distancia entre lineas, en fraccion de la altura de linea
    "alinear": "centro",     # centro | izquierda | derecha
    "vertical": False,       # letras apiladas de arriba a abajo
    "rotar": 0,              # grados (sentido antihorario)
    "color": None,           # [r, g, b]; por defecto, el color del trazo original
    "color_inicial": None,   # [r, g, b] para la primera letra
    "alto": None,            # alto del texto en px (por defecto, el del texto original)
    "escala_alto": 1.0,      # multiplica el alto medido
    "ancho_max": None,       # px; por defecto, el ancho del texto original
    "escala_ancho": 1.1,     # cuanto puede exceder el ancho del original
    "caja": None,            # [x0, y0, x1, y1] para forzar la caja del texto
    "brillo": "auto",        # false | radio en px | "auto" (si el original tiene halo)
    "fuerza_brillo": 1.0,
    "color_brillo": "auto",  # [r, g, b] | "auto" (color del halo del original) | None (color del texto)
    "borde": 0,              # borde fino de otro color alrededor del texto, en px
    "color_borde": "auto",   # [r, g, b] | "auto" (color del halo del original)
    "contorno": 0,           # grosor de contorno en px
    "color_contorno": None,  # por defecto, el color del texto (sirve para engrosar el trazo)
    "fondo": "auto",         # "negro" | "transparente" | "auto" (como el original)
    "desenfoque": 0,         # px: para las copias borrosas que usan las animaciones
    "recorte_original": False,  # deja ver el texto solo donde el original tenia tinta (piezas cortadas)
    "umbral": 150,           # luminancia que cuenta como trazo al medir el original
}


# ---------------------------------------------------------------------------
# Fuentes
# ---------------------------------------------------------------------------
def ruta_fuente(nombre):
    with open(os.path.join(AQUI, "rotulos", "fuentes.json"), encoding="utf-8") as f:
        lista = json.load(f)
    archivo = lista[nombre]["archivo"]
    ruta = os.path.join(CARPETA_FUENTES, archivo)
    if not os.path.exists(ruta):
        os.makedirs(CARPETA_FUENTES, exist_ok=True)
        print(f"Descargando fuente {nombre}...")
        urllib.request.urlretrieve(lista[nombre]["url"], ruta)
    return ruta


def cargar_fuente(nombre, tam, peso=None):
    f = ImageFont.truetype(ruta_fuente(nombre), tam)
    if peso is not None:
        try:
            f.set_variation_by_axes([peso])
        except (OSError, ValueError):
            pass
    return f


# ---------------------------------------------------------------------------
# Medir el original
# ---------------------------------------------------------------------------
def es_transparente(img):
    h = img.getchannel("A").histogram()
    return h[255] < img.width * img.height * 0.5


def luminancia(img):
    """Lo que cuenta como tinta: el alfa si la textura es transparente; si no, la luminancia."""
    if es_transparente(img):
        return img.getchannel("A")
    return img.convert("L")


def medir(img, umbral):
    lum = luminancia(img)
    umbral = min(umbral, int(lum.getextrema()[1] * 0.6))
    todo = lum.point(lambda v: 255 if v > 24 else 0).getbbox()
    nucleo = lum.point(lambda v: 255 if v > umbral else 0).getbbox() or todo
    return nucleo, todo


def color_halo(img, nucleo, todo):
    """Color del brillo: los pixeles mas saturados de luminancia media alrededor del trazo."""
    datos = [p for p in img.convert("RGBA").crop(todo).getdata() if p[3] > 60 and 40 < max(p[:3]) < 250]
    if not datos:
        return None
    datos.sort(key=lambda p: (max(p[:3]) - min(p[:3])) * p[3], reverse=True)
    top = datos[:max(1, len(datos) // 20)]
    c = tuple(sum(p[i] for p in top) // len(top) for i in range(3))
    return c if max(c) - min(c) > 40 else None


def color_trazo(img, caja):
    datos = [p for p in img.convert("RGBA").crop(caja).getdata() if p[3] > 128]
    if not datos:
        return (255, 255, 255)
    if es_transparente(img):  # transparente: el color de relleno es el mas frecuente
        cubos = {}
        for p in datos:
            if p[3] > 230:
                k = (p[0] >> 5, p[1] >> 5, p[2] >> 5)
                cubos.setdefault(k, []).append(p)
        if cubos:
            grupo = max(cubos.values(), key=len)
            return tuple(sum(p[i] for p in grupo) // len(grupo) for i in range(3))
    datos.sort(key=lambda p: max(p[:3]) * p[3], reverse=True)
    top = datos[:max(1, len(datos) // 40)]
    return tuple(sum(p[i] for p in top) // len(top) for i in range(3))


# ---------------------------------------------------------------------------
# Dibujar
# ---------------------------------------------------------------------------
def dibujar_texto(texto, op, color, tam=160):
    """Texto en blanco/color sobre transparente, recortado a su caja."""
    f = cargar_fuente(op["fuente"], tam, op["peso"])
    asc, desc = f.getmetrics()
    lineas = texto.split("|")
    imgs = []
    for linea in lineas:
        if op["vertical"]:
            alto_letra = int((asc + desc) * 0.82)
            lienzo = Image.new("RGBA", (tam * 3, alto_letra * (len(linea) + 1)), tuple(color) + (0,))
            d = ImageDraw.Draw(lienzo)
            for i, c in enumerate(linea):
                col = op["color_inicial"] if (i == 0 and op["color_inicial"]) else color
                d.text((tam * 1.5, alto_letra * i + asc), c, font=f, fill=tuple(col) + (255,), anchor="ms")
        else:
            ancho = int(sum(f.getlength(c) for c in linea) + op["espaciado"] * tam * len(linea)) + tam
            lienzo = Image.new("RGBA", (ancho, (asc + desc) * 2), tuple(color) + (0,))
            d = ImageDraw.Draw(lienzo)
            x = tam // 2
            for i, c in enumerate(linea):
                col = op["color_inicial"] if (i == 0 and op["color_inicial"] and linea is lineas[0]) else color
                d.text((x, asc + desc // 2), c, font=f, fill=tuple(col) + (255,), anchor="ls")
                x += f.getlength(c) + op["espaciado"] * tam
        caja = lienzo.getbbox()
        if caja is None:
            continue
        # Conservar la linea base comun: recortar en vertical por las metricas, no por la tinta
        if op["vertical"]:
            lienzo = lienzo.crop((caja[0], caja[1], caja[2], caja[3]))
        else:
            lienzo = lienzo.crop((caja[0], 0, caja[2], lienzo.height))
        if op["condensar"] != 1.0:
            lienzo = lienzo.resize((max(1, int(lienzo.width * op["condensar"])), lienzo.height), Image.LANCZOS)
        imgs.append(lienzo)
    if op["vertical"]:
        sep = int(tam * op["interlineado"] * 0.5)
        total = sum(i.width for i in imgs) + sep * (len(imgs) - 1)
        out = Image.new("RGBA", (total, max(i.height for i in imgs)), tuple(color) + (0,))
        x = 0
        for i in imgs:
            out.alpha_composite(i, (x, 0))
            x += i.width + sep
    else:
        paso = int((asc + desc) * op["interlineado"])
        out = Image.new("RGBA", (max(i.width for i in imgs), paso * (len(imgs) - 1) + imgs[-1].height), tuple(color) + (0,))
        for n, i in enumerate(imgs):
            x = {"centro": (out.width - i.width) // 2, "izquierda": 0, "derecha": out.width - i.width}[op["alinear"]]
            out.alpha_composite(i, (x, n * paso))
    if op["rotar"]:
        out = out.rotate(op["rotar"], resample=Image.BICUBIC, expand=True)
    caja = out.getbbox()
    return out.crop(caja) if caja else out


def contorno(capa, grosor, color):
    con_margen = Image.new("RGBA", (capa.width + grosor * 2, capa.height + grosor * 2), capa.getpixel((0, 0))[:3] + (0,))
    con_margen.paste(capa, (grosor, grosor))
    capa = con_margen
    alfa = capa.getchannel("A").filter(ImageFilter.MaxFilter(grosor * 2 + 1))
    borde = Image.new("RGBA", capa.size, tuple(color) + (0,))
    borde.putalpha(alfa)
    return Image.alpha_composite(borde, capa)


def pegar(destino, img, pos):
    """Pega `img` (RGBA) sobre `destino` transparente sin oscurecer los bordes."""
    capa = Image.new("RGBA", destino.size, (0, 0, 0, 0))
    capa.paste(img, pos)
    return Image.alpha_composite(destino, capa)


def rehacer(orig, texto, op):
    W, H = orig.size
    if not texto.strip() or medir(orig, op["umbral"])[1] is None:  # trozo vacio (o que sobra en espanol)
        fondo = op["fondo"] if op["fondo"] != "auto" else ("transparente" if es_transparente(orig) else "negro")
        return Image.new("RGBA", (W, H), (0, 0, 0, 255 if fondo == "negro" else 0))
    nucleo, todo = medir(orig, op["umbral"])
    caja = op["caja"] or nucleo
    color = op["color"] or color_trazo(orig, nucleo)
    if op["color_inicial"] == "auto":  # color de la primera letra del original (la parte mas saturada a la izquierda)
        izq = orig.convert("RGB").crop((todo[0], todo[1], todo[0] + max(4, (todo[2] - todo[0]) // 10), todo[3]))
        op = dict(op, color_inicial=max(izq.getdata(), key=lambda p: max(p) - min(p)))
    img = dibujar_texto(texto, op, color)
    if op["contorno"]:
        img = contorno(img, max(1, op["contorno"] * 4), op["color_contorno"] or color)  # a escala del dibujo (x4 aprox)
    if op["borde"]:
        cb = color_halo(orig, nucleo, todo) if op["color_borde"] == "auto" else op["color_borde"]
        img = contorno(img, max(1, op["borde"] * 4), cb or (255, 255, 255))
    alto = op["alto"] or (caja[3] - caja[1]) * op["escala_alto"]
    esc = alto / img.height
    ancho_max = op["ancho_max"] or min(W - 16, (caja[2] - caja[0]) * op["escala_ancho"])
    if img.width * esc > ancho_max:
        esc = ancho_max / img.width
    img = img.resize((max(1, round(img.width * esc)), max(1, round(img.height * esc))), Image.LANCZOS)
    cx, cy = (caja[0] + caja[2]) / 2, (caja[1] + caja[3]) / 2
    x = {"centro": cx - img.width / 2, "izquierda": caja[0], "derecha": caja[2] - img.width}[op["alinear"]]
    capa = Image.new("RGBA", (W, H), tuple(color) + (0,))
    capa.paste(img, (int(round(x)), int(round(cy - img.height / 2))))

    brillo = op["brillo"]
    if brillo == "auto":
        exceso = ((todo[2] - todo[0]) - (nucleo[2] - nucleo[0]) + (todo[3] - todo[1]) - (nucleo[3] - nucleo[1])) / 4
        brillo = exceso if exceso > 2 else False
    if brillo:
        base = capa
        color_b = color_halo(orig, nucleo, todo) if op["color_brillo"] == "auto" else op["color_brillo"]
        if color_b:
            base = Image.new("RGBA", capa.size, tuple(color_b) + (0,))
            base.putalpha(capa.getchannel("A"))
        halo = Image.new("RGBA", capa.size, (0, 0, 0, 0))
        for r, k in ((brillo * 0.5, 0.9), (brillo, 0.7), (brillo * 2, 0.5)):
            h = base.filter(ImageFilter.GaussianBlur(r))
            h.putalpha(h.getchannel("A").point(lambda v, k=k: min(255, int(v * k * op["fuerza_brillo"] * 1.6))))
            halo = Image.alpha_composite(halo, h)
        capa = Image.alpha_composite(halo, capa)

    if op["desenfoque"]:
        capa = capa.filter(ImageFilter.GaussianBlur(op["desenfoque"]))
    if op["recorte_original"]:
        mascara = luminancia(orig).point(lambda v: 255 if v > 24 else 0).filter(ImageFilter.MaxFilter(9))
        capa.putalpha(ImageChops.multiply(capa.getchannel("A"), mascara))
    fondo = op["fondo"]
    if fondo == "auto":
        fondo = "transparente" if es_transparente(orig) else "negro"
    if fondo == "negro":
        return Image.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), capa)
    return capa


# ---------------------------------------------------------------------------
# Recetas
# ---------------------------------------------------------------------------
def opciones(receta, entrada):
    op = dict(OPCIONES)
    op.update(receta.get("estilo", {}))
    if isinstance(entrada, dict):
        if "usar" in entrada:
            op.update(receta.get("estilos", {})[entrada["usar"]])
        op.update({k: v for k, v in entrada.items() if k not in ("texto", "usar")})
    return op


def procesar(ruta_receta, data_win, salida, previas):
    with open(ruta_receta, encoding="utf-8") as f:
        receta = json.load(f)
    origen = os.path.join(data_win, receta["spc"])
    originales = {t.nombre: t for ts in drv3srd.texturas_de_spc(origen).values() for t in ts}
    carpeta = os.path.join(previas, os.path.splitext(os.path.basename(receta["spc"]))[0]) if previas else tempfile.mkdtemp()
    os.makedirs(carpeta, exist_ok=True)
    for textura, entrada in receta["textos"].items():
        t = originales[textura + ".png"]
        orig = Image.frombytes("RGBA", (t.ancho, t.alto), bytes(t.rgba()))
        texto = entrada["texto"] if isinstance(entrada, dict) else entrada
        img = rehacer(orig, texto, opciones(receta, entrada))
        img.save(os.path.join(carpeta, textura + ".png"))
        print(f"  {textura}: {texto.replace('|', ' / ')}")
    destino = os.path.join(salida, receta["spc"])
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    return drv3srd.importar(origen, carpeta, destino)


def main(argv):
    args = argv[1:]
    def sacar(nombre):
        if nombre in args:
            i = args.index(nombre)
            v = args[i + 1]
            del args[i:i + 2]
            return v
        return None
    data_win, salida, previas = sacar("--juego"), sacar("--salida"), sacar("--png")
    if not args or not data_win or not salida:
        print(__doc__)
        return 2
    for r in args:
        print(r)
        if procesar(r, data_win, salida, previas):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
