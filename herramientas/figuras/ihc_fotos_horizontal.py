"""Reacomoda las fotomicrografías de IHC (figuras/Fig5_IHC_fotos.png: 4 filas de grupos x 2 columnas,
PCNA y DCX) en 2 filas (PCNA, DCX) x 4 columnas (grupos), para que la figura sea ancha y baja y no deje
una página a medio llenar (28 oct. 2026). Las fotos no se tocan: solo se recortan y se reubican; la
barra de escala queda en la foto DCX del sacarosa adulto, como en el original.
Uso:  python herramientas/figuras/ihc_fotos_horizontal.py  ->  figuras/Fig5_IHC_fotos_horizontal.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")) + os.sep
FIG = R + "figuras" + os.sep
ARIALB = "C:/Windows/Fonts/arialbd.ttf"

src = Image.open(FIG + "Fig5_IHC_fotos.png").convert("RGB")
COLS = [(53, 309), (324, 582)]                       # PCNA, DCX
FILAS = [(48, 319), (346, 616), (649, 917), (951, 1221)]
GRUPOS = ["Control juvenil", "Sacarosa juvenil", "Control adulto", "Sacarosa adulto"]
MARC = ["PCNA", "DCX"]

tw, th = 258, 272                                     # tamaño común de cada foto
ML, MT, G = 70, 70, 14                                # margen izquierdo (rótulos), superior, separación
W = ML + 4 * tw + 3 * G
H = MT + 2 * th + G
out = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(out)
f = ImageFont.truetype(ARIALB, 26)
for j, (y0, y1) in enumerate(FILAS):
    for i, (x0, x1) in enumerate(COLS):
        foto = src.crop((x0, y0, x1, y1)).resize((tw, th), Image.LANCZOS)
        out.paste(foto, (ML + j * (tw + G), MT + i * (th + G)))
    d.text((ML + j * (tw + G) + tw / 2, MT / 2), GRUPOS[j], font=f, fill="black", anchor="mm")
for i, m in enumerate(MARC):
    t = Image.new("RGBA", (th, 40), (255, 255, 255, 0))
    ImageDraw.Draw(t).text((th / 2, 20), m, font=ImageFont.truetype(ARIALB, 32), fill="black", anchor="mm")
    t = t.rotate(90, expand=True)
    out.paste(t, (ML // 2 - 20, MT + i * (th + G)), t)
out.save(FIG + "Fig5_IHC_fotos_horizontal.png", dpi=(300, 300))
print(out.size)
