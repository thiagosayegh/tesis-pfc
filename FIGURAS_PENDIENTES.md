# Figuras pendientes de corregir en GraphPad Prism

Estas figuras están exportadas desde Prism como PDF/PNG y no se pueden editar desde el
código fuente (`.tex`); hay que corregirlas en Prism y volver a exportarlas con el mismo
nombre de archivo en `figuras/`. Los números de figura son los actuales (después de las
Fases 1–5 de la revisión de jurado); pueden correrse si se agregan o quitan figuras más
adelante.

## Paleta única (aplicar a todas las figuras de grupos)

Las figuras de consumo (5.1, 5.2, 5.4) ya usan una paleta por color: **azul = control,
rojo = sacarosa, verde = stevia**. Las figuras de NOR (5.6) ya están en color (actualizadas en Prism). Las de SLR por barras (5.9 y 5.10) ya están en color para s-SLR (actualizadas en Prism); falta d-SLR (DI y tasa), que sigue en grises con su propia leyenda gris. Unificar todo a la paleta de
color ya establecida en 5.1/5.2/5.4 (azul/rojo/verde), de modo que el color de un grupo
sea el mismo en toda la tesis. Los captions del `.tex` ya se actualizaron para describir
esta paleta (Fig. 5.5, 5.8 y A.1); una vez corregidas las figuras en Prism, van a coincidir.

## Fig. 5.1 — Consumo de líquidos, grupo juvenil y adulto (`Fig5_consumo_liquidos_juvenil.pdf`, `Fig5_consumo_liquidos_adulto.pdf`)
- [ ] Título "JUVENILE group" / "ADULT group" → "Grupo juvenil" / "Grupo adulto" (o quitar el título, ya que el panel se identifica en el caption del `.tex`).
- [ ] Eje Y "Liquid consumption (mL/g BW/day)" → "Consumo de líquido (mL/g de peso corporal/día)".
- [ ] Leyenda: "Control juvenil", "Stevia water", "Stevia stevia", "SUC water", "SUC sucrose" → "Control", "Stevia – agua", "Stevia – stevia", "Sacarosa – agua", "Sacarosa – sacarosa" (mismos nombres que la Tabla 5.1).
- [ ] Eje X "PD" puede dejarse así (ya se usa "PD" como abreviatura en toda la tesis).

## Fig. 5.2 — Consumo de líquidos promediado (`Fig5_consumo_liquidos_promedio.pdf`)
- [ ] Título "consumption averaged across the experimental period" → "Consumo promediado durante el período experimental" (o quitarlo).
- [ ] Eje Y "Liquid consumption (mL/g BW/day)" → "Consumo de líquido (mL/g de peso corporal/día)".
- [ ] Eje X: "Juvenile" (en inglés) / "Adulto" (en español) están mezclados → unificar a "Juvenil" / "Adulto".
- [ ] Leyenda: "Control", "SUC sucrose", "Stevia stevia", "SUC water", "Stevia water" → "Control", "Sacarosa – sacarosa", "Stevia – stevia", "Sacarosa – agua", "Stevia – agua".

## Fig. 5.3 — Consumo de agua durante el lavado (`Fig5_agua_lavado.pdf`)
- [ ] Eje Y "% over control" → "% del control".
- [ ] Eje X "days post-treatment" → "días post-tratamiento".
- [ ] Leyenda: "Juvenil SUC" / "Juvenil stevia" (español) mezclado con "Adult SUC" / "Adult stevia" (inglés) → unificar a "Juvenil – Sacarosa", "Juvenil – Stevia", "Adulto – Sacarosa", "Adulto – Stevia".

## Fig. 5.4 — Consumo de alimento, grupo juvenil (`Fig5_chow_juvenil.pdf`)
- [ ] Título "chow JUVENILE" → "Alimento, grupo juvenil".
- [ ] Eje Y "Chow (g/g BW/day)" → "Alimento (g/g de peso corporal/día)".
- [ ] Leyenda: "Control", "SUC", "Stevia" → "Control", "Sacarosa", "Stevia".
- [ ] Falta también el gráfico equivalente del grupo adulto (`Fig5_chow_adulto.pdf` o similar), pendiente en el texto (§5.1.3).

## Fig. 5.6 — Tasa de exploración, prueba NOR (`Fig5_NOR_T2.pdf`, `Fig5_NOR_T3.pdf`, `Fig5_NOR_T4.pdf`)
- [x] Título "T2/T3/T4 Two-way ANOVA" eliminado.
- [x] Eje Y "Tasa de exploración" (sin "(%)").
- [x] Paleta azul/rojo/verde.
- [x] Leyenda de colores: se usa la imagen común `figuras/Fig5_leyenda_grupos.png` (Control / 10% Sacarosa / 4% Stevia, tomada de la presentación de OF), insertada bajo los tres paneles en el `.tex`.
- [ ] Eje X "Juvenile" / "Adult" (T3 y T4) → "Juvenil" / "Adulto" (T2 ya está: "Juvenil" / "Adultos"). Decisión de Thiago: se deja por ahora.

## Fig. 5.9 — Índice de discriminación (DI), prueba SLR (`Fig5_DI_SLR_d.pdf`, `Fig5_DI_SLR_s.pdf`)
- [x] s-SLR (`Fig5_DI_SLR_s.pdf`): actualizado en Prism (color, eje "Índice de discriminación", corchetes solo significativos, barras pegadas).
- [ ] **d-SLR (`Fig5_DI_SLR_d.pdf`)**: pendiente. Hacer igual que s-SLR: agrupar por edad (Juvenil/Adulto, tres barras pegadas: Spacing "Between adjacent data" 0 %), colores azul/rojo/verde (0,0,255 / 255,0,0 / 0,192,0), eje Y "Índice de discriminación (DI)" (no "Tasa de discriminación"), sin título ni "XTitle", solo corchetes significativos (los de la Tabla 5.4).
- [ ] Una vez recoloreadas las dos: agregar la leyenda común `Fig5_leyenda_grupos.png` bajo la figura en el `.tex` y borrar la leyenda propia de Prism.

## Fig. 5.10 — Tasa de exploración, prueba SLR (`Fig5_tasa_SLR_d.pdf`, `Fig5_tasa_SLR_s.pdf`)
- [x] s-SLR (`Fig5_tasa_SLR_s.pdf`): actualizado en Prism.
- [ ] **d-SLR (`Fig5_tasa_SLR_d.pdf`)**: pendiente, mismos puntos que el DI (eje Y "Tasa de exploración", azar 0,5).
- [ ] Agregar la leyenda común bajo la figura una vez recoloreadas las dos.

## Fig. 3.2 — Gradiente de carga SLR
- [x] Ya reemplazada por una versión propia (`figuras/Fig3_SLR_carga_cognitiva.png`, generada con matplotlib, en español, sin BioRender ni la configuración xs-SLR). Sin pendientes.

## Fig. 4.4 — Objetos utilizados en la prueba SLR
- [ ] Reemplazar por una foto propia de los objetos reales del laboratorio (tazas con dibujos y ranas de juguete), en vez de la imagen de stock actual.

## Otras figuras pendientes (sin datos/archivo todavía, no son correcciones de Prism)
- Fig. 3.1 (cascada neurogénica): falta el esquema.
- Fig. 4.2 (aparato de OF): falta la foto.
- Fig. 4.5 (confocal giro dentado): faltan las fotomicrografías.
- Fig. 5.7 (exploración SLR día 1 vs. día 2): falta el archivo y la leyenda.
