"""Índice de preferencia por la solución endulzada: §5.1.1 de la tesis (Figura 5.1).

Índice de preferencia por caja = consumo de solución endulzada / (solución + agua), con el consumo
promedio de todo el período de tratamiento (mL por g de peso corporal por día). La caja es la unidad
experimental (n = 7 cajas por grupo). Se compara entre los grupos sacarosa y stevia con un ANOVA de
dos vías (edad x tratamiento), prueba de Tukey entre las cuatro celdas que comparten fila o columna,
pruebas de supuestos (Shapiro-Wilk sobre los residuos, Brown-Forsythe) y, como los residuos no son
normales, confirmación con la prueba de Mann-Whitney dentro de cada edad.

Datos: datos/consumo_promedio_por_caja.csv (exportado de la hoja "averaged rm" del Excel de consumos
del laboratorio; la caja i de solución está emparejada con la caja i de agua del mismo grupo).
Uso:  python analisis/indice_preferencia.py   (escribe analisis/resultados_indice_preferencia.txt)
"""
import io, itertools, os
import numpy as np, pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.libqsturng import psturng
from scipy import stats

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
salida = io.StringIO()
def out(*a):
    print(*a); print(*a, file=salida)

d = pd.read_csv(os.path.join(RAIZ, "datos", "consumo_promedio_por_caja.csv"))
d["IP"] = d.solucion_mL_g_dia / (d.solucion_mL_g_dia + d.agua_mL_g_dia)
out("Índice de preferencia por grupo:")
out(d.groupby(["edad", "tratamiento"]).IP.agg(["count", "mean", "sem"]).round(3).to_string())

m = smf.ols("IP ~ C(edad, Sum) * C(tratamiento, Sum)", data=d).fit()
a = anova_lm(m, typ=3)
gl = int(m.df_resid)
out("\nANOVA de dos vías (edad x tratamiento):")
for src, nom in [("C(edad, Sum):C(tratamiento, Sum)", "Interacción"), ("C(tratamiento, Sum)", "Tratamiento"), ("C(edad, Sum)", "Edad")]:
    F, gl1 = a.loc[src, "F"], a.loc[src, "df"]
    out(f"   {nom}: F({int(gl1)}, {gl}) = {F:.2f}; p = {a.loc[src, 'PR(>F)']:.4g}; eta2p = {F * gl1 / (F * gl1 + gl):.3f}")

out("\nTukey:")
cel = d.groupby(["edad", "tratamiento"]).IP.agg(["mean", "count"])
for c1, c2 in itertools.combinations(cel.index, 2):
    if c1[0] != c2[0] and c1[1] != c2[1]:
        continue
    q = abs(cel.loc[c1, "mean"] - cel.loc[c2, "mean"]) / np.sqrt(m.mse_resid / 2 * (1 / cel.loc[c1, "count"] + 1 / cel.loc[c2, "count"]))
    out(f"   {c1[0]} {c1[1]} vs. {c2[0]} {c2[1]}: p = {float(np.atleast_1d(psturng(q, 4, gl))[0]):.4f}")

out("\nSupuestos:")
out(f"   Shapiro-Wilk (residuos): p = {stats.shapiro(m.resid).pvalue:.4f}")
out(f"   Brown-Forsythe: p = {stats.levene(*[g.IP.values for _, g in d.groupby(['edad', 'tratamiento'])], center='median').pvalue:.4f}")
out("\nMann-Whitney, sacarosa vs. stevia dentro de cada edad:")
for edad in ("Juvenil", "Adulto"):
    x = d[d.edad == edad]
    p = stats.mannwhitneyu(x[x.tratamiento == "Sacarosa"].IP, x[x.tratamiento == "Stevia"].IP).pvalue
    out(f"   {edad}: p = {p:.4f}")

open(os.path.join(RAIZ, "analisis", "resultados_indice_preferencia.txt"), "w", encoding="utf-8").write(salida.getvalue())
