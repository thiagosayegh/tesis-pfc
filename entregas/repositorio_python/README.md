# Análisis en Python — PFC de Bioingeniería (ITBA)

**Efectos neurobiológicos a largo plazo de la exposición a *Stevia rebaudiana* durante la etapa juvenil y la adultez**

Autor: Thiago Sayegh (62260) · Tutora: Dra. María Sol Kruse · IByME-CONICET

Este repositorio contiene el código y los datos de los análisis de la tesis que se hicieron en Python. El resto de la estadística (consumo de líquidos, *open field*, NOR, SLR e inmunocitoquímica) se hizo en GraphPad Prism 11.1.0, como se indica en §4.5 de la tesis.

## Contenido

| Script | Qué hace | Sección de la tesis |
|---|---|---|
| `analisis/slr_multivariado.py` | Análisis multivariado de la prueba SLR: PCA, clustering jerárquico de Ward (silueta y ARI) y Random Forest (validación cruzada estratificada 5 × 10, prueba de permutación e importancia por permutación). Genera las Figuras 5.15 y 5.16. | §3.4, §4.6, §5.6 y §6.6 (objetivos de máxima 1 y 2) |
| `analisis/slr_fase_muestreo.py` | Fase de muestreo (día 1) de la SLR: ANOVA de tres vías del tiempo de exploración de los tres objetos (edad × tratamiento × objeto, con corrección de Greenhouse-Geisser) y ANOVA de dos vías de la distancia recorrida, con pruebas de Tukey. | §5.4 (Figura 5.9) |
| `analisis/indice_preferencia.py` | Índice de preferencia por la solución endulzada por caja: ANOVA de dos vías, Tukey, supuestos y Mann-Whitney. | §5.1.1 (Figura 5.1) |

Cada script escribe sus resultados en `analisis/resultados_*.txt`. Los archivos incluidos son los que se obtuvieron al correr los scripts y coinciden con los valores informados en la tesis.

## Datos

- `datos/slr_por_animal.csv`: una fila por animal de la prueba SLR (n = 117). Se armó uniendo, por edad, tratamiento, configuración, número de animal y par de sesiones, los registros de la fase de muestreo (día 1) y de la fase de prueba (día 2) exportados de AnyMaze 7.66 y cargados en Prism.
  - `edad`, `trat`, `configuracion` (d-SLR o s-SLR), `anio` (cohorte), `lote`, sesiones y número de animal de cada día;
  - `t_A1_dia1_s`, `t_A2_dia1_s`, `t_A3_dia1_s`: tiempo de exploración de cada objeto en la fase de muestreo (s);
  - `distancia_dia1_m_min`: distancia recorrida por minuto en la fase de muestreo (sin registro en 6 animales);
  - `exploracion_total_dia2_s`, `tasa_exploracion_dia2`, `DI_dia2`: exploración total, tasa de exploración e índice de discriminación en la fase de prueba.
- `datos/consumo_promedio_por_caja.csv`: consumo promedio de solución endulzada y de agua durante el tratamiento, por caja (mL por g de peso corporal por día; n = 7 cajas por grupo).

## Cómo correrlo

```bash
pip install -r requirements.txt
python analisis/slr_multivariado.py
python analisis/slr_fase_muestreo.py
python analisis/indice_preferencia.py
```

Los scripts se corren desde la raíz del repositorio. El multivariado tarda unos minutos por las 500 permutaciones; con `N_PERM=1` solo rehace las figuras, sin los valores *p*. Todas las semillas aleatorias están fijas, así que los resultados son reproducibles.

## Notas

- En la prueba de Tukey, `psturng` de statsmodels informa 0,9 como valor máximo: un `p = 0.9000` significa *p* ≥ 0,9.
- En el multivariado se excluye la distancia del día 1 del análisis principal, porque permite identificar la cohorte de 2026 (que no tuvo un grupo control contemporáneo). Se informa como análisis de sensibilidad (§4.6 y §5.6).
- Los datos son del laboratorio de la Dra. M. S. Kruse (IByME-CONICET), en parte todavía no publicados, y se comparten solo para evaluar este trabajo.
