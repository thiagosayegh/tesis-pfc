# Índice de PDF de referencias

Estado de la descarga de PDF legales (acceso abierto / repositorio institucional / PMC) para las entradas de `referencias.bib`. Nunca se usaron sitios piratas ni se intentó saltear paywalls o protecciones anti-bot (Cloudflare, CAPTCHA).

**Progreso: 7 de 37 entradas procesadas** (6 pedidas explícitamente + `ghoshswaby2021slr`, agregada el 2026-10-01 como fuente de la Figura 3.2). Las restantes todavía no se intentaron — quedan listadas al final para continuar cuando Thiago lo pida.

**Actualización 2026-10-01:** Thiago subió él mismo el PDF de `kruse2019sucrose` (`2019 Psychoneuroendocrinol.pdf`), resolviendo la única entrada paywalled de la tanda original. También subió duplicados de `coirini2022sucrose` y `reichelt2021slr` (sin novedad) y material de contexto no citable directamente: un borrador de manuscrito de Agustina Marchena (mismo lab, diseño hermano con GTT/EPM que Thiago no usa) y la tesina de Agostina Miranda (Instituto Leloir, lab de Trinchero/Schinder — **no es del mismo laboratorio**, solo antecedente general de anatomía hipocampal).

## Hallazgo importante: 3 referencias con DOI/PMID/URL incorrectos en `referencias.bib`

Al verificar cada descarga contra los metadatos reales del PDF/registro encontrado, aparecieron **tres discrepancias** entre lo citado en el `.bib` y la fuente real. No se tocó `referencias.bib` (la tarea pidió no modificar nada todavía), pero esto rompe la numeración IEEE si no se corrige:

| Clave | Campo | Valor actual en `referencias.bib` | Valor correcto verificado |
|---|---|---|---|
| `reichelt2021slr` | `doi` | `10.1038/s41596-021-00617-2` | `10.1038/s41596-021-00627-w` |
| `reichelt2021slr` | `url` | `pmc.ncbi.nlm.nih.gov/articles/PMC10267474/` (apunta a **otro paper**, de Frontiers in Behavioral Neuroscience) | el PMC correcto no está identificado; usar la URL de Nature: `https://www.nature.com/articles/s41596-021-00627-w` |
| `coirini2022sucrose` | `doi` / `eid` | `10.3390/biomedicines10112803` | `10.3390/biomedicines10112723` |
| `reichelt2016sucrose` | `url` (PMID) | `pubmed/27317798` (ese PMID es un editorial de HIV en *Clinical Infectious Diseases*, no tiene nada que ver) | PMID correcto: `27317199` |

## Las 6 entradas pedidas

| Clave | Título | Estado | Detalle |
|---|---|---|---|
| `reichelt2021slr` | The spontaneous location recognition task for assessing spatial pattern separation and memory across a delay in rats and mice | ✅ **Descargado** | `reichelt2021slr.pdf`. Bajado del sitio del laboratorio de la autora (tcnlab.ca), copia del PDF de Springer auto-archivada legalmente. Verificado por metadatos internos del PDF (título, DOI y autor exactos). |
| `coirini2022sucrose` | Long-Term Memory Function Impairments following Sucrose Exposure in Juvenile versus Adult Rats | ✅ **Descargado** | `coirini2022sucrose.pdf`. MDPI (Biomedicines) es open access, pero el sitio bloquea descargas automáticas (403, protección anti-bot) — se consiguió en cambio desde el repositorio institucional CONICET (`ri.conicet.gov.ar`), acceso libre, verificado por metadatos. |
| `kruse2019sucrose` | Sucrose exposure in juvenile rats produces long-term changes in fear memory and anxiety-like behavior | ✅ **Descargado** (a mano, por Thiago) | `2019 Psychoneuroendocrinol.pdf`. Psychoneuroendocrinology (Elsevier), paywall — no se consiguió por vía automática (ni PMC ni CONICET lo tenían), pero Thiago tiene acceso institucional y lo subió directamente el 2026-10-01. |
| `ghoshswaby2021slr` | Can you separate it? Using landmarks with similar locations to test memory in rodents | ✅ **Descargado** | `Can you separate it_...pdf`. Entrada "Behind the Paper" de Research Communities by Springer Nature, acceso abierto sin restricciones. Fuente de la Figura 3.2 (gradiente de carga d/s/xs-SLR). Agregada a `referencias.bib` el 2026-10-01. |
| `kruse2025stevia` | Early Consumption of Stevia rebaudiana Bertoni on Rat Females: Actions on Their Fertility, Progeny, and Behavior | ❌ No disponible | *The Journal of Nutrition* (ahora Elsevier), paywall. El sitio de la revista devuelve un desafío Cloudflare ("Just a moment...") ante requests automáticos — no se intentó sortear. Publicado en 2025, probablemente aún no tenga depósito en PMC. |
| `reichelt2016sucrose` | Daily access to sucrose impairs aspects of spatial memory tasks reliant on pattern separation and neural proliferation in rats | ❌ No disponible | Existe en PMC (`PMC4918785`, PMID correcto `27317199`, ver tabla de arriba), pero la descarga directa del PDF está detrás de una verificación anti-bot de NCBI ("CloudPMC viewer") que no se intentó sortear. Se puede bajar a mano abriendo `https://pmc.ncbi.nlm.nih.gov/articles/PMC4918785/` en un navegador. |
| `rey2024metformin` | Effects of metformin on behavioral alterations produced by chronic sucrose consumption in male rats | ❌ No disponible | *Journal of Neuroendocrinology* (Wiley), paywall. Existe en el repositorio CONICET (`ri.conicet.gov.ar/handle/11336/234011`) pero en **acceso restringido** (botón "Solicitar", requiere pedido formal) — no es una descarga directa. |

## Resto de las entradas (no procesadas todavía)

| Clave | Título |
|---|---|
| fad2026bebidas | Más sobre bebidas azucaradas y enfermedad |
| ennys2019 | 2ª Encuesta Nacional de Nutrición y Salud (ENNyS 2) |
| pichonriviere2023 | Carga de enfermedad e impacto económico del consumo de bebidas azucaradas en Argentina |
| laracastor2025ssb | Burdens of type 2 diabetes and cardiovascular disease attributable to sugar-sweetened beverages in 184 countries |
| mordor2024stevia | Stevia Market — Size, Share & Trends Analysis Report 2024–2029 |
| ie2025latam | Mercado Latinoamericano de Stevia 2025–2034 |
| ie2025argentina | Mercado de Edulcorantes Alimentarios en Argentina 2025–2034 |
| leger2013nor | Object recognition test in mice |
| sharma2009stevia | Effect of Stevia Extract Intervention on Lipid Profile |
| charan2013sample | How to calculate sample size in animal studies? |
| sakimoto2022critical | A critical period for learning and plastic changes at hippocampal CA1 synapses |
| bhatt2025prenatal | Prenatal influences on postnatal neuroplasticity |
| yunker2020nns | Effects of non-nutritive sweeteners on sweet taste processing and neuroendocrine regulation of eating behavior |
| mccarthy2020saccharin | Transgenerational transmission of behavioral phenotypes produced by exposure of male mice to saccharin and nicotine |
| delagarza2022maternal | Maternal sweeteners intake modulates gut microbiota and exacerbates learning and memory processes in adult male offspring |
| tsan2022lcs | Early-life low-calorie sweetener consumption disrupts glucose regulation, sugar-motivated behavior, and memory function in rats |
| pozdnyakova2025stevia | Neuroprotective potential of Stevia rebaudiana and Stachys sieboldii: effects on oxidative stress and locomotor activity in male rats fed a high-fat, high-sucrose diet |
| prata2017glycosides | Glycosides from Stevia rebaudiana Bertoni possess insulin-mimetic and antioxidant activities in rat cardiac fibroblasts |
| noble2021microbial | Gut microbial taxa elevated by dietary sugar disrupt memory function |
| maniam2016sugar | Sugar consumption produces effects similar to early life stress exposure on hippocampal markers of neurogenesis and stress response |
| sanchezhuerta2022sucrose | Sucrose consumption during late adolescence impairs adult neurogenesis of the ventral dentate gyrus without inducing an anxiety-like behavior |
| gharagozloo2021ml | Machine learning in modeling of mouse behavior |
| lukovikov2026cylinder | Automated phenotyping of rodent behavior in the Cylinder Exploration Test using machine learning |
| geros2020tracking | Improved 3D tracking and automated classification of rodents' behavioral activity using depth-sensing cameras |
| jolliffe2016pca | Principal component analysis: a review and recent developments |
| ward1963hierarchical | Hierarchical grouping to optimize an objective function |
| breiman2001rf | Random forests |
| kruse2012lxr | Alterations of LXRα and LXRβ expression in the hypothalamus of glucose-intolerant rats |
| pian2009milk | Milk consumption during adolescence decreases alcohol drinking in adulthood |
| perezgarcia2016malnutrition | Early malnutrition results in long-lasting impairments in pattern-separation for overlapping novel object and novel location memories and reduced hippocampal neurogenesis |

## Método usado (para continuar con las que faltan)

1. Buscar el paper por título exacto + DOI/PMID citado en `referencias.bib`.
2. Verificar que el DOI/PMID citado realmente corresponde a ese título (varias veces no coincidía — ver tabla de discrepancias arriba).
3. Priorizar, en este orden: (a) PDF en el sitio de la revista si es open access sin protección anti-bot, (b) depósito en PMC si existe y es descargable, (c) repositorio institucional del autor (CONICET, universidad), (d) sitio del laboratorio del autor.
4. Si todo está bloqueado por paywall o por protección anti-bot (Cloudflare, "CloudPMC viewer", 403 sistemático) **no se insiste ni se sortea** — se marca "no disponible" con el motivo y, si existe, el link para que Thiago lo baje a mano con su acceso institucional.
5. Todo PDF descargado se verifica releyendo sus metadatos internos (`pdfinfo`: título, DOI, autor) contra la entrada del `.bib`, no solo el nombre de archivo.
