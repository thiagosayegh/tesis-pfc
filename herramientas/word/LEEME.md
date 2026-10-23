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
3b. Tesis completa en Word (desde el 23 oct. 2026; carátula, Resumen, glosario, índices como campos de Word, numeración romana y arábiga), compilando antes solo `main.tex`:
   ```
   DOC=tesis python herramientas/word/tex2docx.py "entregas/tesina AAAAMMDD.docx"
   python herramientas/word/retocar.py "entregas/tesina AAAAMMDD.docx"
   python herramientas/word/tipos_png.py "entregas/tesina AAAAMMDD.docx"
   python herramientas/word/resaltar.py "entregas/tesina AAAAMMDD.docx"
   python herramientas/word/tesis_word.py "entregas/tesina AAAAMMDD.docx"
   powershell -ExecutionPolicy Bypass -File herramientas/word/actualizar_word.ps1 "C:\ruta\completa\tesina AAAAMMDD.docx" "C:\ruta\control.pdf"
   ```
   `resaltar.py` pone en amarillo lo que en los `.tex` está dentro de `\resaltar{...}` (cambios de la última ronda; en el PDF no se ven). Sirve también para los otros documentos. Al empezar una ronda nueva, sacar las marcas viejas (`\resaltar{` → nada, con su llave de cierre).
4. **Antes de mandar, abrir cada `.docx` con Word y mirarlo** (Word está instalado: se puede exportar a PDF por COM desde PowerShell con `Word.Application` → `Documents.Open` → `SaveAs(..., 17)` y revisar las páginas).

`reference.docx` es la plantilla: A4, idioma es-AR, texto justificado, títulos negros, estilos `Centrado`, `Justificado` y `TituloPortada`.
