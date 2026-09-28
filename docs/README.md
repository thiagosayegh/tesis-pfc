# docs/ — documentación de apoyo

Leer antes de redactar o modificar el texto de la tesis:

| Archivo | Cuándo leerlo |
|---|---|
| `guia_plantilla_ITBA.md` | Siempre que se escriba o revise un capítulo: qué exige la plantilla, límites de extensión |
| `estilo_y_redaccion.md` | Siempre: tono, reglas de fondo, cómo comunicarse con Thiago |
| `analisis_y_datos.md` | Al tocar Métodos, Resultados, Discusión o cualquier cosa con datos, estadística o limitaciones |
| `referencia/` | Consulta: documento del laboratorio (protocolos), plantilla original, guía IEEE |

## Carpetas de trabajo (vacías por ahora)
- `docs/referencia/papers/` — PDF de los artículos clave. Conviene tener acá: Reichelt 2016, Reichelt 2021 (protocolo SLR), Coirini 2022, Kruse 2019, Kruse 2025, Rey 2024. Sin los PDF, Claude Code solo conoce esos trabajos por título y resumen, y no debe atribuirles hallazgos específicos.
- `datos/` — planillas de AnyMaze y exportaciones de Prism (Excel/CSV), si se quiere que Claude Code las lea o regenere tablas. Si son pesadas o sensibles, agregar `datos/` al `.gitignore`.
- `analisis/` — scripts (por ejemplo `slr_pipeline.py` y, cuando exista, el de PCA / clustering / Random Forest para M1 y M2).
