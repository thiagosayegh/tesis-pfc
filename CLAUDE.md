# CLAUDE.md — Contexto para trabajar en este proyecto

## Qué es
Tesina (PFC) de Bioingeniería, ITBA. Autor: Thiago Sayegh (legajo 62260).
Título: *Impacto de la nutrición temprana sobre el desarrollo neurobiológico y la conducta: efectos de Stevia rebaudiana Bertoni*.
Lugar: IByME-CONICET. Tutora: Dra. María Sol Kruse.
Diseño: ratas macho Sprague-Dawley; 2 ventanas etarias (juvenil desde PD25, adulta desde PD75) × 3 condiciones (stevia 4 % p/v, sacarosa 10 % p/v, agua). 25 días de exposición + 25 días de lavado. Batería: consumo/peso, OF, NOR (T1–T4), SLR (d-SLR y s-SLR). Histología: NeuN, DCX, PCNA (confocal). Aporte de bioingeniería: PCA + clustering jerárquico (Ward) y Random Forest sobre métricas de AnyMaze©.

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

Nota técnica: `preambulo.tex` mapea `\DeclareLanguageMapping{english}{american}` para la bibliografía. Es necesario porque el `\DeclareSourcemap` fuerza `langid=english` en cada entrada, pero `english.lbx` no activa `\uspunctuation` (biblatex resetea la puntuación de las comillas del título en cada entrada); mapear a `american.lbx` corrige que la coma del título IEEE quede dentro de las comillas. No tocar sin entender esto.

## Estructura del repositorio
- `main.tex` — orden de secciones (plantilla oficial ITBA). No poner contenido acá.
- `preambulo.tex` — paquetes, formato, macros (incluye `tikz` y `subcaption`).
- `capitulos/` — un archivo por capítulo/sección preliminar (`00_caratula.tex` … `9_anexos.tex`).
- `referencias.bib` — bibliografía (biblatex-ieee), 38 entradas. Cada una tiene comentado su número en la versión de Google Docs.
- `figuras/`, `logos/` — imágenes ya procesadas y listas para `\incluirfigura`. Convención de nombre: `Fig<capítulo>_<tema>[_<subgrupo>].ext` (p. ej. `Fig5_consumo_liquidos_adulto.pdf`). Preferir PDF vectorial (exportado de GraphPad Prism) sobre PNG/JPG.
- `FIGURAS_PENDIENTES.md` — checklist de correcciones a hacer en GraphPad Prism (ejes/leyendas en inglés, paleta de colores, etc.) para las figuras que no se pueden editar desde el `.tex`.
- `docs/referencia/papers/` — PDF de los artículos citados, bajados de fuentes legales (nunca sitios piratas). `INDICE.md` documenta de dónde salió cada uno.
- `datos/`, `analisis/` — vacíos; destinados a planillas y scripts de Python si en algún momento se corre el pipeline propio (ver `docs/analisis_y_datos.md`). **Ningún análisis de la tesis sale de acá**: los números de los Resultados salen de GraphPad Prism.
- Carpetas `Resultado(s) <tema>/` en la raíz (`Resultado consumos/`, `Resultados NOR/`, `Resultados Open Field/`, `Resultados SLR/`, `Resultados inmucitoquimica/`) — datos crudos y exports de Prism (xlsx/txt/pdf) que respaldan cada sección de Resultados, para trazabilidad y para poder re-verificar cualquier número. No son parte del texto de la tesis.

## Convenciones de redacción y notación
- **Idioma:** español académico formal, impersonal ("se evaluó", "se utilizaron"). Sin calcos del inglés. Primera persona solo en la Justificación.
- **Citas:** `\cite{clave}` (varias: `\cite{a,b}`). Numeración IEEE automática por orden de aparición: nunca escribir números a mano.
- **Referencias cruzadas:** siempre `\ref{}`. Prefijos: `cap:`, `sec:`, `tab:`, `fig:`, `eq:`, `anx:`. Estilo en el texto: `\S\ref{sec:...}`, `Tabla~\ref{tab:...}`, `Figura~\ref{fig:...}`.
- **Figuras:** `\incluirfigura[width=...]{Archivo.ext}` (dibuja un recuadro "FALTA ARCHIVO" si falta el archivo — no es un error de compilación, hay que revisar visualmente). Paneles A/B/C con `subfigure` (ver `fig:consumo-liquidos`, `fig:nor-tasa`, `fig:slr-di` como ejemplos). Toda figura/tabla con `\caption[corto]{largo}` y `\label`.
- **Números:** coma decimal. En texto: `0,015`; en modo matemático: `$p = 0{,}015$`. **El símbolo `\%` nunca va dentro de `$...$`** (babel lo redefine y rompe la compilación) — cerrar el modo matemático antes: `$92{,}32$\,\%`. Unidades con siunitx: `\SI{50}{\micro\metre}`. Porcentajes en texto: `10\,\%`.
- **"Tasa de exploración" / "índice de discriminación (DI)"**: terminología unificada (no usar "índice de exploración"). Definidas una sola vez, en `sec:nor` (§4.4.3) con notación $t_N$/$t_F$ (DI = 2·tasa − 1, azar 0,5 y 0); el resto del documento remite ahí, no redefine.
- **Convención de signo** (fijada en §4.6.1): toda diferencia de medias se reporta como "primer grupo − segundo grupo", nombrando explícitamente ambos grupos en el texto (p. ej. "diferencia control − sacarosa = 0,138"), para que el signo sea interpretable sin ambigüedad.
- **Paleta de colores de las figuras por grupo**: azul = control, rojo = sacarosa, verde = stevia (ya usada en las figuras de consumo; ítem pendiente de unificar en NOR/SLR, ver `FIGURAS_PENDIENTES.md`).
- **Pendientes:** `\pendiente{}` (falta redactar/datos), `\confirmar{}` (dato a confirmar con Sol), `\revisar{}` (problema detectado, sin resolver). Buscar con `grep -rn "pendiente{\|confirmar{\|revisar{" capitulos/`.
- **Macros:** `\stevia` (*Stevia rebaudiana* Bertoni), `\Srebaudiana`, `\anymaze`.
- Tablas con booktabs (`\toprule/\midrule/\bottomrule`), sin líneas verticales.

## Reglas de contenido (no negociables)
- **El GTT (test de tolerancia a la glucosa) y el EPM (laberinto en cruz elevado) están excluidos de esta tesis**: no se realizaron en este diseño (sí existen en un manuscrito hermano del mismo laboratorio); no deben aparecer en índice, métodos ni resultados.
- No inventar datos, resultados, n, valores de p ni referencias. Si falta un dato, usar `\confirmar{}` o `\pendiente{}`.
- No modificar los objetivos de mínima/máxima ni la hipótesis sin pedido explícito.
- Software estadístico: GraphPad Prism 11.1.0 (todos los resultados). ML: Python + scikit-learn (todavía no corrido).

## Decisiones de análisis estadístico vigentes
- **SLR**: ANOVA de dos vías edad × tratamiento, cada configuración por separado (d-SLR, s-SLR); Tukey comparando cada media con su fila y columna; se reportan **tanto el DI como la tasa de exploración equivalente**, ambos en el cuerpo de §5.4 (Tablas 5.4/5.6, Figuras 5.8/5.9), con una explicación explícita de que DI = 2·tasa − 1 y de que ambos dan resultados estadísticos idénticos; t de una muestra contra DI = 0; Mann-Whitney cuando los residuos no son normales. Los DI negativos son válidos y no se corrigen. La exploración del día 1 del SLR no fue equivalente entre grupos: tratarla como covariable/control, no como resultado. Resultados de §5.4 organizados por hallazgo (validación / efecto sacarosa / efecto stevia), no por configuración, igual que el NOR.
- **NOR**: mismo esquema que SLR — ANOVA de dos vías edad × tratamiento, cada demora (T2, T3, T4) por separado; Tukey comparando cada media con su fila y columna; se reporta tasa de exploración (azar 0,5), con t de una muestra contra el azar para cada grupo y demora (agregada en la Fase 5 de la revisión de jurado, calculada a partir de los datos crudos por animal en `Resultados NOR/RESULTADOS NOR T2 T3 T4.xlsx`). Resultados de §5.3 organizados por hallazgo (validación / efecto sacarosa / efecto stevia / síntesis), no por demora.
- **Consumo de líquidos/alimento**: normalizado al peso corporal (mL o g por g de peso/día); la **caja**, no el animal, es la unidad experimental. Analizado con ANOVA de medidas repetidas multifactorial (edad × tratamiento × fluido × tiempo durante el tratamiento; edad × tratamiento × tiempo durante el lavado; edad × tratamiento sobre el promedio del período para alimento), corrección de Geisser-Greenhouse, post hoc de **Šídák** (no Tukey).
- **Fuente de los resultados de consumo**: `Resultado consumos/Resultados consumos.pdf` tiene 12 páginas, pero **solo las primeras 5 están validadas** (consumo combinado durante el tratamiento, consumo de agua durante el lavado, consumo de alimento). Las páginas 6–12 (ANOVA separados por edad, AUC, prueba de preferencia de sacarosa) son análisis exploratorios descartados; la prueba de preferencia de dos botellas no se incluye en la tesis (solo el índice de preferencia calculado desde el consumo del tratamiento): no usarlos sin confirmar antes.
- **OF**: aparato cuadrado de 75×75×30 cm (no 75×55×30, que son las dimensiones del NOR — error ya corregido). Sesión de 5 min. Cita del aparato: `pian2009milk` (confirmada correcta contra la propuesta original del laboratorio).
- **Protocolo de extracto de stevia**: decocción 10 min, reposo 20 min, filtrado, re-hervido 45–50 min hasta 300 mL, dilución a 4 % (40 mL/L). Esta es la versión correcta (ya reflejada en el texto).

## Estado de la tesis por sección
| Sección | Estado |
|---|---|
| Carátula, Resumen, Glosario | Completos. Resumen en pasado con resultado real de SLR; falta solo fecha de entrega/co-tutor. |
| 1. Introducción | Completa. |
| 2. Estado del arte | Completo. |
| 3. Marco teórico | Completo. Figura del gradiente de carga cognitiva del SLR (`fig:slr-carga`) regenerada con matplotlib en español (ya no es la versión BioRender adaptada del blog); esquema de la cascada neurogénica (`fig:cascada-neurogenica`, `Fig3_cascada_neurogenica.jpg`, PCNA → DCX → NeuN) generado con IA a partir de un prompt propio; el pie lo declara y cita conceptualmente `kempermann2015neurogenesis`; el borde inferior de los paneles quedó recortado en el original. |
| 4. Materiales y métodos | Completo. Placeholder de foto pendiente: aparato de OF (`fig:of-esquema`) y fotomicrografías confocales (`fig:confocal-giro-dentado`). Inventario de cohortes movido a Anexo B (antes Tabla 4.2 en §4.1). Sec. 4.5 (inmunocitoquímica) con varios `\pendiente{}` puntuales nuevos (fijación/perfusión, n por grupo, secciones por animal/región, método de conteo). |
| 5.1 Consumo y peso corporal | Líquidos (tratamiento y lavado) y alimento redactados y verificados contra datos crudos, con índice de preferencia y estimación calórica de la sacarosa agregados. Falta: gráfico de chow del grupo adulto, y toda la subsección de peso corporal (sin datos todavía). |
| 5.2 Campo abierto (OF) | `\pendiente{}`. Hay datos sin subir a `Resultados Open Field/` más que dos PDF de presentación/resumen sin analizar. |
| 5.3 NOR | Completo, reorganizado por hallazgo (validación/sacarosa/stevia/síntesis), con prueba t contra el azar agregada a la Tabla 5.2 y forest plot de Tukey (`fig:nor-tukey`) nuevo. Verificado contra datos crudos. |
| 5.4 SLR | Completo, reorganizado por el mismo esquema que el NOR (validación/sacarosa/stevia), sin cambios numéricos. Subsección de exploración (día 1 vs. día 2, `fig:slr-exploracion`) redactada con `Resultados SLR/SLR_exploracion_D1_vs_D2.xlsx` (tiempo de exploración activa por sesión, d-SLR y s-SLR combinadas; figura generada con matplotlib desde ese Excel). Incluye ANOVA de dos vías sobre log(tiempo) por sesión, con Tukey (familias restringidas), calculado en Python (no en Prism; interacción edad × tratamiento significativa en ambos días, día 1 no equivalente entre grupos). Falta aclarar los n del día 1. |
| 5.5 Neurogénesis | `\pendiente{}`. Hay un PDF en `Resultados inmucitoquimica/` pero es insuficiente (pocos datos, falta el grupo stevia); hace falta el archivo de Prism de Sol para completarlo. |
| 5.6 ML/multivariado | `\pendiente{}`. No corrido todavía (`datos/` y `analisis/` vacíos). |
| 6. Discusión, 7. Perspectivas, 8. Conclusiones, Agradecimientos | `\pendiente{}` en su totalidad. |
| Anexos | Un solo anexo: Anexo A (n por grupo experimental en la SLR, sin desglose por año ni cohorte). El DI y la tasa de exploración del SLR se muestran juntos en el cuerpo de §5.4 (a pedido de Thiago, ambos índices se presentan y discuten en el texto, no solo el DI). |

## Material de referencia adicional (`docs/referencia/papers/`)
No son citas verificadas para `referencias.bib` salvo que ya estén incorporadas (ver `INDICE.md`):
- `mat meth draft (1).pdf` / `extracto stevia.pdf` — borrador de manuscrito hermano (Agustina Marchena, mismo laboratorio): diseño similar pero con GTT y EPM (que esta tesis no usa). Útil como referencia cruzada de protocolo y de la composición química real del extracto de stevia.
- `AGOSTINA MIRANDA_LU1113912_PFI BIO-BIN 2024.pdf` — **no es del laboratorio de Kruse** (Laboratorio de Plasticidad Neuronal, Instituto Leloir, dir. Trinchero/Schinder). Solo sirve como antecedente general de anatomía hipocampal/neurogénesis, no como continuidad metodológica.
- `proyecto efectos a largo plazo stevia.docx.pdf` — propuesta de proyecto original del laboratorio (mismo título que esta tesis). Fuente primaria para Materiales y métodos; ya se usó para corregir el aparato de OF y el protocolo de stevia.
- `ghoshswaby2021slr` — ya **no** se cita en el texto: `fig:slr-carga` se regeneró con matplotlib (Fase 6 de la revisión de jurado) y el caption ahora cita el protocolo `reichelt2021slr` como fuente conceptual. Queda en `referencias.bib` sin citar, marcada con un comentario; decidir si se borra.

## Scripts
Ninguno todavía. `docs/analisis_y_datos.md` describe cómo sería un futuro pipeline en Python (`analisis/slr_pipeline.py`) para preparar datos de AnyMaze, pero es exploratorio: los números de la tesis salen siempre de Prism, no de ese pipeline.

## Etiquetas existentes
Capítulos: cap:introduccion, cap:estado-arte, cap:marco-teorico, cap:metodos, cap:resultados, cap:discusion, cap:perspectivas, cap:conclusiones.
Marco teórico: sec:ventanas (3.1), sec:bases (3.2), sec:cascada (3.3), sec:multivariado (3.4).
Métodos: sec:diseno, sec:soluciones, sec:registro, sec:conductual, sec:principio, sec:of, sec:nor, sec:slr, sec:rigor, sec:histologia, sec:analisis, sec:estadistico, sec:ml.
Resultados: sec:res-consumo (sec:res-consumo-tratamiento, sec:res-consumo-lavado, sec:res-consumo-chow, sec:res-consumo-peso), sec:res-of, sec:res-nor (sec:res-nor-validacion, sec:res-nor-sacarosa, sec:res-nor-stevia, sec:res-nor-sintesis), sec:res-slr (sec:res-slr-exploracion, sec:res-slr-validacion, sec:res-slr-sacarosa, sec:res-slr-stevia, sec:res-slr-sintesis), sec:res-neurogenesis, sec:res-ml.
Tablas: tab:diseno, tab:n-slr (Anexo A), tab:consumo-liquidos, tab:nor-tasa, tab:nor-anova, tab:slr-di, tab:slr-tasa, tab:slr-anova.
Figuras: fig:esquema-slr, fig:objetos-slr, fig:cascada-neurogenica, fig:slr-carga, fig:linea-temporal, fig:of-esquema, fig:confocal-giro-dentado, fig:consumo-liquidos, fig:consumo-liquidos-promedio, fig:agua-lavado, fig:chow-juvenil, fig:nor-tasa, fig:nor-tukey, fig:slr-exploracion, fig:slr-di, fig:slr-tasa, fig:slr-tukey.
Ecuaciones: eq:fwer, eq:pca, eq:tasa, eq:di. Anexo: anx:muestra (A, único anexo).

## Pendientes a confirmar con Sol
- Comité de ética: qué CICUAL aprobó el protocolo (IByME y/o Facultad de Ciencias Veterinarias, UBA) y su número (no figura en fuentes públicas; solo lo sabe Sol).
- Participación del grupo adulto en el brazo de tiempos agudos.
- SLR, exploración (§5.4.1): el Excel está por sesión (no por animal) y mezcla d-SLR y s-SLR, por lo que el análisis (hecho en Python, aprobado por Thiago como análisis chico) es exploratorio y así se declara en el texto y en §4.6.1. Los n del día 1 no coinciden con el día 2 ni con el Anexo A (juvenil-sacarosa 13 vs. 18, juvenil-stevia 15 vs. 20, adulto-control 21 vs. 20): confirmar con Sol. La Discusión todavía no trata la no equivalencia de la exploración del día 1.
- Archivo de Prism completo de inmunocitoquímica (falta grupo stevia).
- Métodos (§4): umbral numérico de exploración total para el criterio de inclusión (NOR y SLR); si se evaluó un efecto de cohorte antes de combinar los datos; cita de ARRIVE 2.0 (Percie du Sert et al., PLoS Biol., 2020; sin agregar al .bib). Resuelto con datos de Sol: alojamiento 3–4 por jaula, ciclo 12:12, asignación pareja, un único experimentador ciego, AnyMaze última versión, valores muy atípicos excluidos (ninguno en SLR), pruebas a las 10:00 h, eutanasia por CO2. Ojo: el abstracto de OF (`Resultados Open Field/`) usa ANOVA de dos vías edad × tratamiento, no una vía como dice el documento del laboratorio.
- Histología (§4.5): PD al sacrificio, nivel rostro-caudal (bregma) y hemisferio analizado; método de fijación/perfusión, n por grupo, secciones por animal/región del giro dentado, y método de conteo (¿manual/ImageJ/estereología?, ¿ciego al tratamiento?).
- Cita que respalde la equivalencia de dulzor entre la stevia al 4\,% p/v y la sacarosa al 10\,% p/v (§3.2).
- kcal/g del alimento balanceado, para completar la estimación calórica de §5.1.
- Bibliografía: `pichonriviere2023` y `rey2024metformin` no se citan en el texto; `ennys2019` quedó sin URL (la que tenía era de otro documento) y hay que conseguir la oficial de la ENNyS 2; falta volumen y páginas de `bhatt2025prenatal`; decidir si se borra `ghoshswaby2021slr` (ya no se cita, ver más arriba). 30 de las 38 entradas de `referencias.bib` siguen sin intentar bajar (ver `docs/referencia/papers/INDICE.md`).
- Figuras GraphPad: ver el checklist completo en `FIGURAS_PENDIENTES.md` (traducciones, typo "Sacaosa", paleta de colores, corchetes de Tukey).

## Cronograma
Redacción en octubre, entrega en noviembre de 2026.
