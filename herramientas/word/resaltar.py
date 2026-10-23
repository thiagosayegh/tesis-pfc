"""Convierte las marcas de \\resaltar{...} que deja tex2docx.py (caracteres U+2E22 y U+2E23) en resaltado
amarillo de Word (pedido de la Dra. Kruse, 23 oct. 2026: ver en el texto los ultimos cambios realizados).
El resaltado puede abarcar varios runs, formulas y parrafos. Uso: python resaltar.py archivo.docx"""
import copy, sys
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

INI, FIN = "⸢", "⸣"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
ruta = sys.argv[1]
doc = Document(ruta)

def resaltar(r):
    """Agrega <w:highlight w:val="yellow"/> al run (de texto o de formula)."""
    rpr = r.find(qn("w:rPr"))
    if rpr is None:
        rpr = OxmlElement("w:rPr")
        if r.tag == M + "r" and r.find(M + "rPr") is not None:
            r.find(M + "rPr").addnext(rpr)
        else:
            r.insert(0, rpr)
    if rpr.find(qn("w:highlight")) is None:
        h = OxmlElement("w:highlight"); h.set(qn("w:val"), "yellow")
        rpr.append(h)

activo, n = False, 0
runs = [r for r in doc.element.body.iter() if r.tag in (qn("w:r"), M + "r")]
for r in runs:
    ts = r.findall(qn("w:t")) if r.tag == qn("w:r") else r.findall(M + "t")
    texto = "".join(t.text or "" for t in ts)
    if INI not in texto and FIN not in texto:
        if activo and texto: resaltar(r); n += 1
        continue
    # partir el run en tramos dentro y fuera del resaltado
    tramos, actual = [], ""
    for c in texto:
        if c in (INI, FIN):
            if actual: tramos.append((actual, activo))
            actual, activo = "", (c == INI)
        else:
            actual += c
    if actual: tramos.append((actual, activo))
    for tx, hl in tramos:
        nuevo = copy.deepcopy(r)
        nts = nuevo.findall(qn("w:t")) if nuevo.tag == qn("w:r") else nuevo.findall(M + "t")
        for t in nts[1:]: t.getparent().remove(t)
        nts[0].text = tx
        nts[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        if hl: resaltar(nuevo); n += 1
        r.addprevious(nuevo)
    r.getparent().remove(r)
doc.save(ruta)
print("runs resaltados:", n)
