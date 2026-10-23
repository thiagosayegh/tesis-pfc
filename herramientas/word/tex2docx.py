"""Convierte las secciones 4 a 8 de la tesis (con DOC=intro, las 1, 2, 3, 7 y 8; con DOC=tesis, la tesis
completa, con caratula, glosario e indices) a un .docx editable con pandoc.
Usa los numeros de figuras, tablas, secciones y citas de la compilacion del documento para Sol
(build/metodos_resultados_discusion_sol.aux / .bbl) y la lista de referencias de su PDF."""
import os, re, shutil, subprocess, sys
import pymupdf

W = os.path.dirname(os.path.abspath(__file__)).replace(chr(92), "/") + "/"
R = os.path.dirname(os.path.dirname(W.rstrip("/"))).replace(chr(92), "/") + "/"
IMG = W + "img/"
os.makedirs(IMG, exist_ok=True)
# DOC=intro (variable de entorno): secciones 1, 2, 3, 7 y 8 (introduccion_conclusiones_sol.tex)
INTRO = os.environ.get("DOC") == "intro"
# DOC=tesis: tesis completa (main.tex); los indices y la paginacion los completa tesis_word.py
TESIS = os.environ.get("DOC") == "tesis"
BASE = R + "build/" + ("main" if TESIS else "introduccion_conclusiones_sol" if INTRO else "metodos_resultados_discusion_sol")
# \resaltar{...} (cambios de la ultima ronda) -> marcas que resaltar.py convierte en resaltado amarillo
HL_INI, HL_FIN = "⸢", "⸣"
SALIDA = sys.argv[1] if len(sys.argv) > 1 else R + "entregas/metodos resultados discusion 20261019.docx"
ANCHO = 16.0  # cm de texto en A4 con margenes de 2,5 cm

# ------------------------------------------------------------------ etiquetas y citas
labels = {}
for aux in (R + "build/main.aux", BASE + ".aux"):
    for k, v in re.findall(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}", open(aux, encoding="utf-8", errors="ignore").read()):
        labels[k] = v
orden = re.findall(r"\\entry\{([^}]+)\}", open(BASE + ".bbl", encoding="utf-8").read())
num_cita = {k: i + 1 for i, k in enumerate(orden)}

def grupo(s, i):
    """s[i] == '{' -> (contenido, indice despues de la llave de cierre)."""
    assert s[i] == "{", s[i:i + 30]
    d, j = 0, i
    while True:
        if s[j] == "\\":
            j += 2; continue
        if s[j] == "{": d += 1
        elif s[j] == "}":
            d -= 1
            if d == 0: return s[i + 1:j], j + 1
        j += 1

def opcional(s, i):
    """s[i] == '[' -> (contenido, fin)."""
    d, j = 0, i
    while True:
        if s[j] == "[": d += 1
        elif s[j] == "]":
            d -= 1
            if d == 0: return s[i + 1:j], j + 1
        j += 1

def reemplazar_cmd(s, cmd, f, nargs=1):
    """Reemplaza \\cmd{a}{b}... por f(a, b, ...) respetando llaves anidadas."""
    out, i = [], 0
    pat = "\\" + cmd
    while True:
        k = s.find(pat, i)
        if k < 0:
            out.append(s[i:]); break
        fin = k + len(pat)
        if fin < len(s) and (s[fin].isalpha()):
            out.append(s[i:fin]); i = fin; continue
        out.append(s[i:k])
        j = fin
        while j < len(s) and s[j] == " ": j += 1
        args = []
        for _ in range(nargs):
            a, j = grupo(s, j); args.append(a)
        out.append(f(*args)); i = j
    return "".join(out)

def comprimir(nums):
    nums = sorted(set(nums)); res, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1: j += 1
        if j - i >= 2: res.append(f"{nums[i]}–{nums[j]}")
        else: res.extend(str(n) for n in nums[i:j + 1])
        i = j + 1
    return ", ".join(res)

UNIDADES = {r"\celsius": "°C", r"\micro\metre": "µm", r"\micro\gram": "µg", r"\milli\litre": "mL"}

def matematica(m):
    """Convierte una expresion en linea simple a texto con sub/superindices; si no puede, la deja."""
    s = m
    s = reemplazar_cmd(s, "text", lambda a: a)
    s = reemplazar_cmd(s, "mathrm", lambda a: a)
    s = reemplazar_cmd(s, "textit", lambda a: a)
    for a, b in ((r"{,}", ","), (r"\times", "×"), (r"\pm", "±"), (r"\leq", "≤"), (r"\geq", "≥"), (r"\cdot", "·"),
                 (r"\eta", "η"), (r"\alpha", "α"), (r"\lambda", "λ"), (r"\Delta", "Δ"), (r"\ldots", "…"), (r"\,", " "),
                 (r"\%", "%"), ("~", " ")):
        s = s.replace(a, b)
    s = re.sub(r"_\{([^{}]*)\}", r"\\textsubscript{\1}", s)
    s = re.sub(r"_([A-Za-z0-9])", r"\\textsubscript{\1}", s)
    s = re.sub(r"\^\{([^{}]*)\}", r"\\textsuperscript{\1}", s)
    s = re.sub(r"\^([A-Za-z0-9*+])", r"\\textsuperscript{\1}", s)
    resto = re.sub(r"\\text(sub|super)script\{[^{}]*\}", "", s)
    if re.search(r"\\[A-Za-z]", resto) or "{" in resto or "}" in resto:
        return "$" + m + "$"
    s = re.sub(r"(?<![\w\\{])([Fptn])(?!\w)", r"\\textit{\1}", s)
    s = re.sub(r"(?<=\s)-(?=\s)", "−", s)
    return s

def en_linea(s):
    s = re.sub(r"(?<!\\)%.*", "", s)
    s = reemplazar_cmd(s, "resaltar", lambda a: HL_INI + a + HL_FIN)
    s = s.replace(r"\stevia{}", r"\textit{Stevia rebaudiana} Bertoni").replace(r"\stevia", r"\textit{Stevia rebaudiana} Bertoni")
    s = s.replace(r"\anymaze{}", "AnyMaze©").replace(r"\anymaze", "AnyMaze©")
    s = s.replace(r"\Srebaudiana", r"\textit{S. rebaudiana}")
    for c, t in (("pendiente", "PENDIENTE"), ("confirmar", "CONFIRMAR"), ("revisar", "REVISAR")):
        s = reemplazar_cmd(s, c, lambda a, t=t: r"\textbf{[" + t + ": " + a + "]}")
    s = reemplazar_cmd(s, "SI", lambda a, u: a + " " + UNIDADES.get(u.strip(), u), 2)
    s = reemplazar_cmd(s, "si", lambda u: UNIDADES.get(u.strip(), u))
    s = reemplazar_cmd(s, "enquote", lambda a: "“" + a + "”")
    def ref(a):
        if a not in labels: raise KeyError("etiqueta sin numero: " + a)
        return labels[a]
    s = re.sub(r"\\S~?\\ref\{([^}]+)\}", lambda m: "§" + ref(m.group(1)), s)
    s = reemplazar_cmd(s, "ref", ref)
    s = re.sub(r"\\cite\{([^}]+)\}", lambda m: "[" + comprimir([num_cita[k.strip()] for k in m.group(1).split(",")]) + "]", s)
    # matematica en linea (no toca equation ni $$)
    s = re.sub(r"(?<![\\$])\$([^$]+?)\$", lambda m: matematica(m.group(1)), s)
    return s

# ------------------------------------------------------------------ figuras y tablas
def marca_tc(tipo, num, titulo):
    """Solo en la tesis completa: el pie corto en texto plano entre marcas, que tesis_word.py convierte en
    un campo TC de Word (asi los indices de figuras y de tablas se arman y se actualizan en Word)."""
    if not TESIS: return ""
    t = re.sub(r"\\text(it|bf|subscript|superscript)\{([^{}]*)\}", r"\2", titulo)
    t = re.sub(r"\\[A-Za-z]+\*?", "", t).replace("{", "").replace("}", "").replace('"', "'").strip().rstrip(".")
    return " ⟦TC|" + tipo + "|" + num + ". " + t + "⟧"

def imagen(arch):
    destino = IMG + os.path.splitext(os.path.basename(arch))[0] + ".png"
    src = R + "figuras/" + arch
    # se rehace la copia si la figura cambio despues de la ultima conversion
    if not os.path.exists(destino) or os.path.getmtime(src) > os.path.getmtime(destino):
        if arch.lower().endswith(".pdf"):
            pymupdf.open(src)[0].get_pixmap(dpi=300 if arch.startswith("compuestas/") else 200).save(destino)
        else:
            pymupdf.Pixmap(src).save(destino) if arch.lower().endswith((".jpg", ".jpeg")) else shutil.copy(src, destino)
    return "img/" + os.path.basename(destino)

def ancho(opts, factor=1.0):
    m = re.search(r"width=([\d.]*)\\(line|text)width", opts or "")
    f = float(m.group(1) or 1) if m else 1.0
    return round(ANCHO * f * factor, 2)

def figura(cuerpo):
    lab = re.search(r"\\label\{([^}]+)\}", cuerpo).group(1)
    # pie: \caption[corto]{largo} que no este dentro de un subfigure
    sin_sub = re.sub(r"\\begin\{subfigure\}.*?\\end\{subfigure\}", "", cuerpo, flags=re.S)
    k = sin_sub.rfind(r"\caption")
    j = k + len(r"\caption")
    corto = None
    if sin_sub[j] == "[": corto, j = opcional(sin_sub, j)
    pie, _ = grupo(sin_sub, j)
    filas, letra, leyendas = [], 0, []
    if r"\begin{tikzpicture}" in cuerpo:
        # dibujo TikZ: se recorta del PDF compilado, entre el texto anterior y el pie
        num = labels[lab]
        pdf = pymupdf.open(BASE + ".pdf")
        for pg in pdf:
            hits = pg.search_for("Figura " + num + ".")
            if not hits: continue
            y_pie = hits[0].y0
            dib = [d["rect"] for d in pg.get_drawings() if d["rect"].y1 <= y_pie + 1]
            txt = [b for b in pg.get_text("blocks") if b[3] <= y_pie and b[1] >= min(r.y0 for r in dib) - 40]
            caja = pymupdf.Rect(dib[0])
            for r in dib[1:]: caja |= r
            for b in txt: caja |= pymupdf.Rect(b[:4])
            caja = pymupdf.Rect(caja.x0 - 6, caja.y0 - 6, caja.x1 + 6, caja.y1 + 6)
            destino = IMG + "tikz_" + lab.replace(":", "_") + ".png"
            pg.get_pixmap(dpi=220, clip=caja).save(destino)
            filas.append(r"\includegraphics[width=%scm]{%s}" % (round(min(ANCHO, caja.width / 72 * 2.54), 2), "img/" + os.path.basename(destino)))
            break
    for bloque in ([] if filas else re.split(r"\n\s*\n", cuerpo)):
        items = []
        for m in re.finditer(r"\\begin\{subfigure\}(?:\[[^\]]*\])?\{([\d.]*)\\linewidth\}(.*?)\\end\{subfigure\}|\\incluirfigura(\[[^\]]*\])?\{([^}]+)\}", bloque, re.S):
            if m.group(2) is not None:
                f = float(m.group(1) or 1)
                mm = re.search(r"\\incluirfigura(\[[^\]]*\])?\{([^}]+)\}", m.group(2))
                # 0,88: deja lugar para las letras (A), (B)... y que los paneles de una fila entren en un renglon
                items.append("(" + "ABCDEFGH"[letra] + ") " + r"\includegraphics[width=%scm]{%s}" % (ancho(mm.group(1), f * 0.88), imagen(mm.group(2))))
                letra += 1
            else:
                if "leyenda" in m.group(4).lower():
                    leyendas.append(r"\includegraphics[width=%scm]{%s}" % (min(ancho(m.group(3)), 3.5), imagen(m.group(4))))
                else:
                    items.append(r"\includegraphics[width=%scm]{%s}" % (ancho(m.group(3)), imagen(m.group(4))))
        if items: filas.append("  ".join(items))
    filas += leyendas
    return "\n\n".join(filas) + "\n\n" + r"\textbf{Figura " + labels[lab] + ".} " + pie.strip() + marca_tc("F", labels[lab], corto or pie) + "\n\n"

def celdas(fila):
    partes = re.split(r"(?<!\\)&", fila)
    out = []
    for p in partes:
        p = p.strip()
        m = re.match(r"\\multicolumn\{(\d+)\}\{[^}]*\}\{(.*)\}$", p, re.S)
        if m: out += [m.group(2).strip()] * int(m.group(1))
        else: out.append(p)
    return out

def tabla(cuerpo):
    lab = re.search(r"\\label\{([^}]+)\}", cuerpo).group(1)
    k = cuerpo.find(r"\caption"); j = k + len(r"\caption")
    corto = None
    if cuerpo[j] == "[": corto, j = opcional(cuerpo, j)
    pie, _ = grupo(cuerpo, j)
    m = re.search(r"\\begin\{(tabularx|tabular\*?)\}(.*?)\\end\{\1\}", cuerpo, re.S)
    interior = m.group(2)
    interior = re.sub(r"^\s*(\{\\linewidth\})?\{[^\n]*\}\n", "", interior, count=1)  # especificacion de columnas
    interior = re.sub(r"\\(toprule|midrule|bottomrule)|\\cmidrule(\([^)]*\))?\{[^}]*\}", "", interior)
    filas = [f.strip() for f in interior.split(r"\\") if f.strip()]
    filas = [celdas(f) for f in filas]
    grupo_fila = None
    if any(r"\multicolumn" in c for c in re.split(r"(?<!\\)&", interior.split(r"\\")[0])) or (filas and filas[0][0] == "" and len(filas) > 1 and filas[1][0] != ""):
        grupo_fila = filas.pop(0)
    enc = filas.pop(0)
    if grupo_fila:
        enc = [(re.sub(r"\\textbf\{(.*)\}", r"\1", g) + ": " + e) if g.strip() else e for g, e in zip(grupo_fila, enc)]
        enc = [r"\textbf{" + re.sub(r"\\textbf\{([^}]*)\}", r"\1", e) + "}" for e in enc]
    n = len(enc)
    nb = lambda c: re.sub(r"\((\d+), (\d+)\)", "(\\1, \\2)", c)
    filas = [[nb(c) for c in f] for f in filas]
    cuerpo_tab =[r"\begin{tabular}{" + "l" * n + "}", r"\toprule", " & ".join(enc) + r" \\", r"\midrule"]
    cuerpo_tab += [" & ".join(f + [""] * (n - len(f))) + r" \\" for f in filas]
    cuerpo_tab += [r"\bottomrule", r"\end{tabular}"]
    nota = ""
    mn = re.search(r"\\begin\{minipage\}\{[^}]*\}(.*?)\\end\{minipage\}", cuerpo, re.S)
    if mn: nota = "\n\n" + re.sub(r"\\footnotesize", "", mn.group(1)).strip()
    return r"\textbf{Tabla " + labels[lab] + ".} " + pie.strip() + marca_tc("T", labels[lab], corto or pie) + "\n\n" + "\n".join(cuerpo_tab) + nota + "\n\n"

def flotantes(s):
    s = re.sub(r"\\begin\{figure\}(\[[^\]]*\])?(.*?)\\end\{figure\}", lambda m: figura(m.group(2)), s, flags=re.S)
    s = re.sub(r"\\begin\{table\}(\[[^\]]*\])?(.*?)\\end\{table\}", lambda m: tabla(m.group(2)), s, flags=re.S)
    return s

# ------------------------------------------------------------------ titulos numerados
def titulos(s, cap):
    cnt = [cap, 0, 0]
    out = []
    for linea in s.split("\n"):
        m = re.match(r"\s*\\(chapter|section|subsection)(\*?)\{", linea)
        if m:
            nivel = {"chapter": 0, "section": 1, "subsection": 2}[m.group(1)]
            tit, fin = grupo(linea, m.end() - 1)
            if not m.group(2):
                if nivel == 1: cnt[1] += 1; cnt[2] = 0
                if nivel == 2: cnt[2] += 1
                numero = ".".join(str(c) for c in cnt[:nivel + 1])
                tit = numero + ". " + tit if nivel == 0 else numero + " " + tit
            linea = "\\" + m.group(1) + "*{" + tit + "}" + linea[fin:]
        out.append(linea)
    return "\n".join(out)

LIMPIAR = [r"\\FloatBarrier", r"\\clearpage", r"\\centering", r"\\vspace\*?\{[^}]*\}", r"\\hfill", r"\\noindent",
           r"\\small", r"\\footnotesize", r"\\setlength\{[^}]*\}\{[^}]*\}", r"\\label\{[^}]*\}", r"\\medskip", r"\\raggedright"]

def capitulo(arch, cap):
    s = open(R + arch, encoding="utf-8").read()
    s = en_linea(s)
    s = flotantes(s)
    s = titulos(s, cap)
    for p in LIMPIAR: s = re.sub(p, "", s)
    return s

# Resumen (desde el 20 oct. 2026 Sol pidio el titulo y el Resumen al principio; el Anexo A se saco)
res = capitulo("capitulos/01_resumen.tex", 0)
res = re.sub(r"\\addcontentsline\{[^}]*\}\{[^}]*\}\{[^}]*\}", "", res)
if TESIS:
    glo = capitulo("capitulos/02_glosario.tex", 0)
    glo = re.sub(r"\\addcontentsline\{[^}]*\}\{[^}]*\}\{[^}]*\}", "", glo)
    glo = re.sub(r"\\begin\{description\}\[[^\]]*\]", r"\\begin{description}", glo)
    caratula = "".join(r"\begin{center}" + x + r"\end{center}" + "\n\n" for x in (
        r"\textbf{Efectos neurobiológicos a largo plazo de la exposición a \textit{Stevia rebaudiana} durante la etapa juvenil y la adultez}",
        r"\includegraphics[width=8cm]{logo_itba.png}",
        r"\textit{Proyecto final de Carrera para la obtención del título de Bioingeniero}",
        "Autor: Sayegh, Thiago (62260)", "Tutora: Dra. María Sol Kruse", r"Fecha de entrega: \textbf{[CONFIRMAR: fecha]}"))
    # marcas que tesis_word.py reemplaza por los campos de indice
    indices = "Índice\n\nIDXGENERAL\n\nÍndice de figuras\n\nIDXFIGURAS\n\nÍndice de tablas\n\nIDXTABLAS\n\n"
    partes = [caratula + res, glo, indices] + [capitulo("capitulos/%s.tex" % a, n) for n, a in enumerate(
        ("1_introduccion", "2_estado_del_arte", "3_marco_teorico", "4_materiales_y_metodos", "5_resultados",
         "6_discusion", "7_perspectivas_futuras", "8_conclusiones"), start=1)]
elif INTRO:
    partes = [capitulo("capitulos/1_introduccion.tex", 1), capitulo("capitulos/2_estado_del_arte.tex", 2),
              capitulo("capitulos/3_marco_teorico.tex", 3), capitulo("capitulos/7_perspectivas_futuras.tex", 7),
              capitulo("capitulos/8_conclusiones.tex", 8)]
else:
    partes = [res, capitulo("capitulos/4_materiales_y_metodos.tex", 4), capitulo("capitulos/5_resultados.tex", 5),
              capitulo("capitulos/6_discusion.tex", 6), capitulo("capitulos/7_perspectivas_futuras.tex", 7),
              capitulo("capitulos/8_conclusiones.tex", 8)]

# ------------------------------------------------------------------ referencias (del PDF compilado)
doc = pymupdf.open(BASE + ".pdf")
texto = ""
# desde la pagina que empieza con el titulo "Referencias bibliográficas" (en la tesis completa
# el titulo tambien aparece en el indice)
inicio = max(i for i, pg in enumerate(doc) if "Referencias bibliográficas" in [l.strip() for l in pg.get_text().split("\n")[:3]])
for pg in list(doc)[inicio:]:
    t = pg.get_text()
    texto += t[t.find("Referencias bibliográficas") + len("Referencias bibliográficas"):] if not texto else t
lineas = [l.strip() for l in texto.split("\n") if l.strip() and not re.fullmatch(r"\d+", l.strip())]
refs, actual = [], None
for l in lineas:
    if re.match(r"^\[\d+\]", l):
        if actual: refs.append(actual)
        actual = l
    elif actual is not None:
        if actual.endswith("-") and l[:1].islower(): actual = actual[:-1] + l
        elif actual.endswith(("/", ".", "_")) and "doi" in actual[-40:].lower() or actual.endswith("/"): actual += l
        else: actual += " " + l
if actual: refs.append(actual)
esc = lambda t: (t.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")
                  .replace("#", r"\#").replace("$", r"\$").replace("{", r"\{").replace("}", r"\}"))
bib = "\\chapter*{Referencias bibliográficas}\n\n" + "\n\n".join(esc(r) for r in refs) + "\n"

cabecera = (r"\begin{center}\textbf{Efectos neurobiológicos a largo plazo de la exposición a \textit{Stevia rebaudiana} durante la etapa juvenil y la adultez}\end{center}" + "\n\n"
            r"\begin{center}Resumen, Materiales y métodos, Resultados, Discusión, Perspectivas futuras y Conclusiones\end{center}" + "\n\n"
            r"\begin{center}Thiago Sayegh --- IByME-CONICET. Versión para revisión de la Dra. M. S. Kruse, 22 de octubre de 2026\end{center}" + "\n\n"
            r"\textbf{Cómo leer este documento.} Son el Resumen y las secciones 4 a 8 de la tesis, seguidos de su propia lista de referencias (solo las que se citan en estas secciones, numeradas por orden de aparición, por lo que los números difieren de los de la tesis completa). Las referencias a otras secciones conservan la numeración de la tesis." + "\n\n")
if INTRO:
    cabecera = (cabecera.replace("Resumen, Materiales y métodos, Resultados, Discusión, Perspectivas futuras y Conclusiones",
                                 "Introducción, Estado del arte, Marco teórico, Perspectivas futuras y Conclusiones")
                .replace("Son el Resumen y las secciones 4 a 8 de la tesis", "Son las secciones 1, 2, 3, 7 y 8 de la tesis"))
if TESIS: cabecera = ""
fuente = "\\documentclass{report}\n\\usepackage{booktabs}\n\\usepackage{graphicx}\n\\begin{document}\n" + cabecera + "\n\n".join(partes) + "\n\n" + bib + "\\end{document}\n"
open(W + "msr.tex", "w", encoding="utf-8").write(fuente)
print("referencias:", len(refs), "| citas:", len(num_cita), "| imagenes:", len(os.listdir(IMG)))
r = subprocess.run(["pandoc", "-f", "latex", "-t", "docx", "--reference-doc=" + W + "reference.docx",
                    "--resource-path=" + W, "-o", SALIDA, W + "msr.tex"], capture_output=True, text=True, cwd=W)
print("pandoc:", r.returncode, r.stderr[:2000])
