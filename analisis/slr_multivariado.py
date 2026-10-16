"""Análisis multivariado exploratorio de la prueba SLR (objetivos de máxima 1 y 2 de la tesis).

Datos: datos/slr_por_animal.csv, una fila por animal (n = 117), armada uniendo:
  - día 1: tiempo de exploración de cada objeto (A1, A2, A3) y distancia recorrida por minuto
    (Resultados SLR/SLR_Dia1_exploracion_distancia_por_grupo.xlsx, hoja "Datos por animal");
  - día 2: tasa de exploración y DI (Resultados SLR/SLR PRISMA RESULTADOS.xlsx, hoja ORIGEN, que
    reproduce exactamente las tablas cargadas en Prism) y exploración total
    (Resultados SLR/SLR_exploracion_D1_vs_D2  actualizado.xlsx).
Variables del análisis principal (5): t_A1, t_A2 y t_A3 del día 1, exploración total del día 2 y DI.
La distancia del día 1 se excluye porque identifica la cohorte (2026 vs. 2024-2025), que no tiene
control contemporáneo; se informa como análisis de sensibilidad.

Uso:  python analisis/slr_multivariado.py   (escribe analisis/resultados_multivariado.txt y las figuras)
"""
import os, sys, io
import numpy as np, pandas as pd
from scipy import stats
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold, cross_val_score, permutation_test_score
from sklearn.metrics import silhouette_score, adjusted_rand_score, confusion_matrix, balanced_accuracy_score
from sklearn.inspection import permutation_importance
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEMILLA, N_ARBOLES = 0, 300
N_PERM = int(os.environ.get("N_PERM", 500))  # N_PERM=1 para rehacer solo las figuras (los p no se usan)
salida = io.StringIO()
def out(*a):
    print(*a); print(*a, file=salida)

d = pd.read_csv(os.path.join(RAIZ, "datos", "slr_por_animal.csv"))
d["grupo"] = d.edad + " " + d.trat.str.lower()
d["cohorte_2026"] = (d.anio == 2026).astype(int)
F5 = ["t_A1_dia1_s", "t_A2_dia1_s", "t_A3_dia1_s", "exploracion_total_dia2_s", "DI_dia2"]
F6 = F5[:3] + ["distancia_dia1_m_min"] + F5[3:]
NOMBRE = {"t_A1_dia1_s": "A1 (día 1)", "t_A2_dia1_s": "A2 (día 1)", "t_A3_dia1_s": "A3 (día 1)",
          "distancia_dia1_m_min": "Distancia (día 1)", "exploracion_total_dia2_s": "Exploración (día 2)", "DI_dia2": "DI (día 2)"}
out(f"n = {len(d)} animales; faltantes: {d[F6].isna().sum().to_dict()}")
out(pd.crosstab(d.grupo, d.anio).to_string())

# ------------------------------------------------------------------ PCA
Z = StandardScaler().fit_transform(d[F5])
pca = PCA().fit(Z)
sc = pca.transform(Z)
d["PC1"], d["PC2"] = sc[:, 0], sc[:, 1]
out("\n== PCA (5 variables estandarizadas)")
out("varianza explicada (%):", (pca.explained_variance_ratio_ * 100).round(1), "acumulada:", (np.cumsum(pca.explained_variance_ratio_) * 100).round(1))
cargas = pd.DataFrame(pca.components_[:2].T, index=[NOMBRE[f] for f in F5], columns=["PC1", "PC2"])
out(cargas.round(2).to_string())
for c in ("PC1", "PC2"):
    a = anova_lm(smf.ols(f"{c} ~ C(edad, Sum) * C(trat, Sum)", data=d).fit(), typ=3)
    gl = int(a.loc["Residual", "df"])
    out(f"{c}: ANOVA de dos vías  " + "; ".join(f"{n}: F({int(a.loc[i, 'df'])}, {gl}) = {a.loc[i, 'F']:.2f}, p = {a.loc[i, 'PR(>F)']:.4f}"
        for i, n in [("C(edad, Sum)", "edad"), ("C(trat, Sum)", "tratamiento"), ("C(edad, Sum):C(trat, Sum)", "interacción")]))
    t = stats.ttest_ind(d.loc[d.cohorte_2026 == 1, c], d.loc[d.cohorte_2026 == 0, c])
    out(f"     cohorte 2026 vs. 2024-2025: t({len(d) - 2}) = {t.statistic:.2f}, p = {t.pvalue:.4f}")
out(d.groupby("grupo")[["PC1", "PC2"]].agg(["mean", "sem"]).round(2).to_string())

# ------------------------------------------------------------------ Ward
L = linkage(Z, method="ward")
out("\n== Clustering jerárquico de Ward (distancia euclídea, variables estandarizadas)")
sil = {}
for k in range(2, 7):
    lab = fcluster(L, k, "maxclust"); sil[k] = silhouette_score(Z, lab)
    out(f"k = {k}: silueta = {sil[k]:.3f}; ARI con el grupo = {adjusted_rand_score(d.grupo, lab):.3f}; "
        f"con el tratamiento = {adjusted_rand_score(d.trat, lab):.3f}; con la edad = {adjusted_rand_score(d.edad, lab):.3f}; con la cohorte = {adjusted_rand_score(d.cohorte_2026, lab):.3f}")
kmej = max(sil, key=sil.get)
d["cluster"] = fcluster(L, kmej, "maxclust")
out(f"k con mayor silueta = {kmej}")
out(pd.crosstab(d.grupo, d.cluster).to_string())
out(d.groupby("cluster")[F5].median().round(2).to_string())

# ------------------------------------------------------------------ Random Forest
def bosque():
    return make_pipeline(SimpleImputer(strategy="median"),
                         RandomForestClassifier(n_estimators=N_ARBOLES, min_samples_leaf=2, class_weight="balanced", random_state=SEMILLA))
def evaluar(df, feat, y, nombre, detalle=False):
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=SEMILLA)
    s = cross_val_score(bosque(), df[feat], df[y], cv=cv, scoring="balanced_accuracy", n_jobs=-1)
    _, _, pv = permutation_test_score(bosque(), df[feat], df[y], cv=StratifiedKFold(5, shuffle=True, random_state=SEMILLA),
                                      scoring="balanced_accuracy", n_permutations=N_PERM, random_state=SEMILLA, n_jobs=-1)
    out(f"{nombre}: exactitud balanceada = {s.mean():.3f} ± {s.std():.3f} (azar = {1 / df[y].nunique():.3f}); prueba de permutación ({N_PERM}): p = {pv:.4f}")
    if not detalle:
        return
    clases = sorted(df[y].unique())
    cm = np.zeros((len(clases), len(clases))); imp = []
    for tr, te in cv.split(df[feat], df[y]):
        m = bosque().fit(df[feat].iloc[tr], df[y].iloc[tr])
        cm += confusion_matrix(df[y].iloc[te], m.predict(df[feat].iloc[te]), labels=clases)
        imp.append(permutation_importance(m, df[feat].iloc[te], df[y].iloc[te], n_repeats=10, random_state=SEMILLA, scoring="balanced_accuracy").importances_mean)
    cmn = pd.DataFrame(cm / cm.sum(axis=1, keepdims=True), index=clases, columns=clases)
    out("matriz de confusión (proporción por fila, 10 × 5 particiones):\n" + cmn.round(2).to_string())
    imp = pd.DataFrame(imp, columns=[NOMBRE[f] for f in feat])
    out("importancia por permutación en los conjuntos de prueba (media ± DE):\n" + (imp.mean().round(3).astype(str) + " ± " + imp.std().round(3).astype(str)).to_string())
    return cmn, imp

out(f"\n== Random Forest ({N_ARBOLES} árboles; validación cruzada estratificada 5 × 10)")
cmn, imp = evaluar(d, F5, "grupo", "6 grupos (5 variables)", detalle=True)
evaluar(d, F5, "trat", "3 tratamientos (5 variables)")
evaluar(d[d.trat != "Stevia"], F5, "trat", "control vs. sacarosa (5 variables)")
evaluar(d[d.trat != "Sacarosa"], F5, "trat", "control vs. stevia (5 variables)")
out("-- sensibilidad: con la distancia del día 1 (6 variables) y cohorte como variable a predecir")
evaluar(d, F6, "grupo", "6 grupos (6 variables)")
evaluar(d, F6, "cohorte_2026", "cohorte 2026 vs. 2024-2025 (6 variables)")
evaluar(d, F5, "cohorte_2026", "cohorte 2026 vs. 2024-2025 (5 variables)")
open(os.path.join(RAIZ, "analisis", "resultados_multivariado.txt"), "w", encoding="utf-8").write(salida.getvalue())

# ------------------------------------------------------------------ figuras
COL = {"Control": "#0000ff", "Sacarosa": "#ff0000", "Stevia": "#00c000"}
plt.rcParams.update({"font.family": "Arial", "font.weight": "bold", "pdf.fonttype": 42, "axes.labelweight": "bold"})
coma = matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:g}".replace(".", ",").replace("-", "−"))
def ejes(ax):
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"): ax.spines[sp].set_linewidth(1.2)
    ax.tick_params(labelsize=9, width=1.2, length=3.5)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 3.5), gridspec_kw={"width_ratios": [1.45, 1]})
for (e, t), g in d.groupby(["edad", "trat"]):
    lleno = e == "Juvenil"
    a1.scatter(g.PC1, g.PC2, s=16, marker="o" if lleno else "^", facecolor=COL[t] if lleno else "white", edgecolor=COL[t], linewidth=0.8, alpha=0.55, zorder=2)
    a1.errorbar(g.PC1.mean(), g.PC2.mean(), xerr=g.PC1.sem(), yerr=g.PC2.sem(), fmt="o" if lleno else "^", ms=9 if lleno else 10, mfc=COL[t],
                mec="black", mew=1.2, ecolor="black", elinewidth=1, capsize=2, zorder=4)
a1.axhline(0, color="0.75", lw=0.6, zorder=1); a1.axvline(0, color="0.75", lw=0.6, zorder=1)
a1.set_xlabel(f"CP1 ({pca.explained_variance_ratio_[0] * 100:.1f} %)".replace(".", ","), fontsize=9.5)
a1.set_ylabel(f"CP2 ({pca.explained_variance_ratio_[1] * 100:.1f} %)".replace(".", ","), fontsize=9.5)
ejes(a1); a1.xaxis.set_major_formatter(coma); a1.yaxis.set_major_formatter(coma)
a1.text(-0.16, 1.02, "A", transform=a1.transAxes, fontsize=12)
y = np.arange(len(F5))[::-1]
a2.barh(y + 0.18, cargas.PC1, 0.34, color="0.25", label="CP1"); a2.barh(y - 0.18, cargas.PC2, 0.34, color="0.7", label="CP2")
a2.set_yticks(y); a2.set_yticklabels(cargas.index, fontsize=8.5); a2.axvline(0, color="black", lw=0.8)
a2.set_xlabel("Carga", fontsize=9.5); ejes(a2); a2.xaxis.set_major_formatter(coma)
a2.legend(fontsize=8, frameon=False, loc="upper left", bbox_to_anchor=(0.62, 1.0))
a2.text(-0.62, 1.02, "B", transform=a2.transAxes, fontsize=12)
h = [Line2D([], [], marker="o", ls="", mfc=COL[t], mec="black", ms=7, label=t) for t in COL] + \
    [Line2D([], [], marker="o", ls="", mfc="0.5", mec="black", ms=7, label="Juvenil"), Line2D([], [], marker="^", ls="", mfc="0.5", mec="black", ms=7, label="Adulto")]
fig.legend(handles=h, fontsize=8, frameon=False, loc="lower center", ncol=5)
fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig(os.path.join(RAIZ, "figuras", "Fig5_ML_pca.pdf")); plt.close(fig)

orden = ["Juvenil control", "Juvenil sacarosa", "Juvenil stevia", "Adulto control", "Adulto sacarosa", "Adulto stevia"]
cmn = cmn.loc[orden, orden]
fig, (b1, b2) = plt.subplots(1, 2, figsize=(7.6, 3.4), gridspec_kw={"width_ratios": [1.15, 1]})
im = b1.imshow(cmn.values, cmap="Greys", vmin=0, vmax=1)
cort = ["Juv. C", "Juv. S", "Juv. St", "Ad. C", "Ad. S", "Ad. St"]
b1.set_xticks(range(6)); b1.set_xticklabels(cort, fontsize=7.5, rotation=45, ha="right"); b1.set_yticks(range(6)); b1.set_yticklabels(cort, fontsize=7.5)
for i in range(6):
    for j in range(6):
        b1.text(j, i, f"{cmn.values[i, j]:.2f}".replace(".", ","), ha="center", va="center", fontsize=7, color="white" if cmn.values[i, j] > 0.5 else "black")
b1.set_xlabel("Grupo predicho", fontsize=9.5); b1.set_ylabel("Grupo real", fontsize=9.5)
b1.text(-0.3, 1.02, "A", transform=b1.transAxes, fontsize=12)
m, s = imp.mean().sort_values(), imp.std()
b2.barh(range(len(m)), m.values, xerr=s[m.index].values, color="0.45", ecolor="black", capsize=2)
b2.set_yticks(range(len(m))); b2.set_yticklabels(m.index, fontsize=8.5); b2.axvline(0, color="black", lw=0.8)
b2.set_xlabel("Importancia por permutación", fontsize=9.5); ejes(b2); b2.xaxis.set_major_formatter(coma)
b2.text(-0.62, 1.02, "B", transform=b2.transAxes, fontsize=12)
fig.tight_layout(); fig.savefig(os.path.join(RAIZ, "figuras", "Fig5_ML_rf.pdf")); plt.close(fig)
