# CLAUDE.md — Contexto para trabajar en este proyecto

## Qué es
Tesina (PFC) de Bioingeniería, ITBA. Autor: Thiago Sayegh (legajo 62260).
Título: *Impacto de la nutrición temprana sobre el desarrollo neurobiológico y la conducta: efectos de Stevia rebaudiana Bertoni*.
Lugar: IByME-CONICET. Tutora: Dra. María Sol Kruse.
Diseño: ratas macho Sprague-Dawley; 2 ventanas etarias (juvenil desde PD25, adulta desde PD75) × 3 condiciones (stevia 4 % p/v, sacarosa 10 % p/v, agua). 25 días de exposición + lavado. Batería: OF, NOR (T1–T4), SLR (d-SLR y s-SLR), prueba de preferencia. Histología: NeuN, DCX, PCNA (confocal). Aporte de bioingeniería: PCA + clustering jerárquico (Ward) y Random Forest sobre métricas de AnyMaze©.

Este repositorio es la **fuente única** de la tesis. La versión en Google Docs quedó congelada.

## Leer primero (según la tarea)
Este archivo tiene las reglas resumidas. El detalle está en `docs/`:
- `docs/guia_plantilla_ITBA.md` — qué exige la plantilla oficial por capítulo y sus límites. **Leer antes de escribir o revisar cualquier capítulo.**
- `docs/estilo_y_redaccion.md` — tono, reglas de fondo y cómo comunicarte con Thiago (voseo en el chat; español académico formal en el texto de la tesis).
- `docs/analisis_y_datos.md` — reglas de manejo de datos, estadística vigente, diseño de cohortes y limitaciones que debe declarar la Discusión.
- `docs/referencia/` — documento del laboratorio (fuente de protocolos), plantilla original, guía IEEE. `docs/referencia/papers/` es para PDF de artículos clave: si está vacía, no atribuir hallazgos específicos a un paper que no se pueda verificar.
- `datos/` y `analisis/` — planillas y scripts (vacías hasta que Thiago las copie).
Si una regla de este archivo contradice a `docs/`, avisar a Thiago en lugar de elegir una.

## Compilar
```
latexmk          # pdflatex + biber → build/main.pdf
latexmk -c       # limpiar auxiliares
```
Antes de dar por terminado cualquier cambio: compilar y verificar que no haya errores, citas/referencias indefinidas (`undefined` en build/main.log) ni `Overfull \hbox` nuevos.

## Estructura
- `main.tex` — orden de secciones (según la plantilla oficial ITBA). No poner contenido acá.
- `preambulo.tex` — paquetes, formato, macros.
- `capitulos/` — un archivo por capítulo (`1_introduccion.tex` … `9_anexos.tex`).
- `referencias.bib` — bibliografía (biblatex-ieee). Cada entrada tiene comentado su número en la versión de Google Docs.
- `figuras/`, `logos/` — imágenes. Preferir PDF vectorial para gráficos (exportar desde GraphPad Prism como PDF).

## Convenciones
- **Idioma:** español académico formal, impersonal ("se evaluó", "se utilizaron"). Sin calcos del inglés. Primera persona solo en la Justificación.
- **Citas:** `\cite{clave}` (varias: `\cite{a,b}`). La numeración IEEE es automática por orden de aparición: nunca escribir números de referencia a mano. Referencias en convención IEEE inglesa.
- **Referencias cruzadas:** siempre `\ref{}`; nunca números a mano. Prefijos: `cap:`, `sec:`, `tab:`, `fig:`, `eq:`, `anx:`. Estilo usado en el texto: `\S\ref{sec:...}`, `Tabla~\ref{tab:...}`, `Figura~\ref{fig:...}`.
- **Figuras:** usar `\incluirfigura[width=...]{Archivo.ext}` (dibuja un recuadro si falta el archivo). Toda figura/tabla con `\caption[corto]{largo}` y `\label`.
- **Números:** coma decimal. En texto: `0,015`; en modo matemático: `$p = 0{,}015$`. Unidades con siunitx: `\SI{50}{\micro\metre}`, `\SI{4}{\celsius}`. Porcentajes: `10\,\%`.
- **Pendientes:** `\pendiente{}` (falta redactar/datos), `\confirmar{}` (dato a confirmar con Sol), `\revisar{}` (problema detectado). Buscar con `grep -rn "pendiente\|confirmar\|revisar" capitulos/`.
- **Macros:** `\stevia` (*Stevia rebaudiana* Bertoni), `\Srebaudiana`, `\anymaze`.
- Tablas con booktabs (`\toprule/\midrule/\bottomrule`), sin líneas verticales.

## Reglas de contenido (no negociables)
- **El GTT (test de tolerancia a la glucosa) y su AUC están excluidos de la tesis**: no se realizaron; no deben aparecer en índice, métodos ni resultados.
- No inventar datos, resultados, n, valores de p ni referencias. Si falta un dato, usar `\confirmar{}` o `\pendiente{}`.
- No modificar los objetivos de mínima/máxima sin pedido explícito de Thiago.
- SLR: ANOVA de dos vías edad × tratamiento, **cada configuración por separado**; Tukey comparando cada media con su fila y columna; se reporta DI (tasa equivalente en Anexo A); t de una muestra contra DI = 0; Mann-Whitney cuando los residuos no son normales. Los DI negativos son válidos.
- NOR: mismo esquema que SLR —ANOVA de dos vías edad × tratamiento, **cada demora (T2, T3, T4) por separado**; Tukey comparando cada media con su fila y columna; se reporta tasa de exploración (azar 0,5). Sin prueba t de una muestra contra el azar (no forma parte del análisis real para NOR).
- La exploración del día 1 del SLR no fue equivalente entre grupos: debe tratarse como control/covariable en resultados y discusión.
- Software estadístico: GraphPad Prism 11.1.0. ML: Python + scikit-learn.
- Límites de la plantilla: Introducción ≤ 3 carillas; hasta el Marco teórico ≤ 20 % del total; Perspectivas ≤ 1 carilla; Conclusiones ≤ 2 carillas; Resumen ≤ media carilla, con palabras clave.

## Pendientes conocidos
(Actualizado 2026-10-01. Buscar `\confirmar\|\pendiente\|\revisar` en `capitulos/` para el detalle exacto y la ubicación de cada uno.)

A confirmar con Sol:
- Comité de ética y número de protocolo (CICUAL).
- Duración de la sesión de Open Field.
- n finales por grupo de las cohortes previas (Tabla 4.2: cohorte 2024–2025 y cohorte juvenil 2025 "SLR1").
- Participación del grupo adulto en el brazo de tiempos agudos.
- Duración y esquema horario de la prueba de preferencia.
- Fecha de entrega y co-tutor/asesores (carátula).

Bibliografía:
- `pichonriviere2023` y `rey2024metformin` no se citan en el texto (no se imprimen en Referencias): citarlas o borrarlas.
- `ennys2019`: la URL no corresponde al título. `laracastor2025ssb`: la URL es de Infobae; dejar solo el DOI.
- 30 de las 37 entradas de `referencias.bib` todavía no se intentaron bajar a `docs/referencia/papers/` (ver `docs/referencia/papers/INDICE.md` para el detalle y el método).

Texto:
- Nota de la Tabla 4.1 mezcla regiones del brazo agudo con neurogénesis (`\revisar` en 4_materiales_y_metodos.tex).
- Encuadre metodológico de §3.2 (sec:bases) abierto.

Datos/figuras:
- Figuras faltantes: `Fig5_exploracion_SLR.pdf` (exploración día 1 vs. día 2, SLR).
- Placeholders con descripción de la foto/esquema pedido, listos para insertar cuando existan: aparato de OF (fig:of-esquema), fotomicrografías confocales NeuN/DCX/PCNA (fig:confocal-giro-dentado), cascada neurogénica esquemática (fig:cascada-neurogenica).
- Falta la planilla SLR2 JUV CTROL STEV 250606: al subirla, re-correr el análisis y actualizar tablas del SLR.
- `Resultados inmucitoquimica/Resultados inmunocitoquimica.pdf` subido (2026-10-01) pero **no usar todavía**: Thiago tiene pocos datos y falta el grupo stevia; pidió el archivo de Prism a Sol para completarlo antes de redactar §5.6 (sec:res-neurogenesis).
- NOR (§5.3, sec:res-nor) ya redactado (2026-10-01): ANOVA de dos vías edad × tratamiento por demora (T2/T3/T4) — interacción significativa en las tres; sacarosa juvenil difiere del control juvenil en las tres demoras, sacarosa adulta nunca difiere de su control; stevia solo difiere del control en T3 (juvenil) y en T2 (adulto). Fuente: `Resultados NOR/RESULTADOS NOR T2 T3 T4.xlsx`.
- Consumo de líquidos y alimento (§5.1.1-5.1.3, sec:res-consumo-tratamiento/lavado/chow) ya redactado (2026-10-01), a partir de `Resultado consumos/Resultados consumos.pdf` — **ojo**: ese documento tiene 12 páginas pero Sol dijo que solo son válidas las primeras 5 (consumo combinado 4 vías, consumo de agua durante el lavado, consumo de alimento); las secciones de las páginas 6-12 (ANOVAs separados por edad, AUC, prueba de preferencia de sacarosa) **no se usaron** y no hay que usarlas sin confirmar con Sol. Falta: gráfico de chow del grupo adulto (fig:chow-juvenil tiene placeholder) y toda la sección de peso corporal (sec:res-consumo-peso, sin datos subidos todavía).
- Por redactar (todas en `\pendiente{}`): Peso corporal (§5.1.4), OF (§5.2 — Thiago tiene los datos, falta subirlos a una carpeta), neurogénesis (§5.6 — falta completar con Prism y stevia), ML (§5.7); Discusión completa; Conclusiones; Agradecimientos.
- Cronograma: redacción en octubre, entrega en noviembre de 2026.

## Material de referencia adicional (`docs/referencia/papers/`, no son citas verificadas para `referencias.bib` salvo que se indique)
- `mat meth draft (1).pdf`: borrador de manuscrito (Agustina Marchena, lab de Kruse) con diseño hermano (incluye GTT y EPM, que esta tesis **no** usa — confirmado por Thiago). Su protocolo de extracto de stevia (reposo de 20 min, re-hervido de 45–50 min hasta 300\,mL) es el correcto y ya está reflejado en 4_materiales_y_metodos.tex (confirmado por Thiago, 2026-10-01).
- `extracto stevia.pdf`: supplementary materials del mismo manuscrito, con la composición química real del extracto (esteviósidos, RebA, RebC, fenoles, DPPH) — aplicable a esta tesis solo si el lote propio fue caracterizado igual.
- `AGOSTINA MIRANDA_LU1113912_PFI BIO-BIN 2024.pdf`: **no es del laboratorio de Kruse** (es del Laboratorio de Plasticidad Neuronal, Instituto Leloir, dir. Trinchero/Schinder; estudia estimulación Gamma y neurogénesis en ratones envejecidos). Útil solo como antecedente general de anatomía hipocampal y neurogénesis (§1.1–1.5 del documento).
- `proyecto efectos a largo plazo stevia.docx.pdf`: propuesta de proyecto original del laboratorio (mismo título que esta tesis). Resolvió la cita del aparato de OF (`pian2009milk` confirmado correcto) y corrigió sus dimensiones (75×75×30 cm, no 75×55×30 cm, que corresponden al NOR). Buena fuente cruzada para todo Materiales y métodos.
- `ghoshswaby2021slr`: ya integrada a `referencias.bib` y citada en fig:slr-carga (Marco teórico).

## Etiquetas existentes
Capítulos: cap:introduccion, cap:estado-arte, cap:marco-teorico, cap:metodos, cap:resultados, cap:discusion, cap:perspectivas, cap:conclusiones.
Marco teórico: sec:ventanas (3.1), sec:bases (3.2), sec:cascada (3.3), sec:multivariado (3.4).
Métodos: sec:diseno, sec:soluciones, sec:registro, sec:conductual, sec:principio, sec:of, sec:nor, sec:slr, sec:rigor, sec:histologia, sec:analisis, sec:estadistico, sec:ml.
Resultados: sec:res-consumo (sec:res-consumo-tratamiento, sec:res-consumo-lavado, sec:res-consumo-chow, sec:res-consumo-peso), sec:res-of, sec:res-nor (sec:res-nor-t2, sec:res-nor-t3, sec:res-nor-t4, sec:res-nor-sintesis), sec:res-slr (sec:res-slr-exploracion, sec:res-dslr, sec:res-sslr, sec:res-slr-sintesis), sec:res-neurogenesis, sec:res-ml.
Tablas: tab:diseno, tab:cohortes, tab:consumo-liquidos, tab:nor-tasa, tab:nor-anova, tab:slr-di, tab:slr-anova, tab:anx-tasa.
Figuras: fig:esquema-slr, fig:objetos-slr, fig:cascada-neurogenica, fig:slr-carga, fig:linea-temporal, fig:of-esquema, fig:confocal-giro-dentado, fig:consumo-liquidos, fig:consumo-liquidos-promedio, fig:agua-lavado, fig:chow-juvenil, fig:nor-tasa, fig:slr-exploracion, fig:slr-di, fig:slr-tukey, fig:anx-tasa.
Ecuaciones: eq:fwer, eq:pca, eq:tasa, eq:di. Anexo: anx:tasa.
