#!/usr/bin/env python3
"""Cambia la respuesta de un anagrama (Epifania Anagramica) dentro de minigame/anagram/anagram_US.SPC.

Cada respuesta es una tabla answerNNN.dat con una fila por letra:
    文字 (letra), 表示前 (letra que se ve antes de acertar), X_Offset (posicion), パラメータ (rotacion, Monokuma...)
Las letras son indices a una lista de textos UTF-16 (la letra 0 es la inicial y la 1 es el recuadro vacio).
Para no tocar el diseno, la respuesta nueva debe tener la misma cantidad de letras que la anterior; se
conservan los parametros de cada ficha. Si las palabras tienen los mismos largos (ej. "DESLIZO DEL TECHO"
-> "TOBOGAN DEL TECHO") tambien se conservan las posiciones; si no, se recalculan como en el juego:
90 px por letra y 120 px entre palabras (ej. "AMNESI A" -> "AMNESIA").

Uso:
    anagrama.py listar <anagram_US.SPC>
    anagrama.py cambiar <anagram_US.SPC> <answerNNN.dat> "<RESPUESTA>"
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drv3text import SpcFile  # noqa: E402

VACIO = "□"


def _cadenas(d, p, cantidad, ancho):
    res = []
    for _ in range(cantidad):
        if ancho == 1:
            e = d.index(b"\0", p)
            res.append(d[p:e].decode("utf-8"))
            p = e + 1
        else:
            e = p
            while d[e:e + 2] != b"\0\0":
                e += 2
            res.append(d[p:e].decode("utf-16-le"))
            p = e + 2
    return res, p


def leer(d):
    filas, tam, ncol = struct.unpack_from("<III", d, 0)
    p, cols = 12, []
    for _ in range(ncol):
        e = d.index(b"\0", p)
        nombre = d[p:e]
        p = e + 1
        e = d.index(b"\0", p)
        tipo = d[p:e]
        p = e + 1
        cols.append((nombre, tipo, d[p:p + 2]))
        p += 2
    while p % 16:
        p += 1
    cabecera = d[:p]
    tabla = [list(struct.unpack_from("<" + "H" * (tam // 2), d, p + i * tam)) for i in range(filas)]
    p += filas * tam
    n_ascii, n_utf16 = struct.unpack_from("<HH", d, p)
    p += 4
    ascii_, p = _cadenas(d, p, n_ascii, 1)
    if p % 2:
        p += 1
    utf16, p = _cadenas(d, p, n_utf16, 2)
    return cabecera, tabla, ascii_, utf16


def escribir(cabecera, tabla, ascii_, utf16):
    out = bytearray(cabecera)
    for fila in tabla:
        out += struct.pack("<" + "H" * len(fila), *fila)
    out += struct.pack("<HH", len(ascii_), len(utf16))
    for s in ascii_:
        out += s.encode("utf-8") + b"\0"
    if len(out) % 2:
        out += b"\0"
    for s in utf16:
        out += s.encode("utf-16-le") + b"\0\0"
    return bytes(out)


def respuesta(tabla, utf16):
    texto, x_prev = "", None
    for letra, _antes, x, _param in tabla:
        if x_prev is not None and x - x_prev > 90:
            texto += " "
        texto += utf16[letra]
        x_prev = x
    return texto


def cambiar(tabla, utf16, nueva):
    vieja = respuesta(tabla, utf16)
    letras = nueva.replace(" ", "")
    if len(letras) != len(tabla):
        sys.exit(f"'{nueva}' no tiene la misma cantidad de letras que '{vieja}'")
    if [len(w) for w in vieja.split()] != [len(w) for w in nueva.split()]:
        x, i = 0, 0
        for palabra in nueva.split():
            for _ in palabra:
                tabla[i][2] = x
                x += 90
                i += 1
            x += 30
    lista = [letras[0], VACIO]
    for c in letras[1:]:
        if c not in lista:
            lista.append(c)
    for fila, c in zip(tabla, letras):
        fila[0] = lista.index(c)
    return lista


def main(argv):
    if len(argv) < 3 or argv[1] not in ("listar", "cambiar"):
        sys.exit(__doc__)
    spc = SpcFile(argv[2])
    for s in spc.subfiles:
        if not s.name.startswith("answer"):
            continue
        cab, tabla, ascii_, utf16 = leer(s.decompressed())
        assert escribir(cab, tabla, ascii_, utf16) == s.decompressed(), s.name
        if argv[1] == "listar":
            print(f"{s.name}\t{respuesta(tabla, utf16)}")
        elif s.name == argv[3]:
            antes = respuesta(tabla, utf16)
            utf16 = cambiar(tabla, utf16, argv[4])
            s.set_content(escribir(cab, tabla, ascii_, utf16))
            with open(argv[2], "wb") as f:
                f.write(spc.to_bytes())
            print(f"{s.name}: {antes} -> {respuesta(tabla, utf16)}")
            return 0
    if argv[1] == "cambiar":
        sys.exit(f"No se encontro {argv[3]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
