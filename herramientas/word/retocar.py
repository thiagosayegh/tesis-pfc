"""Retoque del .docx que genera pandoc para que se vea como la tesis:
tablas a todo el ancho con anchos de columna definidos, encabezado agrupado y bordes tipo booktabs,
figuras centradas y pegadas a su pie, titulos en negro, referencias sin justificar y encabezado centrado."""
import copy, re, sys
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ruta = sys.argv[1]
doc = Document(ruta)
TOTAL = 9070  # ancho del texto en dxa (16 cm)

# ---------------------------------------------------------------- estilos
for st in doc.styles:
    try:
        nombre = st.name or ""
    except Exception:
        continue
    if nombre.startswith("Heading") or nombre == "Title":
        st.font.color.rgb = RGBColor(0, 0, 0)
        rpr = st.element.rPr
        if rpr is not None:
            for c in rpr.findall(qn("w:color")):
                for a in ("w:themeColor", "w:themeShade", "w:themeTint"):
                    c.attrib.pop(qn(a), None)
for nombre in ("Body Text", "First Paragraph"):
    try:
        st = doc.styles[nombre]
        st.font.size = Pt(11)
        st.paragraph_format.space_after = Pt(6)
        st.paragraph_format.line_spacing = 1.15
    except KeyError:
        pass

def borde(padre, lado, sz="8"):
    b = OxmlElement("w:" + lado)
    b.set(qn("w:val"), "single"); b.set(qn("w:sz"), sz); b.set(qn("w:space"), "0"); b.set(qn("w:color"), "000000")
    padre.append(b)

def tcpr(tc):
    p = tc.find(qn("w:tcPr"))
    if p is None:
        p = OxmlElement("w:tcPr"); tc.insert(0, p)
    return p

def ancho_celda(tc, dxa):
    p = tcpr(tc)
    for w in p.findall(qn("w:tcW")): p.remove(w)
    w = OxmlElement("w:tcW"); w.set(qn("w:w"), str(dxa)); w.set(qn("w:type"), "dxa")
    p.insert(0, w)

def borde_inferior(tc, sz):
    p = tcpr(tc)
    for b in p.findall(qn("w:tcBorders")): p.remove(b)
    tb = OxmlElement("w:tcBorders"); borde(tb, "bottom", sz); p.append(tb)

def quitar_prefijo(tc, n):
    """Borra los primeros n caracteres del texto de la celda, respetando los runs (sub/superindices)."""
    for t in tc.iter(qn("w:t")):
        if n <= 0: break
        s = t.text or ""
        if len(s) <= n:
            n -= len(s); t.text = ""
        else:
            t.text = s[n:]; n = 0

def texto(tc):
    return "".join(t.text or "" for t in tc.iter(qn("w:t")))

# ---------------------------------------------------------------- tablas
for tabla in doc.tables:
    tbl = tabla._tbl
    trs = tbl.findall(qn("w:tr"))
    ncol = len(trs[0].findall(qn("w:tc")))
    tam = 8 if ncol >= 7 else 10
    # anchos: primera columna mas ancha
    if ncol >= 9:   primera = 1750
    elif ncol >= 7: primera = 2000
    elif ncol == 2: primera = 4300
    else:           primera = TOTAL // ncol
    resto = (TOTAL - primera) // (ncol - 1) if ncol > 1 else TOTAL
    anchos = [primera] + [resto] * (ncol - 1)
    grid = tbl.find(qn("w:tblGrid"))
    for g in list(grid): grid.remove(g)
    for a in anchos:
        gc = OxmlElement("w:gridCol"); gc.set(qn("w:w"), str(a)); grid.append(gc)
    tblPr = tbl.tblPr
    for tag in ("w:tblW", "w:tblLayout", "w:tblBorders", "w:jc"):
        for e in tblPr.findall(qn(tag)): tblPr.remove(e)
    w = OxmlElement("w:tblW"); w.set(qn("w:w"), str(TOTAL)); w.set(qn("w:type"), "dxa"); tblPr.append(w)
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    bordes = OxmlElement("w:tblBorders"); borde(bordes, "top", "12"); borde(bordes, "bottom", "12"); tblPr.append(bordes)
    for e in tblPr.findall(qn("w:tblCellMar")): tblPr.remove(e)
    mar = OxmlElement("w:tblCellMar")
    for lado in ("left", "right"):
        m = OxmlElement("w:" + lado); m.set(qn("w:w"), "40"); m.set(qn("w:type"), "dxa"); mar.append(m)
    tblPr.append(mar)
    for tr in trs:
        for k, tc in enumerate(tr.findall(qn("w:tc"))):
            ancho_celda(tc, anchos[k] if k < ncol else resto)
    # encabezado agrupado "Grupo: sub"
    enc = trs[0]
    tcs = enc.findall(qn("w:tc"))
    textos = [texto(tc).strip() for tc in tcs]
    grupos = [x.split(": ", 1)[0] if ": " in x else "" for x in textos]
    filas_enc = 1
    if any(grupos):
        nueva = copy.deepcopy(enc)
        enc.addprevious(nueva)
        # subencabezado: sacar "Grupo: "
        for tc, x in zip(tcs, textos):
            if ": " in x: quitar_prefijo(tc, len(x.split(": ", 1)[0]) + 2)
        # fila de grupos: texto = grupo y celdas combinadas
        gtcs = nueva.findall(qn("w:tc"))
        for tc, g, x in zip(gtcs, grupos, textos):
            ts = list(tc.iter(qn("w:t")))
            for t in ts: t.text = ""
            if ts: ts[0].text = g
        i = 0
        while i < ncol:
            j = i
            while j + 1 < ncol and grupos[i] and grupos[j + 1] == grupos[i]:
                j += 1
            if j > i:
                span = OxmlElement("w:gridSpan"); span.set(qn("w:val"), str(j - i + 1))
                ancho_celda(gtcs[i], sum(anchos[i:j + 1]))
                tcpr(gtcs[i]).append(span)
                for k in range(i + 1, j + 1): nueva.remove(gtcs[k])
            if grupos[i]: borde_inferior(gtcs[i], "4")
            i = j + 1
        filas_enc = 2
    trs = tbl.findall(qn("w:tr"))
    cuerpo_txt = [texto(tc) for tr in trs[filas_enc:] for tc in tr.findall(qn("w:tc"))[1:]]
    texto_largo = bool(cuerpo_txt) and sum(len(x) for x in cuerpo_txt) / len(cuerpo_txt) > 25
    for ri, tr in enumerate(trs):
        for ci, tc in enumerate(tr.findall(qn("w:tc"))):
            for p in tc.findall(qn("w:p")):
                ppr = p.find(qn("w:pPr"))
                if ppr is None:
                    ppr = OxmlElement("w:pPr"); p.insert(0, ppr)
                for e in ppr.findall(qn("w:jc")) + ppr.findall(qn("w:spacing")): ppr.remove(e)
                sp = OxmlElement("w:spacing"); sp.set(qn("w:before"), "20"); sp.set(qn("w:after"), "20"); ppr.append(sp)
                izq = texto_largo or (ci == 0 and ri >= filas_enc - 1 and len(tr.findall(qn("w:tc"))) == ncol)
                jc = OxmlElement("w:jc"); jc.set(qn("w:val"), "left" if izq else "center"); ppr.append(jc)
                for r in p.findall(qn("w:r")):
                    rpr = r.find(qn("w:rPr"))
                    if rpr is None:
                        rpr = OxmlElement("w:rPr"); r.insert(0, rpr)
                    for e in rpr.findall(qn("w:sz")): rpr.remove(e)
                    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(tam * 2)); rpr.append(sz)
                    if ri < filas_enc and rpr.find(qn("w:b")) is None:
                        rpr.insert(0, OxmlElement("w:b"))
    for tc in trs[filas_enc - 1].findall(qn("w:tc")):
        borde_inferior(tc, "8")
    # la tabla no se corta entre paginas: filas indivisibles y cada fila pegada a la siguiente
    for k, tr in enumerate(trs):
        trPr = tr.find(qn("w:trPr"))
        if trPr is None:
            trPr = OxmlElement("w:trPr"); tr.insert(0, trPr)
        if trPr.find(qn("w:cantSplit")) is None:
            trPr.append(OxmlElement("w:cantSplit"))
        if k < len(trs) - 1:
            for p in tr.iter(qn("w:p")):
                ppr = p.find(qn("w:pPr"))
                if ppr.find(qn("w:keepNext")) is None:
                    ppr.insert(1 if ppr.find(qn("w:pStyle")) is not None else 0, OxmlElement("w:keepNext"))

# ---------------------------------------------------------------- parrafos
ps = doc.paragraphs
en_refs = False
for p in ps:
    t = p.text.strip()
    if p._p.xpath(".//w:drawing"):
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.keep_with_next = True
    if re.match(r"^Figura \d+\.\d+\.", t):
        for r in p.runs: r.font.size = Pt(9.5)
        p.paragraph_format.space_after = Pt(12)
    if re.match(r"^Tabla [\dA-Z]+\.\d+\.", t):
        for r in p.runs: r.font.size = Pt(9.5)
        p.paragraph_format.keep_with_next = True
    if p.style.name.startswith("Heading") and "Referencias" in t:
        en_refs = True; continue
    if en_refs and t:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(4)
        for r in p.runs: r.font.size = Pt(9.5)
for k, p in enumerate(ps[:3]):
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if k == 0:
        for r in p.runs: r.bold = True; r.font.size = Pt(14)
for p in ps:
    if p.text.strip() in (".", "}") and not p._p.xpath(".//w:drawing"):
        p._p.getparent().remove(p._p)
doc.save(ruta)
print("tablas:", len(doc.tables))
