"""Arma las figuras de varios paneles como una sola imagen (pedido de la Dra. Kruse, 21 oct. 2026:
"arma todas las figuras formato tif ... asi quedan mas prolijas"; "pone esto mas en el medio").

Cada figura se compone en una pagina de 16 cm de ancho (el ancho del texto de la tesis): los paneles
van alineados y centrados por fila, con su letra debajo, y la leyenda de colores centrada al pie.
Salidas:
  figuras/compuestas/<nombre>.pdf  -> vectorial, la usa la tesis (LaTeX) y el Word
  entregas/figuras TIF/<nombre>.tif -> 300 dpi, LZW, para quien las pida en TIF
Uso:  python herramientas/figuras/componer.py
"""
import os
import pymupdf
from PIL import Image

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")) + os.sep
FIG = R + "figuras" + os.sep
OUT = FIG + "compuestas" + os.sep
TIF = R + "entregas" + os.sep + "figuras TIF" + os.sep
os.makedirs(OUT, exist_ok=True); os.makedirs(TIF, exist_ok=True)

ANCHO = 16 / 2.54 * 72          # 16 cm en puntos
SEP = 8                          # separacion horizontal entre paneles (pt)
ALTO_LETRA = 14                  # renglon de la letra del panel (pt)
VSEP = 8                         # separacion vertical entre filas (pt)
ARIAL = "C:/Windows/Fonts/arial.ttf"
LEY = "Fig5_leyenda_grupos.png"

def recorte(arch):
    """"archivo.pdf|x" -> (archivo.pdf, rectangulo hasta x pt): deja afuera la leyenda propia de Prism,
    a la derecha, cuando la figura lleva una sola leyenda comun (Sol, 14 oct. 2026)."""
    if "|" not in arch:
        return arch, None
    arch, x = arch.split("|")
    r = pymupdf.open(FIG + arch)[0].rect
    return arch, pymupdf.Rect(0, 0, float(x), r.height)

def tam(arch):
    """(ancho, alto) en unidades arbitrarias, para la relacion de aspecto."""
    arch, clip = recorte(arch)
    if arch.lower().endswith(".pdf"):
        r = clip or pymupdf.open(FIG + arch)[0].rect
        return r.width, r.height
    with Image.open(FIG + arch) as im:
        return im.size

def poner(pag, arch, rect):
    arch, clip = recorte(arch)
    if arch.lower().endswith(".pdf"):
        src = pymupdf.open(FIG + arch)
        pag.show_pdf_page(rect, src, 0, clip=clip)
    else:
        pag.insert_image(rect, filename=FIG + arch)

def componer(nombre, filas, pie=None):
    """filas: lista de filas; cada fila es una lista de (archivo, fraccion_del_ancho, rotulo o None).
    pie: rotulo opcional centrado debajo de todo (p. ej. el (D) de la figura del NOR)."""
    plan, y = [], 0
    for fila in filas:
        anchos = [f * ANCHO for _, f, _ in fila]
        total = sum(anchos) + SEP * (len(fila) - 1)
        x = (ANCHO - total) / 2
        con_rotulo = any(r for _, _, r in fila)
        altos = []
        for (arch, f, rot), w in zip(fila, anchos):
            a, b = tam(arch)
            altos.append(w * b / a)
        h = max(altos)
        for (arch, f, rot), w, hh in zip(fila, anchos, altos):
            # alineados abajo dentro de la fila (como subfigure[b])
            plan.append((arch, pymupdf.Rect(x, y + h - hh, x + w, y + h), rot))
            x += w + SEP
        y += h + (ALTO_LETRA if con_rotulo else 0) + VSEP
    alto_total = y - VSEP + 4 + (ALTO_LETRA + 2 if pie else 0)
    doc = pymupdf.open()
    pag = doc.new_page(width=ANCHO, height=alto_total)
    pag.insert_font(fontname="arial", fontfile=ARIAL)
    for arch, rect, rot in plan:
        poner(pag, arch, rect)
        if rot:
            caja = pymupdf.Rect(rect.x0 - 20, rect.y1 + 2, rect.x1 + 20, rect.y1 + ALTO_LETRA + 2)
            pag.insert_textbox(caja, rot, fontname="arial", fontsize=9, align=pymupdf.TEXT_ALIGN_CENTER)
    if pie:
        pag.insert_textbox(pymupdf.Rect(0, alto_total - ALTO_LETRA - 4, ANCHO, alto_total), pie,
                           fontname="arial", fontsize=9, align=pymupdf.TEXT_ALIGN_CENTER)
    doc.save(OUT + nombre + ".pdf", garbage=3, deflate=True)
    pix = pag.get_pixmap(dpi=300)
    Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(TIF + nombre + ".tif", compression="tiff_lzw", dpi=(300, 300))
    print(f"{nombre}: {pix.width}x{pix.height} px")

L = lambda f: (LEY, f, None)   # leyenda de colores

FIGURAS = {
    # Metodos
    "Fig4_OF_esquema": [[("Fig4_OF_zonas_IA.png", 0.56, "(A)"), ("Fig4_OF_rearing_IA.png", 0.33, "(B)")]],
    "Fig4_NOR_fases": [[("Fig4_NOR_objetos_iguales_recortada.png", 0.38, "(A)"), ("Fig4_NOR_objetos_diferentes_recortada.png", 0.38, "(B)")]],
    # Resultados
    "Fig5_consumo_liquidos": [[("Fig5_consumo_liquidos_juvenil_es.pdf", 0.385, "(A) Juvenil"), ("Fig5_consumo_liquidos_adulto_es.pdf", 0.595, "(B) Adulto")]],
    "Fig5_OF_zonas": [
        [("Fig5_OF_distancia_total.pdf", 0.31, "(A)"), ("Fig5_OF_zonas_visitadas.pdf", 0.31, "(B)"), ("Fig5_OF_entradas_zona12.pdf", 0.31, "(C)")],
        [("Fig5_OF_distancia_zona12.pdf", 0.31, "(D)"), ("Fig5_OF_entradas_zona1.pdf", 0.31, "(E)"), ("Fig5_OF_distancia_zona1.pdf", 0.31, "(F)")],
        [L(0.2)]],
    "Fig5_OF_rearing_compuesta": [[("Fig5_OF_rearing_numero.pdf", 0.32, "(A)"), ("Fig5_OF_rearing_tiempo.pdf", 0.32, "(B)"), L(0.22)]],
    "Fig5_NOR_T1_compuesta": [[("Fig5_NOR_T1.pdf", 0.62, None)], [L(0.2)]],
    # 28 oct. 2026: sin el panel D (esquema y objetos), que ahora es la Fig. 4.3 de Metodos
    "Fig5_NOR_tasa": [
        [("Fig5_NOR_T2_es.pdf", 0.31, "(A) T2 (2 h)"), ("Fig5_NOR_T3_es.pdf", 0.31, "(B) T3 (24 h)"), ("Fig5_NOR_T4_es.pdf", 0.31, "(C) T4 (7 días)")],
        [L(0.2)]],
    "Fig5_SLR_dia1_compuesta": [[("Fig5_SLR_dia1_objetos.pdf", 0.95, "(A)")], [("Fig5_SLR_dia1_distancia.pdf", 0.8, "(B)")], [L(0.2)]],
    # 28 oct. 2026: una sola leyenda comun (se recortan las de Prism)
    "Fig5_SLR_DI": [[("Fig5_DI_SLR_d_es.pdf|228", 0.40, "(A) d-SLR"), ("Fig5_DI_SLR_s_es.pdf|228", 0.40, "(B) s-SLR"), L(0.16)]],
    "Fig5_SLR_tasa": [[("Fig5_tasa_SLR_d_es.pdf|224", 0.40, "(A) d-SLR"), ("Fig5_tasa_SLR_s_es.pdf|238", 0.40, "(B) s-SLR"), L(0.16)]],
    "Fig5_IHC_compuesta": [[("Fig5_IHC_pcna.pdf", 0.31, "(A)"), ("Fig5_IHC_dcx.pdf", 0.31, "(B)"), ("Fig5_IHC_pcna_dcx.pdf", 0.31, "(C)")], [("Fig5_IHC_leyenda.pdf", 0.22, None)]],
}

if __name__ == "__main__":
    for nombre, filas in FIGURAS.items():
        pie = None
        if filas[-1][0][0] == "blanco":          # ultima fila = solo un rotulo de texto, sin imagen
            pie = filas[-1][0][2]
            filas = filas[:-1]
        componer(nombre, filas, pie)
