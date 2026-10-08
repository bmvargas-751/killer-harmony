#!/usr/bin/env python3
"""Aplica una lista de erratas (texto_erroneo<TAB>texto_correcto) a los textos del parche.

Uso:
    aplicar_erratas.py <erratas.tsv> [--carpeta latest] [--dry-run]

- Las reglas normales reemplazan palabras completas. Una regla en minusculas tambien
  corrige sus variantes Capitalizada y MAYUSCULAS.
- Las reglas que empiezan con "=" reemplazan ese texto literal exacto ("\\n" = salto de linea).
- Muestra cada cambio, avisa de reglas que no encontraron nada y escribe los SPC
  usando drv3text (que verifica el texto original antes de escribir).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drv3text  # noqa: E402

LETRA = r"[^\W\d_]"


def cargar_reglas(ruta):
    literales, palabras = [], []
    with open(ruta, encoding="utf-8") as f:
        for n, linea in enumerate(f, 1):
            linea = linea.rstrip("\n")
            if not linea.strip() or linea.startswith("#"):
                continue
            partes = linea.split("\t")
            if len(partes) != 2:
                sys.exit(f"{ruta}:{n}: se esperaban 2 columnas")
            viejo, nuevo = partes
            if viejo.startswith("="):
                literales.append((n, drv3text.unescape(viejo[1:]), drv3text.unescape(nuevo)))
            else:
                palabras.append((n, viejo, nuevo))
    return literales, palabras


def variantes(viejo, nuevo):
    """(viejo, nuevo) en minusculas, Capitalizado y MAYUSCULAS si la regla es minuscula."""
    if viejo != viejo.lower():
        return [(viejo, nuevo)]
    cap = lambda s: s[:1].upper() + s[1:]  # noqa: E731
    return [(viejo, nuevo), (cap(viejo), cap(nuevo)), (viejo.upper(), nuevo.upper())]


def compilar_palabras(palabras):
    """Una sola expresion para todas las palabras: {variante: (n_regla, reemplazo)}."""
    tabla = {}
    for n, viejo, nuevo in palabras:
        for v, nv in variantes(viejo, nuevo):
            tabla[v] = (n, nv)
    alternativas = "|".join(re.escape(v) for v in sorted(tabla, key=len, reverse=True))
    return re.compile(rf"(?<!{LETRA})(?:{alternativas})(?!{LETRA})"), tabla


def corregir(texto, literales, patron, tabla, usadas):
    for n, viejo, nuevo in literales:
        if viejo in texto:
            texto = texto.replace(viejo, nuevo)
            usadas.add(n)

    def reemplazo(m):
        n, nuevo = tabla[m.group(0)]
        usadas.add(n)
        return nuevo

    return patron.sub(reemplazo, texto)


def main(argv):
    args = argv[1:]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    carpeta = "latest"
    if "--carpeta" in args:
        i = args.index("--carpeta")
        carpeta = args[i + 1]
        del args[i:i + 2]
    if len(args) != 1:
        print(__doc__)
        return 2

    literales, palabras = cargar_reglas(args[0])
    patron, tabla = compilar_palabras(palabras)
    usadas = set()
    cambios = []
    for spc_path in drv3text.iter_spc([carpeta]):
        spc = drv3text.SpcFile(spc_path)
        for s in spc.subfiles:
            raw = s.decompressed()
            if raw[:8] != b"STXTJPLL":
                continue
            for _, elems in drv3text.StxFile(raw).tables:
                for sid, texto in elems.items():
                    nuevo = corregir(texto, literales, patron, tabla, usadas)
                    if nuevo != texto:
                        cambios.append((spc_path, s.name, sid, texto, nuevo))

    for spc_path, sub, sid, viejo, nuevo in cambios:
        print(f"{os.path.basename(spc_path)} {sub}#{sid}")
        print(f"  - {drv3text.escape(viejo)}")
        print(f"  + {drv3text.escape(nuevo)}")
    sin_uso = [n for n, *_ in literales + palabras if n not in usadas]
    print(f"\n{len(cambios)} lineas modificadas.")
    if sin_uso:
        print(f"[!] Reglas sin coincidencias (lineas de {args[0]}): {sin_uso}")

    tmp = os.path.join(carpeta, ".correcciones.tmp.tsv")
    with open(tmp, "w", encoding="utf-8") as f:
        for spc_path, sub, sid, viejo, nuevo in cambios:
            f.write(f"{os.path.relpath(spc_path)}\t{sub}\t{sid}\t{drv3text.escape(viejo)}\t{drv3text.escape(nuevo)}\n")
    try:
        return drv3text.cmd_apply(tmp, ".", dry)
    finally:
        os.remove(tmp)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
