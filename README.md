# PFC — Thiago Sayegh (ITBA · IByME-CONICET)

Fuente LaTeX de la tesina *Efectos neurobiológicos a largo plazo de la exposición a Stevia rebaudiana durante la etapa juvenil y la adultez*.

## Opción A — Local (recomendada para trabajar con Claude Code)
1. Instalar TeX: **MacTeX** (macOS) o **TeX Live** completo (Windows/Linux). Incluye latexmk y biber.
2. Descomprimir esta carpeta, idealmente en un lugar sincronizado (Drive/Dropbox) o en un repo git:
   ```
   cd tesis-pfc
   git init && git add . && git commit -m "Migración desde Google Docs"
   ```
3. Compilar: `latexmk` → el PDF queda en `build/main.pdf`.
4. Abrir la carpeta en Claude Code (app de escritorio → Code, o `claude` en la terminal). `CLAUDE.md` le da todo el contexto.
5. Editor opcional: VS Code + extensión *LaTeX Workshop* (compila al guardar y muestra el PDF al lado).

## Opción B — Overleaf
New Project → Upload Project → subir el .zip. Compilador: pdfLaTeX (biber se detecta solo). En Menu → Main document: `main.tex`.

## Qué falta poner a mano
Copiar a `figuras/` (desde la carpeta TESIS de Drive o exportando de Prism):
- `Fig4_esquema_SLR.png`
- `Fig4_objetos_SLR.jpg` (foto de tazas y ranas)
- `Fig5_estimacion_Tukey_SLR.png`
- `Fig5_DI_SLR.pdf` y `Fig5_exploracion_SLR.pdf` (cuando estén)

Y a `logos/`: `logo_itba.png` (opcionales: `logo_ibyme.png`, `logo_conicet.png`).

Mientras falten, el PDF muestra un recuadro con el nombre esperado.

## Marcadores
`[PENDIENTE]` rojo · `[CONFIRMAR]` naranja · `[REVISAR]` violeta.
Para listarlos: `grep -rn "pendiente\|confirmar\|revisar" capitulos/`
