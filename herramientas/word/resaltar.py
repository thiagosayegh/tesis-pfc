"""Convierte las marcas que deja tex2docx.py en resaltado de Word: \\resaltar{...} (U+2E22/U+2E23) en
amarillo y \\resaltarb{...} (U+2E24/U+2E25) en celeste (pedidos de la Dra. Kruse, 23 y 24 oct. 2026: ver
en el texto los ultimos cambios; el amarillo es la ronda anterior, que ella todavia relee).
El resaltado puede abarcar varios runs, formulas y parrafos, y anidarse (gana el de adentro).
Uso: python resaltar.py archivo.docx"""
import copy, sys
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ABRE = {"⸢": "yellow", "⸤": "cyan"}
CIERRA = {"⸣", "⸥"}
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
ruta = sys.argv[1]
doc = Document(ruta)

def resaltar(r, color):
    """Agrega <w:highlight w:val="color"/> al run (de texto o de formula)."""
    rpr = r.find(qn("w:rPr"))
    if rpr is None:
        rpr = OxmlElement("w:rPr")
        if r.tag == M + "r" and r.find(M + "rPr") is not None:
            r.find(M + "rPr").addnext(rpr)
        else:
            r.insert(0, rpr)
    for h in rpr.findall(qn("w:highlight")): rpr.remove(h)
    h = OxmlElement("w:highlight"); h.set(qn("w:val"), color)
    rpr.append(h)

pila, n = [], 0
runs = [r for r in doc.element.body.iter() if r.tag in (qn("w:r"), M + "r")]
for r in runs:
    ts = r.findall(qn("w:t")) if r.tag == qn("w:r") else r.findall(M + "t")
    texto = "".join(t.text or "" for t in ts)
    if not any(c in ABRE or c in CIERRA for c in texto):
        if pila and texto: resaltar(r, pila[-1]); n += 1
        continue
    # partir el run en tramos con su color (o sin resaltado)
    tramos, actual = [], ""
    for c in texto:
        if c in ABRE or c in CIERRA:
            if actual: tramos.append((actual, pila[-1] if pila else None))
            actual = ""
            if c in ABRE: pila.append(ABRE[c])
            elif pila: pila.pop()
        else:
            actual += c
    if actual: tramos.append((actual, pila[-1] if pila else None))
    for tx, color in tramos:
        nuevo = copy.deepcopy(r)
        nts = nuevo.findall(qn("w:t")) if nuevo.tag == qn("w:r") else nuevo.findall(M + "t")
        for t in nts[1:]: t.getparent().remove(t)
        nts[0].text = tx
        nts[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        if color: resaltar(nuevo, color); n += 1
        r.addprevious(nuevo)
    r.getparent().remove(r)
doc.save(ruta)
print("runs resaltados:", n)
