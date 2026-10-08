# Guía de escritura del PFC (material de la cátedra ITBA 16.30)

Resumen de tres documentos de la cátedra, guardados en `docs/referencia/`. Usar al escribir o revisar capítulos. Si algo de acá contradice a `guia_plantilla_ITBA.md`, avisar.

Fuentes (PDF en `docs/referencia/`):
- `Template para escritura PFC.pdf` — plantilla: qué va en cada sección y límites.
- `Materiales y métodos (guia de escritura).pdf` — clase de Materiales y métodos (16.30, 2025).
- `Introduccion y Marco Teorico (guia de escritura).pdf` — clase de Introducción y Marco teórico (16.30, 1.er cuatrimestre 2026).

## 1. Template para escritura PFC (orden y límites)
| Sección | Qué pide | Límite |
|---|---|---|
| Agradecimientos | opcional | media carilla |
| **Resumen** | síntesis breve del problema, los objetivos, la metodología y los resultados principales, con palabras clave | **media carilla** |
| Glosario de abreviaturas, Índices (general, figuras, tablas) | — | — |
| Introducción | tema, planteamiento del problema, justificación y objetivos de la investigación | máx. 3 carillas |
| Estado del arte | opcional; agrupa qué investigaciones recientes se hicieron sobre el tema; recomendado si el trabajo innova en el área | — |
| Marco teórico | sustento formal (matemático, físico, fisiológico) que valida las decisiones de diseño e ingeniería; **no** es una recopilación temática ni un glosario; hilo conductor que justifica por qué se aborda el problema con una metodología y no otra. **Evitar el efecto enciclopedia** (se asumen evaluadores expertos); no redactar generalidades redundantes | hasta acá, **máx. 20 % del escrito total** |
| **Materiales y métodos** | qué se hizo, cómo y con qué: tipo de estudio, diseño, población, muestra y herramientas o instrumentos para recolectar los datos | — |
| Resultados | compendio de los resultados del análisis de datos; usar recursos gráficos (diagramas, cuadros, tablas) | — |
| Discusión | analiza los resultados y los relaciona con la teoría y el estado de la cuestión: comparación con estudios previos, contraste con la hipótesis, implicancias y limitaciones; pensamiento crítico | — |
| Perspectivas futuras | opcional; ideas surgidas y objetivos de máxima no alcanzados | máx. 1 carilla |
| Conclusiones | hallazgos más destacados; si se alcanzaron los objetivos y si la hipótesis fue comprobada o refutada; recomendaciones; conclusiones específicas por asunto fundamental; clara y concisa | máx. 2 carillas |
| Anexos | documentos de apoyo, tablas grandes, imágenes adicionales | — |
| Referencias | listado completo de lo citado, normas IEEE; tablas, imágenes y gráficos también se referencian según IEEE | — |

**Resumen: no hay un número de palabras para la tesina.** "Menos de 250 palabras" aparece solo en la pauta del anteproyecto (`pauta_anteproyecto_ITBA.txt`). Con el formato actual (A4, 12 pt, interlineado 1,5), media carilla ≈ 150–180 palabras; usar 250 como techo de seguridad.

## 2. Materiales y métodos (clase de la cátedra)
- **Para qué sirve:** es un "manual de instrucciones". Debe permitir que otra persona **reproduzca o continúe** el trabajo leyendo la tesis, y demostrar rigurosidad técnica.
- **Secciones sugeridas:**
  1. **Diseño del estudio / protocolo experimental:** descripción general del procedimiento y del flujo del experimento.
  2. **Sujetos (pacientes, animales, etc.):** características de la población (edad, sexo, etc.), **criterios de inclusión/exclusión**, **número de casos** (n total o n por grupo/condición) y **comité de ética**.
  3. **Materiales y equipos:** instrumentos, sensores, software, dispositivos, reactivos; **especificar marca, modelo y versión**.
  4. **Estadística:** métodos estadísticos, software usado, criterios de significancia; algoritmos o técnicas de procesamiento de señales, imágenes o simulaciones.
- **Uso de imágenes:** cada imagen debe servir para **reproducir el método o entender su lógica**, no para decorar. Tipos recomendados: esquemas del protocolo experimental (secuencia de pasos, ideales con múltiples condiciones), **fotos del montaje o de los dispositivos (mejor si son propias)**, capturas de pantalla del software o interfaces, diagramas de flujo.
- **Ejemplos de índice** que muestra la clase: "Diseño del estudio y origen de los datos", "Procesamiento y análisis de los datos", "Análisis estadístico", "Implementación".
- **Actividad de la clase** (útil como checklist): identificar tareas críticas o problemáticas, recursos (setup, maquinaria, costos), tareas que requieran validación, software y estadística necesarios.

## 3. Introducción y Marco teórico (clase de la cátedra)
- **Marco teórico:** es "la brújula del trabajo"; muestra el grado de avance sobre el problema, cuánto conoce el autor del tema y **la brecha** entre lo que se sabe y lo que se va a estudiar. Requiere citas (más no es mejor). Partes se recuperan en la Discusión (¿mis resultados son iguales, mejores o peores que los de otros autores?).
- **Introducción vs. Marco teórico:**
  - Introducción: presenta el problema (qué se estudia y por qué es relevante), los objetivos, la hipótesis (si la hay) y la estructura del trabajo; **breve y narrativa**, busca situar al lector.
  - Marco teórico: desarrolla el contexto conceptual y científico (estado del arte) y fundamenta las bases teóricas que sustentan la investigación.
- **Cómo construirlo:** (1) identificar palabras o temas clave; (2) recopilar bibliografía; (3) depurar (**estableciendo antes la metodología del trabajo**); (4) ordenar por relevancia con un hilo conductor, **de lo general a lo particular**, definiendo subsecciones y qué se trata en cada párrafo, y qué figuras se incluyen; (5) escribir.
- **Errores frecuentes:**
  - Marcos teóricos extensos (solo en tesis teóricas). **"Si no está en tu metodología no debería estar en tu marco teórico."**
  - Monotonía: usar figuras (propias o referenciadas) para destacar o ayudar a comprender una idea.
  - Redundancia y repeticiones (copy-paste): acotar con lenguaje breve y técnico; evitar conectores innecesarios ("Es importante resaltar que… además… es de gran importancia mencionar…").
  - **Escribir el marco teórico antes de la metodología: debería ser al revés**; si se hizo así, releer para depurar.
  - "Si a vos te aburre, probablemente a otro también. Si vos no lo entendés, otra persona tampoco." La revisión del tutor es fundamental.

## 4. Cómo se relaciona con esta tesis (a tener en cuenta al reescribir)
- Sol (8 oct. 2026): Materiales y métodos se reescribió copiando textos ya escritos y revisados del laboratorio (borrador `mat meth draft` y Coirini et al. 2022), sin innovar; primero el comportamiento, AnyMaze al final, y toda la estadística en su sección. Ver la regla en `CLAUDE.md`.
- Aplicar al reescribir: método como manual reproducible; sujetos con n, criterios de inclusión/exclusión (en este trabajo **no se aplicaron criterios de inclusión por exploración mínima**) y comité de ética; marca, modelo y versión de todo (AnyMaze 7.66, GraphPad Prism 11.1.0, etc.); imágenes solo si ayudan a reproducir; fotos propias cuando se pueda.
- El Marco teórico debería contener solo lo que se usa en la metodología (hoy puede tener contenido que no se usa) y no repetir al Estado del arte.
