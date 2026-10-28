"""Esquemas de Métodos a partir de las ilustraciones que mandó la Dra. Kruse (28 oct. 2026), hechas con
IA para otra tesina del laboratorio (figuras/fuentes/Sol_Figura5_OF.png y Sol_Figura7_NOL.png).

- Fig4_OF_zonas_IA.png / Fig4_OF_rearing_IA.png: recortes de la Figura 5 (arena del OF con las tres
  zonas y rata en rearing; se deja afuera el grooming, que no se midió). Los compone componer.py.
- Fig4_NOR_protocolo.png: protocolo del NOR con el estilo de la Figura 7 (que es de una prueba NOL,
  que no se hizo acá): se usa su caja negra vacía y su rata, y se pegan los objetos reales del NOR
  (recortes de figuras/Fig5_NOR_objetos_T*.png).
Uso:  python herramientas/figuras/esquemas_ia.py   (después, componer.py para la figura del OF)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")) + os.sep
FIG = R + "figuras" + os.sep
FUE = FIG + "fuentes" + os.sep
SERIF = "c:/texlive/2026/texmf-dist/fonts/truetype/google/noto/NotoSerif-Regular.ttf"
SERIFB = "c:/texlive/2026/texmf-dist/fonts/truetype/google/noto/NotoSerif-Bold.ttf"

# ---------------------------------------------------------------- OF (Figura 5 de Sol)
f5 = Image.open(FUE + "Sol_Figura5_OF.png").convert("RGB")
f5.crop((96, 38, 1000, 898)).save(FIG + "Fig4_OF_zonas_IA.png")        # sin la letra "a"
f5.crop((1215, 535, 1565, 830)).save(FIG + "Fig4_OF_rearing_IA.png")   # sin la letra "c" ni el rótulo

# ---------------------------------------------------------------- NOR
f7 = Image.open(FUE + "Sol_Figura7_NOL.png").convert("RGB")
caja = f7.crop((38, 172, 568, 600))                  # caja de la habituación (con la rata abajo a la izquierda)
W, H = caja.size

# caja vacía: se borra la rata de la habituación (última fila del piso, y 291-387, x 70-350).
# Hasta la línea de la cuadrícula en x = 146 se copia la misma zona de la caja espejada (la caja es
# simétrica y ese lado está vacío); desde ahí el espejo caería sobre la propia rata, así que se copia
# la fila de baldosas de arriba (96 px más arriba), corregida por la diferencia de iluminación.
c = np.asarray(caja).astype(float)
vac = c.copy()
Y0, Y1, YL, XC, DY = 291, 388, 380, 146, 96          # YL: debajo, sin copiar la línea horizontal de arriba
vac[Y0:Y1, 70:XC] = c[Y0:Y1, ::-1][:, 70:XC]
gan = c[Y0:YL, 380:470].mean(axis=(1, 2)) / c[Y0 - DY:YL - DY, 380:470].mean(axis=(1, 2))
vac[Y0:YL, XC:350] = c[Y0 - DY:YL - DY, XC:350] * gan[:, None, None]
vac[YL:Y1, XC:350] = vac[YL - 1, XC:350][None]       # el borde inferior del piso es liso
vacia = Image.fromarray(np.clip(vac, 0, 255).astype("uint8"))

def recorte_rata():
    """Rata de la Prueba 1 de la Figura 7 (vertical, cabeza arriba), con canal alfa."""
    r = np.asarray(f7.crop((770, 312, 905, 540))).astype(int)
    brillo = r.mean(axis=2)
    alfa = (brillo > 105) & ((r[..., 0] - r[..., 2]) < 70)
    alfa[:40, 60:] = False                           # el objeto "Izq" que toca la nariz
    a = Image.fromarray((alfa * 255).astype("uint8")).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    im = Image.fromarray(r.astype("uint8")).convert("RGBA")
    im.putalpha(a)
    return im.crop(im.getbbox())

def recortes_objetos(arch):
    """(izquierdo, derecho) de una foto de objetos sobre fondo oscuro uniforme."""
    im = np.asarray(Image.open(FIG + arch).convert("RGB")).astype(int)
    fondo = np.median(im[:15].reshape(-1, 3), axis=0)
    alfa = np.abs(im - fondo).max(axis=2) > 38
    out = []
    mitad = im.shape[1] // 2
    for xa, xb in ((0, mitad), (mitad, im.shape[1])):
        sub = np.zeros_like(alfa); sub[:, xa:xb] = alfa[:, xa:xb]
        a = Image.fromarray((sub * 255).astype("uint8")).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(0.7))
        o = Image.fromarray(im.astype("uint8")).convert("RGBA"); o.putalpha(a)
        out.append(o.crop(a.getbbox()))
    return out

def sombra(img, desp=(5, 6)):
    s = Image.new("RGBA", img.size, (0, 0, 0, 0))
    s.putalpha(img.getchannel("A").point(lambda v: v * 0.55))
    return s.filter(ImageFilter.GaussianBlur(5)), desp

def pegar(base, img, centro, alto):
    img = img.resize((round(img.width * alto / img.height), alto), Image.LANCZOS)
    x, y = round(centro[0] - img.width / 2), round(centro[1] - img.height / 2)
    s, (dx, dy) = sombra(img)
    base.alpha_composite(s, (x + dx, y + dy))
    base.alpha_composite(img, (x, y))
    return (x, y, x + img.width, y + img.height)

RATA = recorte_rata()
IZQ, DER = (150, 205), (380, 205)                    # posiciones de los objetos dentro de la caja
ALTO_OBJ = 72

def ensayo(arch, rotulos=None, explora="der"):
    b = vacia.convert("RGBA")
    oi, od = recortes_objetos(arch)
    ri = pegar(b, oi, IZQ, ALTO_OBJ)
    rd = pegar(b, od, DER, ALTO_OBJ)
    # rata olfateando un objeto, desde abajo
    rata = RATA if explora == "der" else RATA.transpose(Image.FLIP_LEFT_RIGHT)
    cx = (DER if explora == "der" else IZQ)[0] + (-14 if explora == "der" else 14)
    pegar(b, rata, (cx, (rd[3] if explora == "der" else ri[3]) + 78), 165)
    if rotulos:
        d = ImageDraw.Draw(b); f = ImageFont.truetype(SERIFB, 24)
        for rr, t in ((ri, rotulos[0]), (rd, rotulos[1])):
            cx = (rr[0] + rr[2]) / 2
            d.text((cx, rr[1] - 10), t, font=f, fill="white", anchor="ms")
    return b.convert("RGB")

# ---------------------------------------------------------------- composición
ESC = 1.25
def panel(img, titulo, sub, color):
    img = img.resize((round(W * ESC), round(H * ESC)), Image.LANCZOS)
    hh = 118
    p = Image.new("RGB", (img.width, hh + 18 + img.height), "white")
    d = ImageDraw.Draw(p)
    d.rounded_rectangle((2, 2, img.width - 3, hh), radius=22, fill=color, outline=(70, 70, 70), width=3)
    d.text((img.width / 2, 50), titulo, font=ImageFont.truetype(SERIFB, 40), fill="black", anchor="mm")
    d.text((img.width / 2, 92), sub, font=ImageFont.truetype(SERIF, 30), fill="black", anchor="mm")
    p.paste(img, (0, hh + 18))
    return p

def flecha(d, x0, x1, yc, texto):
    """Flecha gris gruesa con el intervalo adentro, como en la Figura 7."""
    h = 120
    d.polygon([(x0, yc - h * 0.32), (x1 - 55, yc - h * 0.32), (x1 - 55, yc - h / 2), (x1, yc),
               (x1 - 55, yc + h / 2), (x1 - 55, yc + h * 0.32), (x0, yc + h * 0.32)], fill=(200, 200, 200))
    d.text(((x0 + x1 - 40) / 2, yc), texto, font=ImageFont.truetype(SERIFB, 34), fill="black", anchor="mm")

AZUL, NARANJA, VERDE = (226, 231, 240), (250, 228, 214), (222, 236, 222)
hab = panel(caja, "Habituación", "5 min durante 3 días", AZUL)
t1 = panel(ensayo("Fig5_NOR_objetos_T1.png", explora="izq"), "Fase de muestreo (T1)", "5 min · dos objetos iguales", NARANJA)
t2 = panel(ensayo("Fig5_NOR_objetos_T2.png", ("F", "N")), "T2 (corto plazo)", "2 h después de T1 · 5 min", VERDE)
t3 = panel(ensayo("Fig5_NOR_objetos_T3.png", ("F", "N")), "T3 (largo plazo)", "24 h después de T1 · 5 min", VERDE)
t4 = panel(ensayo("Fig5_NOR_objetos_T4.png", ("F", "N")), "T4 (memoria consolidada)", "7 días después de T1 · 5 min", VERDE)

pw, ph = hab.size
gap, fl = 60, 230
ancho = 3 * pw + 2 * gap
fila1 = 2 * pw + fl
lienzo = Image.new("RGB", (ancho, ph * 2 + 170), "white")
d = ImageDraw.Draw(lienzo)
x = (ancho - fila1) // 2
lienzo.paste(hab, (x, 0)); lienzo.paste(t1, (x + pw + fl, 0))
flecha(d, x + pw + 25, x + pw + fl - 25, 118 + 18 + (ph - 136) // 2, "24 h")
# de T1 a los tres ensayos de elección
y2 = ph + 170
cx1 = x + pw + fl + pw // 2
ybar = ph + 85
d.line((cx1, ph + 10, cx1, ybar), fill=(120, 120, 120), width=6)
xs = [pw // 2 + k * (pw + gap) for k in range(3)]
d.line((xs[0], ybar, xs[2], ybar), fill=(120, 120, 120), width=6)
for xx in xs:
    d.line((xx, ybar, xx, y2 - 22), fill=(120, 120, 120), width=6)
    d.polygon([(xx - 18, y2 - 26), (xx + 18, y2 - 26), (xx, y2 - 2)], fill=(120, 120, 120))
for k, im in enumerate((t2, t3, t4)):
    lienzo.paste(im, (k * (pw + gap), y2))
lienzo.save(FIG + "Fig4_NOR_protocolo.png", dpi=(300, 300))
print("NOR:", lienzo.size)

# ---------------------------------------------------------------- rata para la línea temporal (Fig. 4.1)
# la rata caminando de la habituación de la Figura 7, con fondo transparente y mirando a la derecha
r = np.asarray(f7.crop((110, 455, 390, 575))).astype(int)
alfa = (r.mean(axis=2) > 100) & ((r[..., 0] - r[..., 2]) < 90)
from scipy import ndimage                            # solo la rata: la mancha conexa más grande
lab, n = ndimage.label(ndimage.binary_dilation(alfa, iterations=2))
alfa &= lab == (np.bincount(lab.ravel())[1:].argmax() + 1)
a = Image.fromarray((alfa * 255).astype("uint8")).filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
rata = Image.fromarray(r.astype("uint8")).convert("RGBA"); rata.putalpha(a)
rata = rata.crop(rata.getbbox()).transpose(Image.FLIP_LEFT_RIGHT)
rata.save(FIG + "Fig4_rata_IA.png")
print("rata:", rata.size)
