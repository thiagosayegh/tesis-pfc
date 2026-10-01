# CLAUDE.md — Contexto para trabajar en este proyecto

## Qué es
Tesina (PFC) de Bioingeniería, ITBA. Autor: Thiago Sayegh (legajo 62260).
Título: *Impacto de la nutrición temprana sobre el desarrollo neurobiológico y la conducta: efectos de Stevia rebaudiana Bertoni*.
Lugar: IByME-CONICET. Tutora: Dra. María Sol Kruse.
Diseño: ratas macho Sprague-Dawley; 2 ventanas etarias (juvenil desde PD25, adulta desde PD75) × 3 condiciones (stevia 4 % p/v, sacarosa 10 % p/v, agua). 25 días de exposición + 25 días de lavado. Batería: consumo/peso, OF, NOR (T1–T4), SLR (d-SLR y s-SLR), prueba de preferencia. Histología: NeuN, DCX, PCNA (confocal). Aporte de bioingeniería: PCA + clustering jerárquico (Ward) y Random Forest sobre métricas de AnyMaze©.

Este repositorio es la **fuente única** de la tesis. La versión en Google Docs quedó congelada.

## Leer primero (según la tarea)
Este archivo tiene las reglas resumidas. El detalle está en `docs/`:
- `docs/guia_plantilla_ITBA.md` — qué exige la plantilla oficial por capítulo y sus límites. Leer antes de escribir o revisar cualquier capítulo.
- `docs/estilo_y_redaccion.md` — tono, reglas de fondo y cómo comunicarse en el chat (voseo informal; el texto de la tesis siempre en español académico formal).
- `docs/analisis_y_datos.md` — reglas de manejo de datos, diseño de cohortes y limitaciones que debe declarar la Discusión.
- `docs/referencia/` — documento y propuesta original del laboratorio, plantilla ITBA, guía IEEE. `docs/referencia/papers/` tiene los PDF de artículos clave y su `INDICE.md` (estado de descarga, uno por uno, de cada entrada de `referencias.bib`).
Si una regla de este archivo contradice a `docs/`, avisar en vez de elegir una.

## Compilar
```
latexmk          # pdflatex + biber → build/main.pdf
latexmk -c       # limpiar auxiliares
```
Antes de dar por terminado cualquier cambio: compilar y verificar que no haya errores, citas/referencias indefinidas (`undefined` en build/main.log) ni `Overfull \hbox` nuevos.

## Estructura del repositorio
- `main.tex` — orden de secciones (plantilla oficial ITBA). No poner contenido acá.
- `preambulo.tex` — paquetes, formato, macros (incluye `tikz` y `subcaption`).
- `capitulos/` — un archivo por capítulo/sección preliminar (`00_caratula.tex` … `9_anexos.tex`).
- `referencias.bib` — bibliografía (biblatex-ieee), 37 entradas. Cada una tiene comentado su número en la versión de Google Docs.
- `figuras/`, `logos/` — imágenes ya procesadas y listas para `\incluirfigura`. Convención de nombre: `Fig<capítulo>_<tema>[_<subgrupo>].ext` (p. ej. `Fig5_consumo_liquidos_adulto.pdf`). Preferir PDF vectorial (exportado de GraphPad Prism) sobre PNG/JPG.
- `docs/referencia/papers/` — PDF de los artículos citados, bajados de fuentes legales (nunca sitios piratas). `INDICE.md` documenta de dónde salió cada uno.
- `datos/`, `analisis/` — vacíos; destinados a planillas y scripts de Python si en algún momento se corre el pipeline propio (ver `docs/analisis_y_datos.md`). **Ningún análisis de la tesis sale de acá**: los números de los Resultados salen de GraphPad Prism.
- Carpetas `Resultado(s) <tema>/` en la raíz (`Resultado consumos/`, `Resultados NOR/`, `Resultados Open Field/`, `Resultados SLR/`, `Resultados inmucitoquimica/`) — datos crudos y exports de Prism (xlsx/txt/pdf) que respaldan cada sección de Resultados, para trazabilidad y para poder re-verificar cualquier número. No son parte del texto de la tesis.

## Convenciones de redacción y notación
- **Idioma:** español académico formal, impersonal ("se evaluó", "se utilizaron"). Sin calcos del inglés. Primera persona solo en la Justificación.
- **Citas:** `\cite{clave}` (varias: `\cite{a,b}`). Numeración IEEE automática por orden de aparición: nunca escribir números a mano.
- **Referencias cruzadas:** siempre `\ref{}`. Prefijos: `cap:`, `sec:`, `tab:`, `fig:`, `eq:`, `anx:`. Estilo en el texto: `\S\ref{sec:...}`, `Tabla~\ref{tab:...}`, `Figura~\ref{fig:...}`.
- **Figuras:** `\incluirfigura[width=...]{Archivo.ext}` (dibuja un recuadro "FALTA ARCHIVO" si falta el archivo — no es un error de compilación, hay que revisar visualmente). Paneles A/B/C con `subfigure` (ver `fig:consumo-liquidos`, `fig:nor-tasa`, `fig:slr-di` como ejemplos). Toda figura/tabla con `\caption[corto]{largo}` y `\label`.
- **Números:** coma decimal. En texto: `0,015`; en modo matemático: `$p = 0{,}015$`. **El símbolo `\%` nunca va dentro de `$...$`** (babel lo redefine y rompe la compilación) — cerrar el modo matemático antes: `$92{,}32$\,\%`. Unidades con siunitx: `\SI{50}{\micro\metre}`. Porcentajes en texto: `10\,\%`.
- **Pendientes:** `\pendiente{}` (falta redactar/datos), `\confirmar{}` (dato a confirmar con Sol), `\revisar{}` (problema detectado, sin resolver). Buscar con `grep -rn "pendiente{\|confirmar{\|revisar{" capitulos/`.
- **Macros:** `\stevia` (*Stevia rebaudiana* Bertoni), `\Srebaudiana`, `\anymaze`.
- Tablas con booktabs (`\toprule/\midrule/\bottomrule`), sin líneas verticales.

## Reglas de contenido (no negociables)
- **El GTT (test de tolerancia a la glucosa) y el EPM (laberinto en cruz elevado) están excluidos de esta tesis**: no se realizaron en este diseño (sí existen en un manuscrito hermano del mismo laboratorio); no deben aparecer en índice, métodos ni resultados.
- No inventar datos, resultados, n, valores de p ni referencias. Si falta un dato, usar `\confirmar{}` o `\pendiente{}`.
- No modificar los objetivos de mínima/máxima ni la hipótesis sin pedido explícito.
- Software estadístico: GraphPad Prism 11.1.0 (todos los resultados). ML: Python + scikit-learn (todavía no corrido).

## Decisiones de análisis estadístico vigentes
- **SLR**: ANOVA de dos vías edad × tratamiento, cada configuración por separado (d-SLR, s-SLR); Tukey comparando cada media con su fila y columna; se reporta DI (tasa equivalente en Anexo A); t de una muestra contra DI = 0; Mann-Whitney cuando los residuos no son normales. Los DI negativos son válidos y no se corrigen. La exploración del día 1 del SLR no fue equivalente entre grupos: tratarla como covariable/control, no como resultado.
- **NOR**: mismo esquema que SLR — ANOVA de dos vías edad × tratamiento, cada demora (T2, T3, T4) por separado; Tukey comparando cada media con su fila y columna; se reporta tasa de exploración (azar 0,5). Sin prueba t de una muestra contra el azar.
- **Consumo de líquidos/alimento**: normalizado al peso corporal (mL o g por g de peso/día); la **caja**, no el animal, es la unidad experimental. Analizado con ANOVA de medidas repetidas multifactorial (edad × tratamiento × fluido × tiempo durante el tratamiento; edad × tratamiento × tiempo durante el lavado; edad × tratamiento sobre el promedio del período para alimento), corrección de Geisser-Greenhouse, post hoc de **Šídák** (no Tukey).
- **Fuente de los resultados de consumo**: `Resultado consumos/Resultados consumos.pdf` tiene 12 páginas, pero **solo las primeras 5 están validadas** (consumo combinado durante el tratamiento, consumo de agua durante el lavado, consumo de alimento). Las páginas 6–12 (ANOVA separados por edad, AUC, prueba de preferencia de sacarosa) son análisis exploratorios descartados: no usarlos sin confirmar antes.
- **OF**: aparato cuadrado de 75×75×30 cm (no 75×55×30, que son las dimensiones del NOR — error ya corregido). Cita del aparato: `pian2009milk` (confirmada correcta contra la propuesta original del laboratorio).
- **Protocolo de extracto de stevia**: decocción 10 min, reposo 20 min, filtrado, re-hervido 45–50 min hasta 300 mL, dilución a 4 % (40 mL/L). Esta es la versión correcta (ya reflejada en el texto).

## Estado de la tesis por sección
| Sección | Estado |
|---|---|
| Carátula, Resumen, Glosario | Completos. Resumen en pasado con resultado real de SLR; falta solo fecha de entrega/co-tutor. |
| 1. Introducción | Completa. |
| 2. Estado del arte | Completo. |
| 3. Marco teórico | Completo, incluida figura del gradiente de carga cognitiva del SLR (`fig:slr-carga`) y placeholder de la cascada neurogénica (`fig:cascada-neurogenica`, falta el esquema). |
| 4. Materiales y métodos | Completo. Placeholder de foto pendiente: aparato de OF (`fig:of-esquema`) y fotomicrografías confocales (`fig:confocal-giro-dentado`). |
| 5.1 Consumo y peso corporal | Líquidos (tratamiento y lavado) y alimento redactados y verificados contra datos crudos. Falta: gráfico de chow del grupo adulto, y toda la subsección de peso corporal (sin datos todavía). |
| 5.2 Campo abierto (OF) | `\pendiente{}`. Hay datos sin subir a `Resultados Open Field/` más que dos PDF de presentación/resumen sin analizar. |
| 5.3 NOR | Completo (T2, T3, T4), verificado contra datos crudos. |
| 5.4 SLR | Completo, verificado contra datos crudos. Falta solo `Fig5_exploracion_SLR.pdf` (exploración día 1 vs. día 2). |
| 5.5 Neurogénesis | `\pendiente{}`. Hay un PDF en `Resultados inmucitoquimica/` pero es insuficiente (pocos datos, falta el grupo stevia); hace falta el archivo de Prism de Sol para completarlo. |
| 5.6 ML/multivariado | `\pendiente{}`. No corrido todavía (`datos/` y `analisis/` vacíos). |
| 6. Discusión, 7. Perspectivas, 8. Conclusiones, Agradecimientos | `\pendiente{}` en su totalidad. |
| Anexos | Completo (tasa de exploración SLR). |

## Material de referencia adicional (`docs/referencia/papers/`)
No son citas verificadas para `referencias.bib` salvo que ya estén incorporadas (ver `INDICE.md`):
- `mat meth draft (1).pdf` / `extracto stevia.pdf` — borrador de manuscrito hermano (Agustina Marchena, mismo laboratorio): diseño similar pero con GTT y EPM (que esta tesis no usa). Útil como referencia cruzada de protocolo y de la composición química real del extracto de stevia.
- `AGOSTINA MIRANDA_LU1113912_PFI BIO-BIN 2024.pdf` — **no es del laboratorio de Kruse** (Laboratorio de Plasticidad Neuronal, Instituto Leloir, dir. Trinchero/Schinder). Solo sirve como antecedente general de anatomía hipocampal/neurogénesis, no como continuidad metodológica.
- `proyecto efectos a largo plazo stevia.docx.pdf` — propuesta de proyecto original del laboratorio (mismo título que esta tesis). Fuente primaria para Materiales y métodos; ya se usó para corregir el aparato de OF y el protocolo de stevia.
- `ghoshswaby2021slr` — entrada ya integrada a `referencias.bib`, fuente de `fig:slr-carga`.

## Scripts
Ninguno todavía. `docs/analisis_y_datos.md` describe cómo sería un futuro pipeline en Python (`analisis/slr_pipeline.py`) para preparar datos de AnyMaze, pero es exploratorio: los números de la tesis salen siempre de Prism, no de ese pipeline.

## Etiquetas existentes
Capítulos: cap:introduccion, cap:estado-arte, cap:marco-teorico, cap:metodos, cap:resultados, cap:discusion, cap:perspectivas, cap:conclusiones.
Marco teórico: sec:ventanas (3.1), sec:bases (3.2), sec:cascada (3.3), sec:multivariado (3.4).
Métodos: sec:diseno, sec:soluciones, sec:registro, sec:conductual, sec:principio, sec:of, sec:nor, sec:slr, sec:rigor, sec:histologia, sec:analisis, sec:estadistico, sec:ml.
Resultados: sec:res-consumo (sec:res-consumo-tratamiento, sec:res-consumo-lavado, sec:res-consumo-chow, sec:res-consumo-peso), sec:res-of, sec:res-nor (sec:res-nor-t2, sec:res-nor-t3, sec:res-nor-t4, sec:res-nor-sintesis), sec:res-slr (sec:res-slr-exploracion, sec:res-dslr, sec:res-sslr, sec:res-slr-sintesis), sec:res-neurogenesis, sec:res-ml.
Tablas: tab:diseno, tab:cohortes, tab:consumo-liquidos, tab:nor-tasa, tab:nor-anova, tab:slr-di, tab:slr-anova, tab:anx-tasa.
Figuras: fig:esquema-slr, fig:objetos-slr, fig:cascada-neurogenica, fig:slr-carga, fig:linea-temporal, fig:of-esquema, fig:confocal-giro-dentado, fig:consumo-liquidos, fig:consumo-liquidos-promedio, fig:agua-lavado, fig:chow-juvenil, fig:nor-tasa, fig:slr-exploracion, fig:slr-di, fig:slr-tukey, fig:anx-tasa.
Ecuaciones: eq:fwer, eq:pca, eq:tasa, eq:di. Anexo: anx:tasa.

## Pendientes a confirmar con Sol
- Comité de ética y número de protocolo (CICUAL).
- Duración de la sesión de Open Field y de la prueba de preferencia.
- n finales por grupo de las cohortes previas (Tabla 4.2).
- Participación del grupo adulto en el brazo de tiempos agudos.
- Archivo de Prism completo de inmunocitoquímica (falta grupo stevia).
- Bibliografía: `pichonriviere2023` y `rey2024metformin` no se citan en el texto; `ennys2019` tiene la URL mal; `laracastor2025ssb` debería dejar solo el DOI. 30 de las 37 entradas de `referencias.bib` siguen sin intentar bajar (ver `docs/referencia/papers/INDICE.md`).

## Cronograma
Redacción en octubre, entrega en noviembre de 2026.
