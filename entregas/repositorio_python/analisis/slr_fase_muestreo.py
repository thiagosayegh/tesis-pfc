"""Fase de muestreo (día 1) de la prueba SLR: §5.4 de la tesis (Figura 5.9).

1. Tiempo de exploración de cada uno de los tres objetos idénticos (A1, A2, A3): ANOVA de tres vías
   por configuración (d-SLR y s-SLR), con edad y tratamiento como factores entre sujetos y el objeto
   como factor intrasujeto; corrección de Greenhouse-Geisser para el factor intrasujeto.
   Las comparaciones post hoc de Tukey se hacen sobre la exploración media de los tres objetos,
   entre los tres tratamientos dentro de cada edad.
2. Distancia recorrida por minuto: ANOVA de dos vías (edad x tratamiento) por configuración y
   Tukey entre las celdas de la misma fila y columna (como "compare each cell mean with the other
   cell mean in its row and column" de GraphPad Prism).

Datos: datos/slr_por_animal.csv (una fila por animal).
Uso:  python analisis/slr_fase_muestreo.py   (escribe analisis/resultados_fase_muestreo.txt)
"""
import io, itertools, os
import numpy as np, pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.libqsturng import psturng
from scipy import stats
import warnings
# el modelo intrasujeto lleva un término por animal, que es colineal con edad x tratamiento:
# statsmodels avisa que la matriz es de rango incompleto, pero los F del objeto y sus
# interacciones son correctos (mismos resultados que un ANOVA de medidas repetidas)
warnings.filterwarnings("ignore")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
salida = io.StringIO()
def out(*a):
    print(*a); print(*a, file=salida)

d = pd.read_csv(os.path.join(RAIZ, "datos", "slr_por_animal.csv"))
d = d.rename(columns={"t_A1_dia1_s": "A1", "t_A2_dia1_s": "A2", "t_A3_dia1_s": "A3", "distancia_dia1_m_min": "dist"})
d["edad"] = d.edad.str.lower(); d["trat"] = d.trat.str.lower()
d["subj"] = range(len(d))

def tukey(df, y, k, solo_misma_edad=False):
    """Tukey-Kramer entre las celdas edad x tratamiento que comparten fila o columna (k = 6), o solo
    entre los tres tratamientos dentro de cada edad (k = 3), con la varianza residual del modelo."""
    m = smf.ols(f"{y} ~ C(edad, Sum) * C(trat, Sum)", data=df).fit()
    cel = df.groupby(["edad", "trat"])[y].agg(["mean", "count"])
    for c1, c2 in itertools.combinations(cel.index, 2):
        if (c1[0] != c2[0] and c1[1] != c2[1]) or (solo_misma_edad and c1[0] != c2[0]):
            continue
        q = abs(cel.loc[c1, "mean"] - cel.loc[c2, "mean"]) / np.sqrt(m.mse_resid / 2 * (1 / cel.loc[c1, "count"] + 1 / cel.loc[c2, "count"]))
        p = float(np.atleast_1d(psturng(q, k, m.df_resid))[0])
        out(f"      {c1[0]} {c1[1]} vs. {c2[0]} {c2[1]}: p = {p:.4f}")

def anova_mixto(df):
    """Entre sujetos (edad, tratamiento) sobre la media de los 3 objetos; intrasujeto (objeto) con el
    animal como bloque; épsilon de Greenhouse-Geisser con la covarianza de los residuos por grupo."""
    largo = df.melt(id_vars=["subj", "edad", "trat"], value_vars=["A1", "A2", "A3"], var_name="obj", value_name="t")
    df = df.assign(media=df[["A1", "A2", "A3"]].mean(axis=1))
    entre = anova_lm(smf.ols("media ~ C(edad, Sum) * C(trat, Sum)", data=df).fit(), typ=3)
    intra = anova_lm(smf.ols("t ~ C(subj) + C(obj, Sum) * C(edad, Sum) * C(trat, Sum)", data=largo).fit(), typ=2)
    X = df[["A1", "A2", "A3"]].values - df.groupby(["edad", "trat"])[["A1", "A2", "A3"]].transform("mean").values
    S = np.cov(X.T, ddof=df.groupby(["edad", "trat"]).ngroups)
    Q, _ = np.linalg.qr(np.array([[1, -1, 0], [1, 0, -1]], float).T)
    M = Q.T @ S @ Q
    eps = np.trace(M) ** 2 / (2 * np.trace(M @ M))
    out(f"   épsilon de Greenhouse-Geisser = {eps:.3f}")
    gl = entre.loc["Residual", "df"]
    for src, nom in [("C(edad, Sum):C(trat, Sum)", "Edad x Tratamiento"), ("C(trat, Sum)", "Tratamiento"), ("C(edad, Sum)", "Edad")]:
        out(f"   {nom}: F({int(entre.loc[src, 'df'])}, {int(gl)}) = {entre.loc[src, 'F']:.2f}; p = {entre.loc[src, 'PR(>F)']:.4f}")
    gl2 = intra.loc["Residual", "df"]
    for src, nom in [("C(obj, Sum)", "Objeto"), ("C(obj, Sum):C(edad, Sum)", "Objeto x Edad"),
                     ("C(obj, Sum):C(trat, Sum)", "Objeto x Tratamiento"), ("C(obj, Sum):C(edad, Sum):C(trat, Sum)", "Objeto x Edad x Tratamiento")]:
        F, gl1 = intra.loc[src, "F"], intra.loc[src, "df"]
        out(f"   {nom}: F({int(gl1)}, {int(gl2)}) = {F:.2f}; p = {intra.loc[src, 'PR(>F)']:.4f}; "
            f"p (Greenhouse-Geisser) = {stats.f.sf(F, gl1 * eps, gl2 * eps):.4f}")
    out("   Tukey sobre la exploración media de los tres objetos (tratamientos dentro de cada edad):")
    tukey(df, "media", 3, solo_misma_edad=True)

out("=== 1. Exploración de los tres objetos en la fase de muestreo")
for conf in ("d-SLR", "s-SLR"):
    x = d[d.configuracion == conf].reset_index(drop=True)
    out(f"\n-- {conf} (n = {len(x)})")
    out(x.groupby(["edad", "trat"])[["A1", "A2", "A3"]].mean().round(1).to_string())
    anova_mixto(x)

out("\n=== 2. Distancia recorrida por minuto en la fase de muestreo")
for conf in ("d-SLR", "s-SLR"):
    x = d[(d.configuracion == conf) & d.dist.notna()].reset_index(drop=True)
    out(f"\n-- {conf} (n = {len(x)}; sin registro de distancia: {int(((d.configuracion == conf) & d.dist.isna()).sum())})")
    out(x.groupby(["edad", "trat"]).dist.agg(["count", "mean", "sem"]).round(2).to_string())
    m = smf.ols("dist ~ C(edad, Sum) * C(trat, Sum)", data=x).fit()
    a = anova_lm(m, typ=3)
    for src, nom in [("C(edad, Sum):C(trat, Sum)", "Interacción"), ("C(trat, Sum)", "Tratamiento"), ("C(edad, Sum)", "Edad")]:
        out(f"   {nom}: F({int(a.loc[src, 'df'])}, {int(m.df_resid)}) = {a.loc[src, 'F']:.2f}; p = {a.loc[src, 'PR(>F)']:.4f}")
    out("   Tukey:")
    tukey(x, "dist", 6)

open(os.path.join(RAIZ, "analisis", "resultados_fase_muestreo.txt"), "w", encoding="utf-8").write(salida.getvalue())
