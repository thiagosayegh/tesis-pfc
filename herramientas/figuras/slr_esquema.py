"""Esquema de la prueba SLR (Fig. 4.4) con el mismo estilo que el del NOR (28 oct. 2026): arena circular
gris vista desde arriba con las tres señales espaciales, las tazas reales del SLR (recortadas de
figuras/Fig4_objetos_SLR.jpg) y la rata de la ilustración de la Dra. Kruse (figuras/fuentes/Sol_Figura7_NOL.png).
Filas: d-SLR y s-SLR; columnas: día 1 (muestreo, 10 min) y día 2 (prueba, 5 min).
Las posiciones son esquemáticas (ángulos de §4.3.3; las distancias en cm no se dibujan).
Uso:  python herramientas/figuras/slr_esquema.py  ->  figuras/Fig4_SLR_protocolo.png
"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")) + os.sep
FIG = R + "figuras" + os.sep
SERIF = "c:/texlive/2026/texmf-dist/fonts/truetype/google/noto/NotoSerif-Regular.ttf"
SERIFB = "c:/texlive/2026/texmf-dist/fonts/truetype/google/noto/NotoSerif-Bold.ttf"
F = lambda t, b=False: ImageFont.truetype(SERIFB if b else SERIF, t)

# ---------------------------------------------------------------- recortes
def recorte_taza():
    im = np.asarray(Image.open(FIG + "Fig4_objetos_SLR.jpg").convert("RGB")).astype(int)
    L = im.mean(axis=2); sat = im.max(axis=2) - im.min(axis=2)
    m = (sat > 25) | (L > ndimage.uniform_filter(L, 61) + 10)
    m = ndimage.binary_closing(m, iterations=4); m = ndimage.binary_fill_holes(m)
    m = ndimage.binary_opening(m, iterations=2); m = ndimage.binary_erosion(m, iterations=3)
    m[:, 395:] = False                               # solo la taza (la rana está a la derecha)
    o = Image.fromarray(im.astype("uint8")).convert("RGBA")
    o.putalpha(Image.fromarray((m * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1)))
    return o.crop(o.getbbox())

def recorte_rata():
    f7 = Image.open(FIG + "fuentes" + os.sep + "Sol_Figura7_NOL.png").convert("RGB")
    r = np.asarray(f7.crop((770, 312, 905, 540))).astype(int)
    a = (r.mean(axis=2) > 105) & ((r[..., 0] - r[..., 2]) < 70)
    a[:40, 60:] = False
    lab, _ = ndimage.label(ndimage.binary_dilation(a, iterations=2))
    a &= lab == (np.bincount(lab.ravel())[1:].argmax() + 1)
    o = Image.fromarray(r.astype("uint8")).convert("RGBA")
    o.putalpha(Image.fromarray((a * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.8)))
    return o.crop(o.getbbox())                      # vertical, cabeza arriba

TAZA, RATA = recorte_taza(), recorte_rata()

# ---------------------------------------------------------------- arena
S, RP, RW = 680, 268, 300                           # lienzo, radio del piso, radio exterior de la pared
C = S / 2
def arena():
    y, x = np.mgrid[0:S, 0:S]
    d = np.hypot(x - C, y - C)
    img = np.full((S, S, 3), 255.0)
    rng = np.random.default_rng(1)
    piso = 196 + 14 * (1 - d / RP) + rng.normal(0, 2.2, (S, S))          # gris claro, más claro al centro
    pared = 150 + 45 * (RW - d) / (RW - RP)                              # pared en perspectiva
    for k, c in enumerate((1.0, 1.0, 1.04)):
        img[..., k] = np.where(d <= RP, piso * c, np.where(d <= RW, pared * c, 255))
    # sombra suave de la pared sobre el piso
    sombra = np.clip((d - (RP - 18)) / 18, 0, 1) * (d <= RP)
    img *= (1 - 0.18 * sombra)[..., None]
    base = Image.fromarray(np.clip(img, 0, 255).astype("uint8")).convert("RGBA")
    dr = ImageDraw.Draw(base)
    dr.ellipse((C - RW, C - RW, C + RW, C + RW), outline=(95, 95, 95), width=3)
    dr.ellipse((C - RP, C - RP, C + RP, C + RP), outline=(130, 130, 130), width=2)
    # la pared es lisa (Thiago, 28 oct. 2026): sin carteles; las señales espaciales están en la sala
    return base

def cartel(base, ang, tipo):
    w, h = 96, 30
    c = Image.new("RGBA", (w, h), "white")
    d = ImageDraw.Draw(c)
    if tipo == "rayas":
        for x in range(0, w, 12): d.rectangle((x, 0, x + 5, h), fill="black")
    elif tipo == "damero":
        for i in range(0, w, 10):
            for j in range(0, h, 10):
                if (i // 10 + j // 10) % 2: d.rectangle((i, j, i + 9, j + 9), fill="black")
    else:
        for x in range(8, w, 20): d.ellipse((x - 6, 9, x + 6, 21), fill="black")
    d.rectangle((0, 0, w - 1, h - 1), outline="black", width=2)
    c = c.rotate(ang - 90, expand=True, resample=Image.BICUBIC)
    rr = (RP + RW) / 2
    cx, cy = C + rr * math.cos(math.radians(ang)), C - rr * math.sin(math.radians(ang))
    base.alpha_composite(c, (round(cx - c.width / 2), round(cy - c.height / 2)))

def pos(ang, r=0.60 * RP):
    return C + r * math.cos(math.radians(ang)), C - r * math.sin(math.radians(ang))

def pegar(base, img, centro, alto):
    img = img.resize((round(img.width * alto / img.height), alto), Image.LANCZOS)
    x, y = round(centro[0] - img.width / 2), round(centro[1] - img.height / 2)
    s = Image.new("RGBA", img.size, (0, 0, 0, 0)); s.putalpha(img.getchannel("A").point(lambda v: v * 0.45))
    base.alpha_composite(s.filter(ImageFilter.GaussianBlur(4)), (x + 4, y + 5))
    base.alpha_composite(img, (x, y))
    return x, y, x + img.width, y + img.height

def rotulo(base, xy, t):
    d = ImageDraw.Draw(base)
    d.text(xy, t, font=F(26, True), fill=(25, 25, 25), anchor="mm", stroke_width=3, stroke_fill=(235, 235, 235))

def angulo(base, a1, a2, texto):
    """Líneas punteadas del centro a dos objetos y el ángulo entre ellos."""
    d = ImageDraw.Draw(base)
    for a in (a1, a2):
        x, y = pos(a, 0.47 * RP)
        n = 14
        for k in range(0, n, 2):
            d.line((C + (x - C) * k / n, C + (y - C) * k / n, C + (x - C) * (k + 1) / n, C + (y - C) * (k + 1) / n), fill=(80, 80, 80), width=2)
    r = 46
    p1, p2 = sorted((-a1 % 360, -a2 % 360))            # ángulos de PIL (sentido horario desde las 3)
    d.arc((C - r, C - r, C + r, C + r), start=p1, end=p2, fill=(80, 80, 80), width=2)
    pm = math.radians((p1 + p2) / 2)
    d.text((C + 80 * math.cos(pm), C + 80 * math.sin(pm)), texto, font=F(22, True), fill=(60, 60, 60), anchor="mm")

ALTO_TAZA = 70
def muestreo(angs, abre):
    b = arena()
    angulo(b, angs[1], angs[2], abre)
    for k, a in enumerate(angs):
        x0, y0, x1, y1 = pegar(b, TAZA, pos(a), ALTO_TAZA)
        rx, ry = pos(a, 0.60 * RP + (52 if k == 0 else 50))
        rotulo(b, (rx, ry) if k else ((x0 + x1) / 2, y1 + 22), f"A{k + 1}")
    # rata caminando cerca del centro, mirando a A1
    pegar(b, RATA.rotate(-40, expand=True), (C + 95, C - 55), 150)
    return b

def prueba(angs):
    b = arena()
    d = ImageDraw.Draw(b)
    for a in angs[1:]:                                # posiciones que ocupaban A2 y A3
        x, y = pos(a)
        for k in range(0, 360, 24):
            d.arc((x - 27, y - 27, x + 27, y + 27), k, k + 12, fill=(90, 90, 90), width=3)
    x0, y0, x1, y1 = pegar(b, TAZA, pos(angs[0]), ALTO_TAZA)
    rotulo(b, ((x0 + x1) / 2, y1 + 22), "A1 (familiar)")
    xn, yn = pos(-90)
    x0, y0, x1, y1 = pegar(b, TAZA, (xn, yn), ALTO_TAZA)
    rotulo(b, (xn, y1 + 22), "N (novedosa)")
    # rata olfateando el objeto en la posición novedosa, desde arriba
    pegar(b, RATA.rotate(180, expand=True).rotate(-15, expand=True), (xn - 22, yn - 112), 155)
    return b

D_SLR = (90, -30, 210)                               # A1, A2, A3: equidistantes a 120°
S_SLR = (90, -65, -115)                              # A2 y A3 a 50°; A1 a igual distancia de ambos
celdas = [[muestreo(D_SLR, "120°"), prueba(D_SLR)], [muestreo(S_SLR, "50°"), prueba(S_SLR)]]

# ---------------------------------------------------------------- composición
AZUL, NARANJA, VERDE = (226, 231, 240), (250, 228, 214), (222, 236, 222)
ML, MT, GX, GY, FL, MR = 90, 130, 0, 30, 150, 150
W = ML + 2 * S + FL + MR
H = MT + 2 * S + GY
L = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(L)
xs = [ML, ML + S + FL]
for x, (t, sub), col in zip(xs, (("Día 1: fase de muestreo", "10 min · tres objetos iguales"),
                                  ("Día 2: fase de prueba", "5 min · un objeto en posición novedosa")), (NARANJA, VERDE)):
    d.rounded_rectangle((x + 20, 4, x + S - 20, MT - 18), radius=22, fill=col, outline=(70, 70, 70), width=3)
    d.text((x + S / 2, 42), t, font=F(36, True), fill="black", anchor="mm")
    d.text((x + S / 2, 86), sub, font=F(27), fill="black", anchor="mm")
for i, fila in enumerate(celdas):
    y = MT + i * (S + GY)
    for x, img in zip(xs, fila):
        L.paste(img.convert("RGB"), (x, y))
    # flecha de 24 h entre los dos días
    yc, x0, x1, h = y + S / 2, ML + S + 8, ML + S + FL - 8, 96
    d.polygon([(x0, yc - h * .32), (x1 - 44, yc - h * .32), (x1 - 44, yc - h / 2), (x1, yc), (x1 - 44, yc + h / 2),
               (x1 - 44, yc + h * .32), (x0, yc + h * .32)], fill=(200, 200, 200))
    d.text(((x0 + x1 - 30) / 2, yc), "24 h", font=F(30, True), fill="black", anchor="mm")
    # rótulo de la fila, vertical
    t = Image.new("RGBA", (S, 60), (255, 255, 255, 0))
    ImageDraw.Draw(t).text((S / 2, 30), ("d-SLR (separación grande)", "s-SLR (separación pequeña)")[i],
                           font=F(32, True), fill="black", anchor="mm")
    t = t.rotate(90, expand=True)
    L.paste(t, (14, y), t)
# flecha de mayor demanda cognitiva
xa = W - MR / 2
d.line((xa, MT + 60, xa, H - 70), fill=(60, 60, 60), width=14)
d.polygon([(xa - 30, H - 80), (xa + 30, H - 80), (xa, H - 20)], fill=(60, 60, 60))
t = Image.new("RGBA", (S + 200, 60), (255, 255, 255, 0))
ImageDraw.Draw(t).text(((S + 200) / 2, 30), "Mayor demanda cognitiva", font=F(32, True), fill=(40, 40, 40), anchor="mm")
t = t.rotate(-90, expand=True)
L.paste(t, (round(xa + 14), round(MT + (H - MT) / 2 - t.height / 2)), t)
L.save(FIG + "Fig4_SLR_protocolo.png", dpi=(300, 300))
print("SLR:", L.size)
