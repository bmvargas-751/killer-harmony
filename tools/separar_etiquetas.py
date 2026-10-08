#!/usr/bin/env python3
"""Agrega el espacio que falta junto a las etiquetas de formato <CLT=...>.

El juego no agrega espacios alrededor de las etiquetas, asi que
"del<CLT=cltSTRONG>Pianista Definitivo<CLT=cltNORMAL>sabe" se ve como
"delPianista Definitivosabe". Se inserta un espacio justo despues de la etiqueta
(el mismo criterio que ya usa el parche: "del<CLT=cltSTRONG> Pianista").

Solo actua cuando el caracter visible anterior y el siguiente son del alfabeto
latino (letra/numero, o puntuacion de cierre antes y de apertura despues), para no
tocar el texto en japones que quedo en algunos archivos.

Uso:
    separar_etiquetas.py [--carpeta latest] [--dry-run]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drv3text  # noqa: E402

ETIQUETAS = re.compile(r"(?:<CLT=[^>]*>)+")
CIERRE = set(",.;:!?…)]”")
APERTURA = set("¿¡([“")


def latina(c):
    return c.isalnum() and ord(c) < 0x2000


def separar(texto):
    partes, ultimo = [], 0
    for m in ETIQUETAS.finditer(texto):
        antes = ETIQUETAS.sub("", texto[:m.start()])
        despues = ETIQUETAS.sub("", texto[m.end():])
        partes.append(texto[ultimo:m.end()])
        ultimo = m.end()
        if not antes or not despues:
            continue
        x, y = antes[-1], despues[0]
        if (latina(x) or x in CIERRE) and (latina(y) or y in APERTURA):
            partes.append(" ")
    partes.append(texto[ultimo:])
    return "".join(partes)


def main(argv):
    args = argv[1:]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    carpeta = "latest"
    if "--carpeta" in args:
        carpeta = args[args.index("--carpeta") + 1]

    cambios = []
    for spc_path in drv3text.iter_spc([carpeta]):
        spc = drv3text.SpcFile(spc_path)
        for s in spc.subfiles:
            raw = s.decompressed()
            if raw[:8] != b"STXTJPLL":
                continue
            for _, elems in drv3text.StxFile(raw).tables:
                for sid, texto in elems.items():
                    nuevo = separar(texto)
                    if nuevo != texto:
                        cambios.append((spc_path, s.name, sid, texto, nuevo))

    for spc_path, sub, sid, viejo, nuevo in cambios:
        print(f"{os.path.basename(spc_path)} {sub}#{sid}")
        print(f"  - {drv3text.escape(viejo)}")
        print(f"  + {drv3text.escape(nuevo)}")
    print(f"\n{len(cambios)} lineas modificadas.")

    tmp = os.path.join(carpeta, ".separar.tmp.tsv")
    with open(tmp, "w", encoding="utf-8") as f:
        for spc_path, sub, sid, viejo, nuevo in cambios:
            f.write(f"{os.path.relpath(spc_path)}\t{sub}\t{sid}\t{drv3text.escape(viejo)}\t{drv3text.escape(nuevo)}\n")
    try:
        return drv3text.cmd_apply(tmp, ".", dry)
    finally:
        os.remove(tmp)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
