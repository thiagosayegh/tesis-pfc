# Guía oficial de escritura del PFC (plantilla ITBA)

Fuente: "Template para escritura PFC" del ITBA (texto completo en `referencia/plantilla_ITBA/`). Esta es la pauta que evalúa el tribunal: cualquier redacción debe cumplirla.

## Estructura y qué pide cada parte

| Sección (archivo) | Lo que pide la plantilla | Límite |
|---|---|---|
| Carátula (`00_caratula.tex`) | Título, logo institucional (sin imágenes personales; se pueden agregar logos de afiliación), "Proyecto final de Carrera para la obtención del título de Bioingeniero", autor "Apellido, Nombre (Legajo)", tutor, co-tutor, asesor/es, fecha de entrega | — |
| Agradecimientos (`00_agradecimientos.tex`) | Opcional | media carilla |
| Resumen (`01_resumen.tex`) | Síntesis breve del problema, los objetivos, la metodología y los resultados principales, con palabras clave | media carilla |
| Glosario de abreviaturas | Lista de abreviaturas | — |
| Índices | General; de figuras y de tablas (de existir) | — |
| 1. Introducción | Presenta el tema, el planteamiento del problema, la justificación y los objetivos | máx. 3 carillas |
| 2. Estado del arte | Opcional; recomendado en trabajos que innovan. Agrupa qué investigaciones recientes se hicieron sobre el tema | — |
| 3. Marco teórico | Sustento formal (matemático, físico, fisiológico) que valida de manera estricta las decisiones de diseño e ingeniería. NO una recopilación temática ni un glosario: un hilo conductor que justifica por qué se aborda el problema con esa metodología y no otra. Evitar el efecto enciclopedia (evaluadores expertos); no redactar generalidades redundantes | hasta acá ≤ 20 % del escrito total |
| 4. Materiales y métodos | Qué se hizo, cómo y con qué: tipo de estudio, diseño, población, muestra, herramientas/instrumentos de recolección de datos | — |
| 5. Resultados | Compendio de los resultados del análisis de datos; usar recursos gráficos (diagramas, cuadros, tablas) para facilitar la comprensión | — |
| 6. Discusión | Analizar resultados relacionándolos con la teoría y el estado de la cuestión: comparar con estudios previos ya citados, contrastar con la hipótesis, analizar implicancias y limitaciones. Requiere pensamiento crítico | — |
| 7. Perspectivas futuras | Opcional. Ideas a futuro surgidas durante el trabajo y objetivos de máxima no alcanzados | máx. 1 carilla |
| 8. Conclusiones | Hallazgos más destacados; si se alcanzaron los objetivos y si la hipótesis fue comprobada o refutada; recomendaciones para futuros estudiantes. Redacción clara y concisa, conclusiones específicas por cada asunto fundamental | máx. 2 carillas |
| Anexos | Información útil para entender mejor ciertos apartados o grandes caudales de información: documentos de apoyo, tablas grandes, imágenes adicionales | — |
| Referencias bibliográficas | Listado completo de libros, revistas y sitios web citados. Normas IEEE | — |

Nota de la plantilla: **las tablas, imágenes y gráficos también deben referenciarse según IEEE**. Toda figura o tabla tomada o adaptada de una fuente lleva la cita en el epígrafe ("Adaptado de [n]"), como en la Figura 4.1.

## Consecuencias prácticas para redactar
- **Marco teórico:** cada subsección debe terminar justificando una decisión concreta de diseño o análisis del proyecto. Si un párrafo describe algo sin justificar una decisión, sobra.
- **Introducción:** cuidar el límite de 3 carillas (hoy cumple; no engordarla).
- **Discusión:** es el capítulo más exigente. Debe (1) contrastar con la hipótesis, (2) compararse con los estudios ya citados en el Estado del arte, (3) dar implicancias, (4) declarar limitaciones. Las limitaciones del diseño ya conocidas están en `analisis_y_datos.md`.
- **Conclusiones:** una conclusión específica por asunto (consumo/peso, OF, NOR, SLR, neurogénesis, ML) + estado de la hipótesis + estado de cada objetivo de mínima y de máxima.
- **Perspectivas futuras:** acá van los objetivos de máxima que no se alcancen.
- **Resumen:** en pasado, con resultados reales (hoy está en futuro, formato anteproyecto: reescribirlo cuando estén los resultados).
- Verificar el 20 % (hasta Marco teórico) y las carillas máximas al compilar: cada carilla ≈ una página del PDF con la configuración actual (A4, 12 pt, interlineado 1,5).
