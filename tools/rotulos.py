#!/usr/bin/env python3
"""Genera rotulos de interfaz en espanol reutilizando las letras de las propias texturas del juego.

Cada receta (JSON en tools/rotulos/) indica:
  - "spc": archivo a traducir, relativo a data/win (ej. "flash/techou/techou_system_US.spc").
  - "fuentes": texturas de donde se recortan las letras y el texto que contienen:
        ["<spc relativo a data/win>", "<textura sin .png>", "<texto>", <compresion_horizontal>]
    El texto usa "|" para separar lineas. La compresion indica si el diseno original ya
    estrecho esa palabra (ej. 25/28 = 0.893 si las letras miden 25 px en vez de 28).
  - "estilo": parametros del trazo y del brillo (calibrados contra las texturas originales).
  - "textos": {"<textura sin .png>": "<TEXTO EN ESPANOL>"}.
  - "tildes": letras acentuadas que se dibujan sobre la letra base, ej. {"Ú": "U"}.

El proceso: se separa el trazo (blanco puro) del brillo, se recorta cada letra por proyeccion,
se componen las palabras (estrechando las largas como en el original), se dibujan las tildes
que no existen en el juego y se regenera el brillo. El resultado se importa con drv3srd.

Uso:
    rotulos.py <receta.json> <carpeta data/win del juego> <salida> [--png carpeta_previsualizacion]
Ejemplo:
    rotulos.py tools/rotulos/menu_pausa.json "C:/.../Danganronpa V3 Killing Harmony/data/win" latest/win
"""
import json
import math
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drv3srd  # noqa: E402


# ---------------------------------------------------------------------------
# Imagen de un canal (0..1)
# ---------------------------------------------------------------------------
class Img:
    def __init__(self, w, h, v=None):
        self.w, self.h = w, h
        self.v = v if v is not None else [0.0] * (w * h)

    def get(self, x, y):
        return self.v[y * self.w + x] if 0 <= x < self.w and 0 <= y < self.h else 0.0

    def recortar(self, x0, y0, x1, y1):
        out = Img(x1 - x0, y1 - y0)
        for y in range(y0, y1):
            for x in range(x0, x1):
                out.v[(y - y0) * out.w + (x - x0)] = self.get(x, y)
        return out


def desenfocar(img, sigma):
    r = int(math.ceil(sigma * 3))
    k = [math.exp(-(i * i) / (2 * sigma * sigma)) for i in range(-r, r + 1)]
    t = sum(k)
    k = [x / t for x in k]
    tmp, out = Img(img.w, img.h), Img(img.w, img.h)
    for y in range(img.h):
        for x in range(img.w):
            tmp.v[y * img.w + x] = sum(k[i + r] * img.get(x + i, y) for i in range(-r, r + 1))
    for y in range(img.h):
        for x in range(img.w):
            out.v[y * img.w + x] = sum(k[i + r] * tmp.get(x, y + i) for i in range(-r, r + 1))
    return out


# ---------------------------------------------------------------------------
# Letras
# ---------------------------------------------------------------------------
def trazo(textura, bajo):
    """Separa el trazo del brillo: rampa de luminancia entre `bajo` y 1."""
    rgba = textura.rgba()
    v = [max(rgba[i * 4:i * 4 + 3]) / 255.0 for i in range(textura.ancho * textura.alto)]
    return Img(textura.ancho, textura.alto, [min(1.0, max(0.0, (x - bajo) / (1 - bajo))) for x in v])


def segmentar(core, umbral=0.5):
    """[[(x0, x1, y0, y1) por letra] por linea], por proyeccion horizontal y vertical."""
    def tramos(n, hay):
        res, ini = [], None
        for i in range(n + 1):
            h = i < n and hay(i)
            if h and ini is None:
                ini = i
            if not h and ini is not None:
                res.append((ini, i))
                ini = None
        return res
    lineas = tramos(core.h, lambda y: any(core.get(x, y) > umbral for x in range(core.w)))
    return [[(x0, x1, y0, y1) for x0, x1 in tramos(core.w, lambda x: any(core.get(x, y) > umbral for y in range(y0, y1)))]
            for y0, y1 in lineas]


def con_tilde(img):
    """Letra con tilde: paralelogramo inclinado sobre la letra, con antialias (supersampling 4x4)."""
    extra = 9
    out = Img(img.w, img.h + extra)
    for y in range(img.h):
        for x in range(img.w):
            out.v[(y + extra) * img.w + x] = img.get(x, y)
    cx = img.w / 2 + 1
    poly = [(cx - 3, extra - 2), (cx + 3, extra - 2), (cx + 9, 1), (cx + 3, 1)]

    def dentro(px, py):
        c = False
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
            if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1:
                c = not c
        return c

    for y in range(extra):
        for x in range(img.w):
            k = sum(dentro(x + (i + .5) / 4, y + (j + .5) / 4) for i in range(4) for j in range(4)) / 16
            out.v[y * img.w + x] = max(out.v[y * img.w + x], k)
    return out


def biblioteca(receta, data_win):
    """{letra: (Img del trazo, compresion)} prefiriendo las letras de ancho normal."""
    est = receta["estilo"]
    lib, cache = {}, {}
    for spc, textura, texto, comp in receta["fuentes"]:
        if spc not in cache:
            cache[spc] = {t.nombre: t for ts in drv3srd.texturas_de_spc(os.path.join(data_win, spc)).values() for t in ts}
        core = trazo(cache[spc][textura + ".png"], est["nucleo_bajo"])
        lineas = segmentar(core)
        palabras = [p.replace(" ", "") for p in texto.split("|")]
        for letras, palabra in zip(lineas, palabras):
            if len(letras) != len(palabra):
                raise ValueError(f"{textura}: se detectaron {len(letras)} letras para '{palabra}'")
            for (x0, x1, y0, y1), c in zip(letras, palabra):
                if c not in lib or lib[c][1] < comp:
                    lib[c] = (core.recortar(x0 - 1, y0, x1 + 1, y1), comp)
    for acentuada, base in receta.get("tildes", {}).items():
        if base in lib:
            lib[acentuada] = (con_tilde(lib[base][0]), lib[base][1])
    return lib


def componer(lib, texto, w, h, est):
    faltan = sorted({c for c in texto if c not in "| " and c not in lib})
    if faltan:
        raise ValueError(f"'{texto}': faltan letras {faltan} (habra que dibujarlas)")
    lienzo = Img(w, h)
    lineas = texto.split("|")
    gap, alto = est["espacio"], est["alto"]
    for linea, yl in zip(lineas, est["lineas_y"][str(len(lineas))]):
        letras = [c for c in linea if c != " "]
        natural = sum(lib[c][0].w / lib[c][1] for c in letras) + gap * (len(letras) - 1) + est["espacio_palabra"] * linea.count(" ")
        escala = min(1.0, est["ancho_max"] / natural)
        anchos = [int(round(lib[c][0].w * escala / lib[c][1])) for c in letras]
        total = sum(anchos) + gap * (len(letras) - 1) + est["espacio_palabra"] * linea.count(" ")
        x = int(round((w - total) / 2))
        i = 0
        for c in linea:
            if c == " ":
                x += est["espacio_palabra"]
                continue
            g, gw, e = lib[c][0], anchos[i], escala / lib[c][1]
            dy = yl + alto - g.h
            for yy in range(g.h):
                for xx in range(gw):
                    sx = xx / e
                    x0 = int(sx)
                    f = sx - x0
                    v = g.get(x0, yy) * (1 - f) + g.get(x0 + 1, yy) * f
                    px, py = x + xx, dy + yy
                    if 0 <= px < w and 0 <= py < h:
                        lienzo.v[py * w + px] = max(lienzo.v[py * w + px], v)
            x += gw + gap
            i += 1
    capas = [(desenfocar(lienzo, s), k) for s, k in est["brillo"]]
    return Img(w, h, [max(c, min(1.0, sum(k * b.v[i] for b, k in capas))) for i, c in enumerate(lienzo.v)])


def main(argv):
    args = argv[1:]
    previa = None
    if "--png" in args:
        i = args.index("--png")
        previa = args[i + 1]
        del args[i:i + 2]
    if len(args) != 3:
        print(__doc__)
        return 2
    ruta_receta, data_win, salida = args
    with open(ruta_receta, encoding="utf-8") as f:
        receta = json.load(f)
    lib = biblioteca(receta, data_win)
    origen = os.path.join(data_win, receta["spc"])
    originales = {t.nombre: t for ts in drv3srd.texturas_de_spc(origen).values() for t in ts}
    carpeta = previa or tempfile.mkdtemp()
    os.makedirs(carpeta, exist_ok=True)
    color = receta["estilo"].get("color", [255, 255, 255])
    for textura, texto in receta["textos"].items():
        t = originales[textura + ".png"]
        img = componer(lib, texto, t.ancho, t.alto, receta["estilo"])
        rgba = bytearray(t.ancho * t.alto * 4)
        for i, v in enumerate(img.v):
            rgba[i * 4:i * 4 + 4] = bytes((int(color[0] * v), int(color[1] * v), int(color[2] * v), 255))
        drv3srd.guardar_png(os.path.join(carpeta, textura + ".png"), t.ancho, t.alto, rgba)
        print(f"{textura}: {texto.replace('|', ' / ')}")
    return drv3srd.importar(origen, carpeta, os.path.join(salida, receta["spc"]))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
