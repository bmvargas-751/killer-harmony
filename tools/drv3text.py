#!/usr/bin/env python3
"""Lee y edita los textos de Danganronpa V3 dentro de archivos .SPC (contenedores CPS.) con .stx.

Formatos portados de V3Lib (https://github.com/redssu/Harmony-Tools, dependencies/V3Lib).

Uso:
    drv3text.py dump <carpeta_o_spc>... > textos.tsv
        Vuelca todas las lineas como TSV: archivo, subarchivo, id, texto (saltos de linea como \\n).

    drv3text.py apply <correcciones.tsv> [--root <carpeta>] [--dry-run]
        Aplica correcciones. Cada linea del TSV: archivo<TAB>subarchivo<TAB>id<TAB>texto_viejo<TAB>texto_nuevo
        El texto viejo debe coincidir exactamente con el actual (si no, se aborta sin escribir nada).

    drv3text.py verify <carpeta_o_spc>...
        Comprueba que cada SPC/STX se reconstruye byte a byte (para validar la herramienta).
"""
import os
import struct
import sys

SPC_WINDOW = 1024
SPC_MAX_SEQ = 65


def _reverse_bits(b):
    return int(f"{b:08b}"[::-1], 2)


_REV = bytes(_reverse_bits(i) for i in range(256))


# ---------------------------------------------------------------------------
# SPC
# ---------------------------------------------------------------------------
class SpcSubfile:
    def __init__(self, name, data, compression, unknown, original_size):
        self.name = name
        self.data = data  # datos tal como estan en el archivo (comprimidos o no)
        self.compression = compression
        self.unknown = unknown
        self.original_size = original_size

    def decompressed(self):
        if self.compression != 2:
            return self.data
        data, out = self.data, bytearray()
        flag, pos, size = 1, 0, len(data)
        while pos < size:
            if flag == 1:
                flag = 0x100 | _REV[data[pos]]
                pos += 1
            if pos >= size:
                break
            if flag & 1:
                out.append(data[pos])
                pos += 1
            else:
                b = data[pos] | (data[pos + 1] << 8)
                pos += 2
                count = (b >> 10) + 2
                offset = b & (SPC_WINDOW - 1)
                for _ in range(count):
                    out.append(out[len(out) - SPC_WINDOW + offset])
            flag >>= 1
        return bytes(out)

    def set_content(self, raw):
        """Reemplaza el contenido (sin comprimir) y lo comprime igual que V3Lib."""
        self.original_size = len(raw)
        self.data = compress(raw)
        self.compression = 2


def compress(raw):
    """Port exacto de SpcSubfile.Compress() de V3Lib."""
    size = len(raw)
    out = bytearray()
    pos = 0
    flag = 0
    bit = 0
    block = bytearray()
    while True:
        if bit == 8 or pos >= size:
            out.append(_REV[flag])
            out += block
            if pos >= size:
                break
            flag, bit, block = 0, 0, bytearray()

        seq_len = 1
        found_at = -1
        back = min(pos, SPC_WINDOW)
        while seq_len <= SPC_MAX_SEQ:
            ahead = min(seq_len - 1, size - pos)
            if pos + seq_len > size:
                seq_len -= 1
                break
            start = pos - back
            last = found_at
            idx = raw.rfind(raw[pos:pos + seq_len], start, pos + ahead)
            found_at = idx - start if idx != -1 else -1
            if found_at == -1:
                found_at = last
                seq_len -= 1
                break
            seq_len += 1
        if seq_len > SPC_MAX_SEQ:
            seq_len = SPC_MAX_SEQ

        if seq_len >= 2 and found_at != -1:
            rep = (SPC_WINDOW - back + found_at) | ((seq_len - 2) << 10)
            block += struct.pack("<H", rep & 0xFFFF)
        else:
            flag |= 1 << bit
            block.append(raw[pos])
        pos += max(1, seq_len)
        bit += 1
    return bytes(out)


class SpcFile:
    def __init__(self, path):
        with open(path, "rb") as f:
            buf = f.read()
        if buf[:4] != b"CPS.":
            raise ValueError(f"{path}: no es un SPC (magic {buf[:4]!r})")
        self.unknown1 = buf[4:0x28]
        count, self.unknown2 = struct.unpack_from("<ii", buf, 0x28)
        if buf[0x40:0x44] != b"Root":
            raise ValueError(f"{path}: tabla 'Root' no encontrada")
        pos = 0x50
        self.subfiles = []
        for _ in range(count):
            comp, unk, cur, orig, name_len = struct.unpack_from("<hhiii", buf, pos)
            pos += 16 + 0x10
            name = buf[pos:pos + name_len].decode("shift-jis")
            pos += name_len + (0x10 - (name_len + 1) % 0x10) % 0x10 + 1
            data = buf[pos:pos + cur]
            pos += cur + (0x10 - cur % 0x10) % 0x10
            self.subfiles.append(SpcSubfile(name, data, comp, unk, orig))

    def to_bytes(self):
        out = bytearray(b"CPS.")
        out += self.unknown1
        out += struct.pack("<ii", len(self.subfiles), self.unknown2)
        out += bytes(0x10) + b"Root" + bytes(0x0C)
        for s in self.subfiles:
            name = s.name.encode("shift-jis")
            out += struct.pack("<hhiii", s.compression, s.unknown, len(s.data), s.original_size, len(name))
            out += bytes(0x10)
            out += name + bytes((0x10 - (len(name) + 1) % 0x10) % 0x10 + 1)
            out += s.data + bytes((0x10 - len(s.data) % 0x10) % 0x10)
        return bytes(out)


# ---------------------------------------------------------------------------
# STX
# ---------------------------------------------------------------------------
class StxFile:
    def __init__(self, raw):
        if raw[:8] != b"STXTJPLL":
            raise ValueError("no es STX")
        table_count, table_offset = struct.unpack_from("<iI", raw, 8)
        info = []
        pos = 0x10
        for _ in range(table_count):
            info.append(struct.unpack_from("<II", raw, pos))
            pos += 16
        pos = table_offset
        self.tables = []  # lista de (unknown, dict id -> texto)
        offsets = []
        for unknown, n in info:
            elems = {}
            for _ in range(n):
                sid, off = struct.unpack_from("<II", raw, pos)
                pos += 8
                offsets.append(off)
                if sid in elems:
                    continue
                end = off
                while raw[end:end + 2] != b"\x00\x00":
                    end += 2
                elems[sid] = raw[off:end].decode("utf-16-le")
            self.tables.append((unknown, elems))
        self.dedupe = len(set(offsets)) < len(offsets)

    def to_bytes(self):
        out = bytearray(b"STXTJPLL")
        out += struct.pack("<iI", len(self.tables), 0)
        for unknown, elems in self.tables:
            out += struct.pack("<IiQ", unknown, len(elems), 0)
        struct.pack_into("<I", out, 0x0C, len(out))
        pairs_pos = len(out)
        out += bytes(sum(8 * len(e) for _, e in self.tables))
        for _, elems in self.tables:
            written = {}
            for sid, text in elems.items():
                # Las cadenas repetidas solo se comparten si el archivo original lo hacia
                if self.dedupe and text in written:
                    off = written[text]
                else:
                    off = len(out)
                    written[text] = off
                    out += text.encode("utf-16-le") + b"\x00\x00"
                struct.pack_into("<II", out, pairs_pos, sid, off)
                pairs_pos += 8
        return bytes(out)


# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------
def iter_spc(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for f in sorted(files):
                    if f.lower().endswith(".spc"):
                        yield os.path.join(root, f)
        else:
            yield p


def escape(text):
    return text.replace("\\", "\\\\").replace("\t", "\\t").replace("\r", "\\r").replace("\n", "\\n")


def unescape(text):
    out, i = [], 0
    while i < len(text):
        c = text[i]
        if c == "\\" and i + 1 < len(text):
            out.append({"n": "\n", "r": "\r", "t": "\t", "\\": "\\"}.get(text[i + 1], "\\" + text[i + 1]))
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def cmd_dump(paths):
    for spc_path in iter_spc(paths):
        spc = SpcFile(spc_path)
        for s in spc.subfiles:
            raw = s.decompressed()
            if raw[:8] != b"STXTJPLL":
                continue
            stx = StxFile(raw)
            for _, elems in stx.tables:
                for sid, text in elems.items():
                    print(f"{spc_path}\t{s.name}\t{sid}\t{escape(text)}")


def cmd_verify(paths):
    ok = True
    for spc_path in iter_spc(paths):
        with open(spc_path, "rb") as f:
            original = f.read()
        spc = SpcFile(spc_path)
        problems = []
        if spc.to_bytes() != original:
            problems.append("contenedor SPC")
        for s in spc.subfiles:
            raw = s.decompressed()
            if len(raw) != s.original_size:
                problems.append(f"{s.name}: tamano descomprimido")
            if s.compression == 2 and compress(raw) != s.data:
                problems.append(f"{s.name}: compresion")
            if raw[:8] == b"STXTJPLL" and StxFile(raw).to_bytes() != raw:
                problems.append(f"{s.name}: STX")
        if problems:
            ok = False
            print(f"[DIFERENTE] {spc_path}: {', '.join(problems[:5])}")
        else:
            print(f"[OK] {spc_path}")
    return 0 if ok else 1


def cmd_apply(corrections_path, root=".", dry_run=False):
    cambios = {}
    with open(corrections_path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            partes = line.split("\t")
            if len(partes) != 5:
                sys.exit(f"{corrections_path}:{n}: se esperaban 5 columnas, hay {len(partes)}")
            archivo, sub, sid, viejo, nuevo = partes
            cambios.setdefault(archivo, []).append((n, sub, int(sid), unescape(viejo), unescape(nuevo)))

    errores = []
    resultados = {}
    for archivo, lista in cambios.items():
        ruta = os.path.join(root, archivo)
        spc = SpcFile(ruta)
        por_nombre = {s.name: s for s in spc.subfiles}
        stx_mod = {}
        for n, sub, sid, viejo, nuevo in lista:
            if sub not in por_nombre:
                errores.append(f"linea {n}: {archivo} no contiene {sub}")
                continue
            stx = stx_mod.get(sub) or StxFile(por_nombre[sub].decompressed())
            stx_mod[sub] = stx
            tabla = next((e for _, e in stx.tables if sid in e), None)
            if tabla is None:
                errores.append(f"linea {n}: {sub} no tiene el id {sid}")
            elif tabla[sid] != viejo:
                errores.append(f"linea {n}: el texto actual de {sub}#{sid} no coincide:\n    actual:   {tabla[sid]!r}\n    esperado: {viejo!r}")
            else:
                tabla[sid] = nuevo
        for sub, stx in stx_mod.items():
            por_nombre[sub].set_content(stx.to_bytes())
        resultados[ruta] = (spc, len(lista))

    if errores:
        print("No se aplico nada. Errores:", file=sys.stderr)
        for e in errores:
            print("  " + e, file=sys.stderr)
        return 1
    for ruta, (spc, n) in resultados.items():
        print(f"{'[simulado] ' if dry_run else ''}{ruta}: {n} correcciones")
        if not dry_run:
            with open(ruta, "wb") as f:
                f.write(spc.to_bytes())
    return 0


def main(argv):
    if len(argv) < 2 or argv[1] not in ("dump", "apply", "verify"):
        print(__doc__)
        return 2
    if argv[1] == "dump":
        cmd_dump(argv[2:])
        return 0
    if argv[1] == "verify":
        return cmd_verify(argv[2:])
    args = argv[2:]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    root = "."
    if "--root" in args:
        i = args.index("--root")
        root = args[i + 1]
        del args[i:i + 2]
    return cmd_apply(args[0], root, dry)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
