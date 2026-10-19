# Generar las entregas en Word

Scripts que arman los `.docx` de `entregas/` a partir de las fuentes de la tesis (19 oct. 2026).

1. Compilar antes `main.tex` y `metodos_resultados_discusion_sol.tex` (el conversor toma de su `.aux`/`.bbl`/`.pdf` los números de figuras, tablas, secciones y citas, y la lista de referencias).
2. Métodos, Resultados y Discusión:
   ```
   python herramientas/word/tex2docx.py "entregas/metodos resultados discusion AAAAMMDD.docx"
   python herramientas/word/retocar.py "entregas/metodos resultados discusion AAAAMMDD.docx"
   python herramientas/word/tipos_png.py "entregas/metodos resultados discusion AAAAMMDD.docx"
   ```
3. Resumen para la cátedra (carátula + resumen) y documento del multivariado: editar `resumen.md` / `multivariado.md` y, desde esta carpeta,
   ```
   pandoc resumen.md -o ../../entregas/Resumen_catedra.docx --reference-doc=reference.docx
   pandoc multivariado.md -o "../../entregas/Análisis multivariado de la SLR qué hicimos y qué encontramos.docx" --reference-doc=reference.docx
   python retocar.py "../../entregas/Análisis multivariado de la SLR qué hicimos y qué encontramos.docx"
   ```
4. **Antes de mandar, abrir cada `.docx` con Word y mirarlo** (Word está instalado: se puede exportar a PDF por COM desde PowerShell con `Word.Application` → `Documents.Open` → `SaveAs(..., 17)` y revisar las páginas).

`reference.docx` es la plantilla: A4, idioma es-AR, texto justificado, títulos negros, estilos `Centrado`, `Justificado` y `TituloPortada`.
