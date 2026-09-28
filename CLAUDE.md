# CLAUDE.md — Contexto para trabajar en este proyecto

## Qué es
Tesina (PFC) de Bioingeniería, ITBA. Autor: Thiago Sayegh (legajo 62260).
Título: *Impacto de la nutrición temprana sobre el desarrollo neurobiológico y la conducta: efectos de Stevia rebaudiana Bertoni*.
Lugar: IByME-CONICET. Tutora: Dra. María Sol Kruse.
Diseño: ratas macho Sprague-Dawley; 2 ventanas etarias (juvenil desde PD25, adulta desde PD75) × 3 condiciones (stevia 4 % p/v, sacarosa 10 % p/v, agua). 25 días de exposición + lavado. Batería: OF, NOR (T1–T4), SLR (d-SLR y s-SLR), prueba de preferencia. Histología: NeuN, DCX, PCNA (confocal). Aporte de bioingeniería: PCA + clustering jerárquico (Ward) y Random Forest sobre métricas de AnyMaze©.

Este repositorio es la **fuente única** de la tesis. La versión en Google Docs quedó congelada.

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
- La exploración del día 1 del SLR no fue equivalente entre grupos: debe tratarse como control/covariable en resultados y discusión.
- Software estadístico: GraphPad Prism 11.1.0. ML: Python + scikit-learn.
- Límites de la plantilla: Introducción ≤ 3 carillas; hasta el Marco teórico ≤ 20 % del total; Perspectivas ≤ 1 carilla; Conclusiones ≤ 2 carillas; Resumen ≤ media carilla, con palabras clave.

## Pendientes conocidos
A confirmar con Sol:
- Comité de ética y número de protocolo.
- Duración de la sesión de Open Field.
- n finales por grupo de las cohortes previas (Tabla 4.2).
- Participación del grupo adulto en el brazo de tiempos agudos.
- Duración y esquema de la prueba de preferencia.
- Cita del aparato de OF: `pian2009milk` probablemente mal mapeada (candidatas: `kruse2019sucrose`, `rey2024metformin`).

Bibliografía:
- `pichonriviere2023` y `rey2024metformin` no se citan (no se imprimen): citarlas o borrarlas.
- `ennys2019`: la URL no corresponde al título. `laracastor2025ssb`: la URL es de Infobae; dejar solo el DOI.

Texto:
- Resumen en tiempo futuro (formato anteproyecto) y sin palabras clave.
- Nota de la Tabla 4.1 mezcla regiones del brazo agudo con neurogénesis.
- Encuadre metodológico de §3.2 (sec:bases) abierto.
- Erratas: "isóceles" → "isósceles"; falta punto en "nivel de azar 0 En ambos casos" (4_materiales_y_metodos.tex).
- Carátula: fecha de entrega; docentes de cátedra comentados.

Datos/figuras:
- Figuras faltantes: `Fig4_esquema_SLR.png`, `Fig4_objetos_SLR.jpg`, `Fig5_exploracion_SLR.pdf`, `Fig5_DI_SLR.pdf`, `Fig5_estimacion_Tukey_SLR.png`; logo `logos/logo_itba.png`.
- Falta la planilla SLR2 JUV CTROL STEV 250606: al subirla, re-correr el análisis y actualizar tablas del SLR.
- Por redactar: Resultados de consumo/peso, OF, NOR, neurogénesis, ML; Discusión; Conclusiones.
- Cronograma: redacción en octubre, entrega en noviembre de 2026.

## Etiquetas existentes
Capítulos: cap:introduccion, cap:estado-arte, cap:marco-teorico, cap:metodos, cap:resultados, cap:discusion, cap:perspectivas, cap:conclusiones.
Marco teórico: sec:ventanas (3.1), sec:bases (3.2), sec:cascada (3.3), sec:multivariado (3.4).
Métodos: sec:diseno, sec:soluciones, sec:registro, sec:conductual, sec:principio, sec:of, sec:nor, sec:slr, sec:rigor, sec:histologia, sec:analisis, sec:estadistico, sec:ml.
Tablas: tab:diseno, tab:cohortes, tab:slr-di, tab:slr-anova, tab:anx-tasa. Figuras: fig:esquema-slr, fig:objetos-slr, fig:slr-exploracion, fig:slr-di, fig:slr-tukey. Ecuaciones: eq:fwer, eq:pca, eq:tasa, eq:di. Anexo: anx:tasa.
