"""Termina el Word de la tesis completa (DOC=tesis en tex2docx.py), despues de retocar.py:
cada seccion en pagina nueva, indice general y de figuras y de tablas como campos de Word, numeracion
romana en los preliminares y arabiga desde la Introduccion, con el numero de pagina al pie.
Los campos se actualizan despues abriendo el documento con Word (ver LEEME.md).
Uso: python tesis_word.py archivo.docx"""
import copy, re, sys
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

ruta = sys.argv[1]
doc = Document(ruta)
body = doc.element.body

def run_campo(p_el, instr, texto=""):
    """Agrega al parrafo un campo de Word (begin / instr / separate / texto / end), marcado para actualizar."""
    def r(hijo):
        rr = OxmlElement("w:r"); rr.append(hijo); p_el.append(rr); return hijo
    b = OxmlElement("w:fldChar"); b.set(qn("w:fldCharType"), "begin"); b.set(qn("w:dirty"), "true"); r(b)
    it = OxmlElement("w:instrText"); it.set("{http://www.w3.org/XML/1998/namespace}space", "preserve"); it.text = instr; r(it)
    s = OxmlElement("w:fldChar"); s.set(qn("w:fldCharType"), "separate"); r(s)
    if texto:
        t = OxmlElement("w:t"); t.text = texto; r(t)
    e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), "end"); r(e)

# ---------------------------------------------------------------- cada seccion en pagina nueva
# (doc.styles["Heading 1"] falla: pandoc escribe el nombre con mayuscula y python-docx busca "heading 1")
h1 = next(s for s in doc.styles if s.name == "Heading 1")
# Sol (27 oct. 2026): las secciones 1 a 8 van seguidas; solo los preliminares (Resumen,
# glosario, índices) y las Referencias empiezan en página nueva. La Introducción ya empieza
# en página nueva por el salto de sección de la numeración (más abajo).
h1.paragraph_format.page_break_before = False
h1.paragraph_format.space_before = Pt(24)
for p in doc.paragraphs:
    if p.style.name == "Heading 1" and p.text.strip() in ("Resumen", "Glosario de abreviaturas", "Referencias bibliográficas"):
        p.paragraph_format.page_break_before = True
try:
    st = doc.styles["Titulo de indice"]
except KeyError:
    st = doc.styles.add_style("Titulo de indice", WD_STYLE_TYPE.PARAGRAPH)
st.base_style = doc.styles["Normal"]
st.font.bold = True
st.font.size = h1.font.size or Pt(16)
st.paragraph_format.page_break_before = True
st.paragraph_format.space_after = Pt(12)
st.paragraph_format.keep_with_next = True

# ---------------------------------------------------------------- caratula: todo centrado y espaciado
for k, p in enumerate(doc.paragraphs):
    if p.style.name == "Heading 1": break
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(36 if k else 60)
    if k == 0:
        for r in p.runs: r.font.size = Pt(18)

# ---------------------------------------------------------------- listas (objetivos, Perspectivas): como el cuerpo
# (Sol, 26 oct. 2026: texto justificado y con el mismo tamaño de letra)
n_lista = 0
for p in doc.paragraphs:
    ppr = p._p.pPr
    if ppr is None or ppr.find(qn("w:numPr")) is None or not p.text.strip():
        continue
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    for r in p.runs:
        r.font.size = Pt(11)
    n_lista += 1

# ---------------------------------------------------------------- glosario: sigla y definicion en un renglon
from docx.shared import Cm
from docx.enum.text import WD_TAB_ALIGNMENT
ps = doc.paragraphs
for a, b in zip(ps, ps[1:]):
    if a.style.name == "Definition Term" and b.style.name == "Definition":
        for r in a.runs: r.bold = True
        tab = OxmlElement("w:r"); tab.append(OxmlElement("w:tab")); a._p.append(tab)
        for r in b._p.findall(qn("w:r")): a._p.append(r)
        a.style = b.style  # estilo de la definicion (sin negrita); la sigla queda en negrita por el run
        b._p.getparent().remove(b._p)
        f = a.paragraph_format
        f.left_indent, f.first_line_indent = Cm(2.4), Cm(-2.4)
        f.tab_stops.add_tab_stop(Cm(2.4), WD_TAB_ALIGNMENT.LEFT)
        f.space_before, f.space_after = Pt(0), Pt(3)

# ---------------------------------------------------------------- indices
CAMPOS = {"IDXGENERAL": ' TOC \\o "1-3" \\h \\z \\u ', "IDXFIGURAS": " TOC \\h \\z \\f F ", "IDXTABLAS": " TOC \\h \\z \\f T "}
for p in doc.paragraphs:
    t = p.text.strip()
    if t in ("Índice", "Índice de figuras", "Índice de tablas"):
        p.style = st
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    elif t in CAMPOS:
        for r in list(p._p.findall(qn("w:r"))): p._p.remove(r)
        run_campo(p._p, CAMPOS[t], "Clic derecho > Actualizar campo")

# ---------------------------------------------------------------- pies de figura y de tabla -> campo TC
n_tc = 0
for p in doc.paragraphs:
    texto = p.text
    m = re.search(r"\s*⟦TC\|([FT])\|(.*?)⟧\s*$", texto)
    if not m: continue
    borrar = len(texto) - m.start()
    for r in reversed(p.runs):
        if borrar <= 0: break
        s = r.text
        if len(s) <= borrar:
            borrar -= len(s); r._r.getparent().remove(r._r)
        else:
            r.text = s[:len(s) - borrar]; borrar = 0
    run_campo(p._p, ' TC "%s" \\f %s \\l 1 ' % (m.group(2).replace('"', "'"), m.group(1)))
    n_tc += 1

# ---------------------------------------------------------------- paginacion: romana hasta la Introduccion
intro = next(p for p in doc.paragraphs if p.style.name == "Heading 1" and p.text.strip().startswith("1. "))
sect_final = body.find(qn("w:sectPr"))
sect_pre = copy.deepcopy(sect_final)
for e in sect_pre.findall(qn("w:pgNumType")): sect_pre.remove(e)
pg = OxmlElement("w:pgNumType"); pg.set(qn("w:fmt"), "lowerRoman"); pg.set(qn("w:start"), "1")
sect_pre.append(pg)
sect_pre.append(OxmlElement("w:titlePg"))  # la caratula sin numero
salto = OxmlElement("w:p"); ppr = OxmlElement("w:pPr"); ppr.append(sect_pre); salto.append(ppr)
intro._p.addprevious(salto)
for e in sect_final.findall(qn("w:pgNumType")): sect_final.remove(e)
pg = OxmlElement("w:pgNumType"); pg.set(qn("w:fmt"), "decimal"); pg.set(qn("w:start"), "1")
sect_final.append(pg)

# numero de pagina centrado al pie (la seccion del cuerpo hereda el pie)
sec = doc.sections[0]
pie = sec.footer.paragraphs[0]
for r in list(pie._p.findall(qn("w:r"))): pie._p.remove(r)
pie.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_campo(pie._p, " PAGE ", "1")
for s in doc.sections[1:]:
    s.footer.is_linked_to_previous = True
doc.save(ruta)
print("campos TC:", n_tc, "| secciones:", len(doc.sections))
