"""Marca en el Word para Sol (entrega 20261021) las dudas del mail: resaltado amarillo + comentario de Word.
Uso: python herramientas/word/marcar_dudas_20261021.py "entregas/metodos resultados discusion 20261021.docx" (despues de tex2docx, retocar y tipos_png)."""
import copy, sys
from docx import Document
from docx.enum.text import WD_COLOR_INDEX

ruta = sys.argv[1]
doc = Document(ruta)

def partir(run, k):
    """Parte un run en la posicion k del texto; devuelve el run nuevo (segunda mitad)."""
    t = run.text
    nuevo = copy.deepcopy(run._r)
    run._r.addnext(nuevo)
    run.text = t[:k]
    from docx.text.run import Run
    r2 = Run(nuevo, run._parent)
    r2.text = t[k:]
    return r2

def aislar(par, sub):
    texto = "".join(r.text for r in par.runs)
    i = texto.find(sub)
    if i < 0:
        return None
    j = i + len(sub)
    # partir en j y luego en i
    for lim in (j, i):
        pos = 0
        for r in par.runs:
            n = len(r.text)
            if pos < lim < pos + n:
                partir(r, lim - pos)
                break
            pos += n
    sel, pos = [], 0
    for r in par.runs:
        n = len(r.text)
        if pos >= i and pos + n <= j and n:
            sel.append(r)
        pos += n
    return sel

MARCAS = [
    ("Asimismo, la ingesta de stevia superó la ingesta diaria admisible",
     "Asimismo, la ingesta de stevia superó",
     "(1,8 veces).",
     "Pregunta 1. Lo de los valores diarios lo pude calcular solo para la stevia (IDA de EFSA, 4 mg/kg/día en equivalentes de esteviol): juveniles unas 5 veces la IDA y adultos 1,8 veces. Para la sacarosa haría falta el consumo de alimento de los adultos, así que lo saqué. Lo dejamos solo para la stevia?"),
    ("no produce cambios en la conducta tipo ansiosa de ratas macho juveniles",
     "Estudios previos del laboratorio mostraron",
     "al finalizar la exposición",
     "Pregunta 2. Como presentación a congreso cité el resumen de la Reunión Conjunta SAIC-SAB 2023 (Coirini et al., Medicina 83, Supl. V, p. 148). Ahí dice stevia al 0,5 % y el manuscrito de Marchena dice 4 %. Es el mismo experimento? Si no, cuál cito?"),
    ("no produce cambios en la conducta tipo ansiosa de ratas macho juveniles",
     "[CONFIRMAR:", "]",
     "Pregunta 3. Cité el manuscrito como \"A. Marchena et al., manuscrito enviado para publicación\". Me pasás los coautores y la revista?"),
    ("memoria de localización de objetos (prueba NOL)",
     "no produce alteraciones en la memoria de localización", "dependiente del hipocampo",
     "Pregunta 4. En el estudio agudo la memoria se evaluó con NOL, así que cambié \"memoria de reconocimiento a corto plazo\" por \"memoria de localización de objetos\". Está bien?"),
]

hechas = 0
for clave, desde, hasta, comentario in MARCAS:
    par = next((p for p in doc.paragraphs if clave in "".join(r.text for r in p.runs)), None)
    if par is None:
        print("NO ENCONTRADO:", clave); continue
    texto = "".join(r.text for r in par.runs)
    i = texto.find(desde); j = texto.find(hasta, i) + len(hasta)
    sel = aislar(par, texto[i:j])
    if not sel:
        print("NO AISLADO:", desde); continue
    for r in sel:
        r.font.highlight_color = WD_COLOR_INDEX.YELLOW
    doc.add_comment(sel, text=comentario, author="Thiago Sayegh", initials="TS")
    hechas += 1
doc.save(ruta)
print("marcas:", hechas)
