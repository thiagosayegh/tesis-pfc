# Análisis y manejo de datos

## Reglas de manejo de datos
- Un DI negativo es un resultado válido: nunca se corrige, ajusta ni se interpreta como error.
- Los resultados se reportan tal como salen. Marco investigativo, no confirmatorio.
- **Día 1 del SLR (muestreo de tres objetos):** solo control de equivalencia de codificación (no se aplicó ningún criterio de inclusión por exploración mínima); no es una variable de resultado. La exploración del día 1 **no fue equivalente entre grupos**: debe tratarse como control/covariable y discutirse.
- Las celdas "inv" son datos faltantes irrecuperables: se preservan como NaN, nunca se imputan.
- Sesiones de duración distinta = cortes tempranos de grabación, no errores de datos.
- Distancias > 1000 en exportaciones de AnyMaze: dividir por 1000 (problema de separador decimal por configuración regional).
- AnyMaze genera dos familias de datos: (a) variables automáticas de seguimiento (distancia, velocidad, cruces de línea, entradas y tiempo por zona); (b) tiempo de exploración activa puntuado **manualmente**. DI y tasa de exploración se calculan **solo** con (b).
- Tasa de exploración = t_nov / (t_nov + t_fam), azar = 0,5. DI = (t_nov − t_fam) / (t_nov + t_fam), azar = 0. DI = 2·tasa − 1 (mismos resultados estadísticos; se reporta DI).
- n = 9 en algunos grupos juveniles es simplemente porque hubo 9 animales (no hubo exclusiones).

## Análisis estadístico vigente para el SLR (el que está en la tesis)
- Hecho en GraphPad Prism 11.1.0 (no en el pipeline de Python).
- ANOVA de dos vías **edad de exposición × tratamiento**, **una vez por configuración** (d-SLR y s-SLR por separado). Tukey comparando cada media con las de su misma edad y su mismo tratamiento.
- t de una muestra de cada grupo contra DI = 0. Mann-Whitney cuando los residuos no son normales (ocurrió en s-SLR).
- Pretests: Shapiro-Wilk (normalidad de residuos) y Brown-Forsythe (homogeneidad de varianzas).
- Se reporta DI en el texto; la tasa de exploración va al Anexo A.
- Este análisis reemplaza al hallazgo previo de una interacción tratamiento × configuración. No volver a citar ese hallazgo previo.
- Los datos de stevia d-SLR estaban mal copiados en una versión anterior y fueron corregidos. Si se rehace algún análisis, verificar que los valores de las Tablas 5.1, 5.2 y A.1 coincidan con los datos corregidos.

## Pipeline de Python (`analisis/slr_pipeline.py`, si se copia acá)
- Lee exportaciones Excel de AnyMaze con subtablas de estructura irregular; las parsea por **nombre de columna, no por posición**; aplica un diccionario de configuración por hoja; produce tablas en formato largo, ancho y un reporte de exclusiones.
- Modelo que usa el pipeline: ANOVA de dos vías tratamiento × configuración (SS tipo II) + Shapiro-Wilk y Brown-Forsythe, contrapartes no paramétricas (Kruskal-Wallis, Mann-Whitney), t de una muestra por celda grupo-configuración, d de Cohen contra el grupo control de mayo. Otros tests en uso: Wilcoxon, correlación de Pearson.
- Inspección de Excel con `openpyxl` (`read_only=True, data_only=True`), en dos pasadas: primero estructura, después contenido.
- Es una herramienta exploratoria y de preparación de datos; **los números de la tesis salen del análisis de Prism descripto arriba**.

## Archivos de datos conocidos (no están en este repo; copiar a `datos/` si se quiere trabajar con ellos)
- `AadultoSLR.xlsx` — SLR adultos 2024-2025.
- `JUVENIL_SLR.xlsx` / `Copy_of_JUVENIL_SLR__1_.xlsx` — SLR juveniles 2025 (incluye el test control + stevia 250606).
- `SLRADULTOS2026.xlsx` — adultos 2026.
- `JUVENIL2026.xlsx` — juveniles 2026.
- Pendiente: la hoja "SLR2 JUV CTROL STEV 250606" está incompleta; al subir la planilla completa, re-correr el análisis y actualizar tablas y figuras del SLR.

## Diseño de las cohortes de SLR (para Métodos y para la Discusión de limitaciones)
- **Adultos 2025 (doc del laboratorio "RATAS SLR"):** control y sacarosa muestreados en dos tandas el mismo día (08/05/2025), test 09/05/2025. Control de diciembre: vasos 18-19/12/2025, ranas 22-23/12/2025. Stevia adulto: 25/04/2024 según la fecha en la hoja (el documento dice "250424": **año a confirmar**).
- **Adultos 2026:** sacarosa 1-5 y stevia 1-5 en diseño cruzado; vasos 06-07/08/2026 y ranas 10-11/08/2026; configuración invertida entre corridas; sin grupo agua propio. El test con ranas (260811) no tiene etiquetas de animal: identidad 1-5 = sacarosa y 6-10 = stevia asumida por orden (**a confirmar**).
- **Juveniles 2026:** 20 animales en dos pares independientes. Primer par (5 sacarosa + 5 stevia) con vasos 19-20/07/2026; segundo par (10 animales nuevos) con ranas 23-24/07/2026; configuración contrabalanceada entre pares. **Par y tipo de objeto quedan confundidos por diseño.**
- Los grupos control provienen solo de cohortes 2025 (sin control 2026): limitación declarada.
- Ambos juegos de objetos (vasos/tazas y ranas) se usaron en todas las cohortes y se agruparon; hubo animales de ambas edades en todos los años.
- Cohortes del estudio: 2024, 2025 y 2026 (Tabla 4.2 del documento).

## Limitaciones que la Discusión debe declarar
1. Controles no contemporáneos con los grupos tratados de 2026.
2. Cohortes agrupadas en distintos años (aunque con protocolo idéntico).
3. Exploración del día 1 no equivalente entre grupos.
4. Par y tipo de objeto confundidos en juveniles 2026.
5. Puntuación manual de la exploración por un único observador ciego: criterio consistente, pero no se estimó concordancia entre observadores.
6. Sin grupo agua propio en adultos 2026.
7. Tamaños muestrales acotados (9-10 por grupo) para los análisis multivariados (M1/M2): declarar la cautela.

## Excluido de la tesis
- **GTT (test de tolerancia a la glucosa) y su AUC:** no se realizó; no debe aparecer en índice, métodos ni resultados. El documento del laboratorio lo menciona: ignorarlo.
- Parámetros séricos (glucosa, fructosamina, triglicéridos, colesterol) y Western blot aparecen en el documento del laboratorio pero **no están** en el borrador actual: no incluirlos sin confirmar con Sol y con Thiago.
