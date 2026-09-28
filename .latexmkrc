# Compilar con: latexmk        (limpiar: latexmk -c)
$pdf_mode = 1;          # pdflatex
$bibtex_use = 2;        # corre biber cuando hace falta
@default_files = ('main.tex');
$out_dir = 'build';
