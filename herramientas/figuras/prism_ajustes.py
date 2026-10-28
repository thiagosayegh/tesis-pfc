"""Ajustes de la Dra. Kruse (28 oct. 2026) sobre dos figuras de Prism ya traducidas (*_es.pdf):
- Fig. 5.4 (período agua, % del control): línea azul en 100 = valor del grupo control, con su
  entrada "Control" en la leyenda -> figuras/Fig5_agua_periodo_agua_D1_D25_es_control.pdf
- Fig. 5.3 (consumo promedio): contorno negro de las barras más fino (2,16 pt -> 1,08 pt)
  -> figuras/Fig5_consumo_liquidos_promedio_es_fino.pdf
Los originales no se tocan. Uso:  python herramientas/figuras/prism_ajustes.py
"""
import os
import pymupdf
from PIL import Image

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")) + os.sep
FIG = R + "figuras" + os.sep
TIF = R + "entregas" + os.sep + "figuras TIF" + os.sep
AZUL = (0, 0, 1)                                 # azul del grupo control en los gráficos de Prism

def tif(doc, nombre):
    pix = doc[0].get_pixmap(dpi=300)
    Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(TIF + nombre + ".tif", compression="tiff_lzw", dpi=(300, 300))

# ---- Fig. 5.4: eje y 50 -> y = 157,3 pt; 100 -> 85,3 pt; área del gráfico x = 55,1 a 271,8 pt
doc = pymupdf.open(FIG + "Fig5_agua_periodo_agua_D1_D25_es.pdf")
p = doc[0]
p.draw_line((55.8, 85.33), (271.8, 85.33), color=AZUL, width=1.2)
# leyenda: quinta fila, con el mismo paso (19,2 pt) que las cuatro de Prism
p.draw_line((304.0, 99.72), (319.3, 99.72), color=AZUL, width=1.44)
p.insert_font(fontname="arial", fontfile="C:/Windows/Fonts/arial.ttf")
p.insert_text((328.0, 103.85), "Control (100\u00a0%)", fontname="arial", fontsize=12)
doc.save(FIG + "Fig5_agua_periodo_agua_D1_D25_es_control.pdf", garbage=3, deflate=True)
tif(doc, "Fig5_agua_periodo_agua")

# ---- Fig. 5.3: grosor del contorno de las barras (y de los cuadros de la leyenda)
doc = pymupdf.open(FIG + "Fig5_consumo_liquidos_promedio_es.pdf")
p = doc[0]
for x in p.get_contents():
    s = doc.xref_stream(x)
    doc.update_stream(x, s.replace(b"2.15997 w", b"1.07999 w"))
doc.save(FIG + "Fig5_consumo_liquidos_promedio_es_fino.pdf", garbage=3, deflate=True)
tif(doc, "Fig5_consumo_liquidos_promedio")
print("listo")
