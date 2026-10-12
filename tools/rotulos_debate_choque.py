#!/usr/bin/env python3
"""Rehace en espanol las preguntas del Debate de Choque (flash/trial/program/t_scm_topic*).

Cada pregunta mezcla dos estilos por palabra:
  - "relleno": letras lilas con brillo morado (serif en t_scm_topic_tx, letra cuadrada en la version en bucle).
  - "contorno": letras serif celestes, solo el contorno.
Hay cuatro texturas por pregunta:
  t_scm_topic/t_scm_topic_tx_00N_US                 serif, transparente, en una o dos lineas
  t_scm_topic_a/t_scm_topic_loop_tx_00N_US_DXT1     en bucle, una linea, fondo negro
  t_scm_topic_a/t_scm_topic_tx_grw_00N_US_DXT1      copia borrosa de la primera
  t_scm_topic_a/t_scm_topic_loop_tx_grw_00N_US_DXT1 copia borrosa de la segunda
El tamano de letra se calibra con el texto en ingles de la textura original (mismo alto de tinta) y
el desenfoque de las copias borrosas se mide comparandolas con el original.

Uso:
    rotulos_debate_choque.py --juego <data/win del juego> --salida <carpeta win> [--png <previas>] [--ingles]
    --ingles dibuja el texto original en ingles (sirve para comparar con el juego y calibrar).
"""
import os
import sys
import tempfile

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drv3srd  # noqa: E402
from rotulos_fuente import ruta_fuente  # noqa: E402

R, C = "relleno", "contorno"
# Cada pregunta: lineas de la version de una o dos lineas; la version en bucle las une en una sola.
PREGUNTAS = {
    0: {"en": [[(R, "Is Shuichi the "), (C, "culprit"), (R, " ?")]],
        "es": [[(R, "¿Es Shuichi el "), (C, "culpable"), (R, "?")]]},
    1: {"en": [[(R, "When was "), (C, "the body put in")], [(R, "the piranha tank?")]],
        "es": [[(R, "¿Cuándo pusieron "), (C, "el cuerpo")], [(C, "en el "), (R, "tanque de pirañas?")]]},
    2: {"en": [[(C, "Vote "), (R, "for Korekiyo?")]],
        "es": [[(C, "¿Votar "), (R, "por Korekiyo?")]]},
    3: {"en": [[(C, "Could "), (R, "Gonta have")], [(C, "committed the crime"), (R, "?")]],
        "es": [[(C, "¿Pudo "), (R, "Gonta haber")], [(C, "cometido el crimen"), (R, "?")]]},
    4: {"en": [[(C, "Which one "), (R, "is dead?")]],
        "es": [[(C, "¿Cuál "), (R, "está muerto?")]]},
}

COLOR_RELLENO = (196, 206, 224)
COLOR_BRILLO = (154, 28, 233)
COLOR_CONTORNO = (0, 255, 255)

# (fuente, peso, escala horizontal, espacio extra entre letras en fraccion del tamano)
FUENTES = {
    ("serif", R): ("EBGaramond", 600, 1.0, 0.04),
    ("cuadrada", R): ("RussoOne", None, 0.8, 0.0),
    ("serif", C): ("EBGaramond", 500, 1.0, 0.04),
    ("cuadrada", C): ("EBGaramond", 500, 1.0, 0.0),
}


def fuente(familia, estilo, tam):
    nombre, peso, condensar, espaciado = FUENTES[(familia, estilo)]
    f = ImageFont.truetype(ruta_fuente(nombre), tam)
    if peso is not None:
        f.set_variation_by_axes([peso])
    return f, condensar, espaciado * tam


def mascara_tramo(texto, familia, estilo, tam):
    """Mascara (L) del tramo, con la linea base en y = tam."""
    f, condensar, espaciado = fuente(familia, estilo, tam)
    largo = f.getlength(texto) + espaciado * len(texto)
    ancho = int(largo) + tam
    img = Image.new("L", (ancho, tam * 2), 0)
    d, x = ImageDraw.Draw(img), 0.0
    for i, ch in enumerate(texto):
        d.text((x, tam), ch, font=f, fill=255, anchor="ls")
        x += f.getlength(texto[:i + 1]) - f.getlength(texto[:i]) + espaciado
    if condensar != 1.0:
        img = img.resize((max(1, int(ancho * condensar)), img.height), Image.LANCZOS)
    return img, int(largo * condensar)


def mascaras_linea(linea, familia, tam):
    """Mascaras de relleno y contorno de una linea, recortadas a la tinta. Devuelve (relleno, contorno)."""
    piezas, x = [], 0
    for estilo, texto in linea:
        m, avance = mascara_tramo(texto, familia, estilo, tam)
        piezas.append((estilo, m, x))
        x += avance
    ancho = x + tam
    rel = Image.new("L", (ancho, tam * 2), 0)
    con = Image.new("L", (ancho, tam * 2), 0)
    for estilo, m, x in piezas:
        destino = rel if estilo == R else con
        destino.paste(ImageChops.lighter(destino.crop((x, 0, x + m.width, m.height)), m), (x, 0))
    x0, y0, x1, y1 = ImageChops.lighter(rel, con).getbbox()
    return rel.crop((x0, 0, x1, rel.height)), con.crop((x0, 0, x1, rel.height)), y0, y1


def a_contorno(m, grosor):
    """Deja solo el borde exterior del trazo (letra hueca)."""
    afuera = m.filter(ImageFilter.MaxFilter(grosor * 2 + 1))
    return ImageChops.subtract(afuera, m.filter(ImageFilter.MinFilter(3)))


def componer(lineas, tam_textura, fondo_negro, radio_brillo=4):
    """Pinta las lineas. lineas: [(mascara_relleno, mascara_contorno, x, y_arriba, escala, ancho_max)].
    La mascara se escala completa (con su linea base), y si queda mas ancha que ancho_max se estrecha."""
    w, h = tam_textura
    rel = Image.new("L", (w, h), 0)
    con = Image.new("L", (w, h), 0)
    for mr, mc, x, y, escala, ancho_max in lineas:
        nw = min(int(mr.width * escala), ancho_max)
        nh = int(mr.height * escala)
        for destino, m in ((rel, mr), (con, mc)):
            m2 = m.resize((nw, nh), Image.LANCZOS)
            capa = Image.new("L", (w, h), 0)
            capa.paste(m2, (x, y))
            destino.paste(ImageChops.lighter(destino, capa))
    con = a_contorno(con, 2)
    brillo = rel.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(radio_brillo))
    brillo = brillo.point(lambda v: int(v * 0.8))
    capa = Image.new("RGBA", (w, h), COLOR_BRILLO + (0,))
    capa.putalpha(brillo)
    for color, m in ((COLOR_RELLENO, rel), (COLOR_CONTORNO, con)):
        s = Image.new("RGBA", (w, h), color + (0,))
        s.putalpha(m)
        capa.alpha_composite(s)
    if fondo_negro:
        negro = Image.new("RGBA", (w, h), (0, 0, 0, 255))
        negro.alpha_composite(capa)
        return negro
    return capa


def cajas_lineas(orig, n_lineas):
    """Cajas de tinta de cada linea del original (separadas por filas vacias)."""
    a = orig.getchannel("A") if orig.mode == "RGBA" and orig.getchannel("A").getextrema()[0] < 200 else orig.convert("L")
    a = a.point(lambda v: 255 if v > 100 else 0)
    filas = [any(a.getpixel((x, y)) for x in range(0, a.width, 2)) for y in range(a.height)]
    tramos, y = [], 0
    while y < len(filas):
        if filas[y]:
            y0 = y
            while y < len(filas) and filas[y]:
                y += 1
            tramos.append((y0, y))
        y += 1
    # unir tramos cortos (acentos, puntos) con el vecino hasta tener n_lineas
    while len(tramos) > n_lineas:
        i = min(range(len(tramos)), key=lambda k: tramos[k][1] - tramos[k][0])
        j = i - 1 if i == len(tramos) - 1 or (i > 0 and tramos[i][0] - tramos[i - 1][1] < tramos[i + 1][0] - tramos[i][1]) else i + 1
        a0, b0 = sorted((i, j))
        tramos[a0:b0 + 1] = [(tramos[a0][0], tramos[b0][1])]
    cajas = []
    for y0, y1 in tramos:
        x0, _, x1, _ = a.crop((0, y0, a.width, y1)).getbbox()
        cajas.append((x0, y0, x1, y1))
    return cajas


def medir_desenfoque(nitido, borroso):
    """Busca el radio y la ganancia con que la textura borrosa sale de la nitida."""
    base = nitido.convert("RGB").resize((nitido.width // 4, nitido.height // 4), Image.BILINEAR)
    obj = borroso.convert("RGB").resize(base.size, Image.BILINEAR)
    mejor = None
    for r in range(1, 12):
        b = base.filter(ImageFilter.GaussianBlur(r))
        num = sum(p * q for x, y in zip(b.getdata(), obj.getdata()) for p, q in zip(x, y))
        den = sum(p * p for x in b.getdata() for p in x) or 1
        k = num / den
        err = sum((p * k - q) ** 2 for x, y in zip(b.getdata(), obj.getdata()) for p, q in zip(x, y))
        if mejor is None or err < mejor[0]:
            mejor = (err, r * 4, k)
    return mejor[1], mejor[2]


def borrosa(img, radio, ganancia):
    b = img.convert("RGB").filter(ImageFilter.GaussianBlur(radio))
    return b.point(lambda v: min(255, int(v * ganancia))).convert("RGBA")


def exportar(spc, carpeta):
    os.makedirs(carpeta, exist_ok=True)
    drv3srd.exportar(spc, carpeta)
    return {os.path.splitext(f)[0]: Image.open(os.path.join(carpeta, f)).convert("RGBA")
            for f in os.listdir(carpeta) if f.endswith(".png")}


def procesar(n, data_win, salida, previas, idioma):
    lineas = PREGUNTAS[n][idioma]
    ingles = PREGUNTAS[n]["en"]
    rutas = {
        "tx": f"flash/trial/program/t_scm_topic/t_scm_topic_tx_{n:03d}_US.spc",
        "loop": f"flash/trial/program/t_scm_topic_a/t_scm_topic_loop_tx_{n:03d}_US_DXT1.spc",
        "tx_grw": f"flash/trial/program/t_scm_topic_a/t_scm_topic_tx_grw_{n:03d}_US_DXT1.spc",
        "loop_grw": f"flash/trial/program/t_scm_topic_a/t_scm_topic_loop_tx_grw_{n:03d}_US_DXT1.spc",
    }
    with tempfile.TemporaryDirectory() as tmp:
        orig = {}
        for clave, rel in rutas.items():
            texs = exportar(os.path.join(data_win, rel), os.path.join(tmp, clave))
            (nombre, img), = texs.items()
            orig[clave] = (nombre, img)

        nuevas = {}
        # Version serif (una o dos lineas): la escala y la linea base salen de rehacer el ingles
        # sobre la caja de tinta de cada linea del original.
        if len(lineas) != len(ingles):
            sys.exit(f"pregunta {n}: el espanol debe tener {len(ingles)} lineas")
        nombre, img = orig["tx"]
        cajas = cajas_lineas(img, len(ingles))
        alin = ["centro"] if len(cajas) == 1 else ["izquierda", "derecha"]
        medidas = []
        for (x0, y0, x1, y1), l_en in zip(cajas, ingles):
            _, _, t, b = mascaras_linea(l_en, "serif", 200)
            medidas.append(((y1 - y0) / (b - t), y0, t))
        escala = sum(m[0] for m in medidas) / len(medidas)
        colocar = []
        for (x0, y0, x1, y1), a, l_es, (_, ye, t) in zip(cajas, alin, lineas, medidas):
            mr, mc, _, _ = mascaras_linea(l_es, "serif", 200)
            ancho = int(mr.width * escala)
            if a == "izquierda":
                x = x0
                ancho_max = img.width - 40 - x
            elif a == "derecha":
                x = max(40, x1 - ancho)
                ancho_max = x1 - x
            else:
                x = max(40, (x0 + x1) // 2 - ancho // 2)
                ancho_max = img.width - 40 - x
            colocar.append((mr, mc, x, int(ye - t * escala), escala, ancho_max))
        nuevas["tx"] = componer(colocar, img.size, fondo_negro=False)

        # Version en bucle: una sola linea, fondo negro
        def unir(ls):
            res = []
            for t in [t for l in ls for t in l]:
                if res and not res[-1][1].endswith(" ") and not t[1].startswith((" ", "?")):
                    t = (t[0], " " + t[1])
                res.append(t)
            return res
        nombre, img = orig["loop"]
        (x0, y0, x1, y1), = cajas_lineas(img, 1)
        _, _, t, b = mascaras_linea(unir(ingles), "cuadrada", 200)
        escala = (y1 - y0) / (b - t)
        mr, mc, _, _ = mascaras_linea(unir(lineas), "cuadrada", 200)
        ancho = min(int(mr.width * escala), img.width - 32)
        x = (x0 + x1) // 2 - ancho // 2
        x = max(16, min(x, img.width - 16 - ancho))
        nuevas["loop"] = componer([(mr, mc, x, int(y0 - t * escala), escala, ancho)], img.size, fondo_negro=True)

        # Copias borrosas: mismo desenfoque que el original
        for clave, base in (("tx_grw", "tx"), ("loop_grw", "loop")):
            _, nitido = orig[base]
            negro = Image.new("RGBA", nitido.size, (0, 0, 0, 255))
            negro.alpha_composite(nitido)
            radio, ganancia = medir_desenfoque(negro, orig[clave][1])
            fuente_img = Image.new("RGBA", nitido.size, (0, 0, 0, 255))
            fuente_img.alpha_composite(nuevas[base])
            nuevas[clave] = borrosa(fuente_img, radio, ganancia)
            print(f"  {orig[clave][0]}: desenfoque {radio}px, ganancia {ganancia:.2f}")

        for clave, rel in rutas.items():
            nombre = orig[clave][0]
            carpeta = os.path.join(tmp, "nuevas_" + clave)
            os.makedirs(carpeta)
            nuevas[clave].save(os.path.join(carpeta, nombre + ".png"))
            if previas:
                os.makedirs(previas, exist_ok=True)
                nuevas[clave].save(os.path.join(previas, nombre + ".png"))
            if salida:
                destino = os.path.join(salida, rel)
                os.makedirs(os.path.dirname(destino), exist_ok=True)
                drv3srd.importar(os.path.join(data_win, rel), carpeta, destino)
        print(f"Pregunta {n}: " + " / ".join("".join(t for _, t in l) for l in lineas))


def main(argv):
    def sacar(nombre):
        if nombre in argv:
            i = argv.index(nombre)
            valor = argv[i + 1]
            del argv[i:i + 2]
            return valor
        return None
    juego, salida, previas = sacar("--juego"), sacar("--salida"), sacar("--png")
    idioma = "en" if "--ingles" in argv else "es"
    if not juego or not (salida or previas):
        sys.exit(__doc__)
    for n in PREGUNTAS:
        procesar(n, juego, salida, previas, idioma)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
