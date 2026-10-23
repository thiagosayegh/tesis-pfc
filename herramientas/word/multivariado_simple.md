---
title: "El análisis multivariado de la SLR, explicado simple"
author: "Thiago Sayegh"
date: "23 de octubre de 2026"
lang: es-AR
---

## La idea

El ANOVA mira las medidas de a una. Acá miramos **todas las medidas de cada animal juntas**, para ver si los grupos se diferencian en su "perfil" de conducta. Se hizo solo con la SLR porque es la única prueba con los datos identificados por animal.

Para cada uno de los 117 animales se usaron 5 medidas:

| Medida | Qué es |
| --- | --- |
| A1, A2, A3 | Tiempo explorando cada objeto en el día 1 |
| Exploración día 2 | Tiempo explorando los objetos en el día 2 |
| DI | Cuánto prefirió la posición nueva (el mismo DI de Prism) |

Se hicieron tres pasos.

## Paso 1. PCA: resumir las 5 medidas en 2

El PCA es como hacer un resumen: busca qué medidas van juntas y las reemplaza por pocas "notas" nuevas. Con las 5 medidas salieron **dos notas por animal**:

- **CP1 = cuánto explora** (junta los tiempos del día 1 y del día 2; resume el 50 % de la información).
- **CP2 = cuánto discrimina** (es casi solo el DI; resume otro 20 %).

Que salgan separadas quiere decir que **explorar mucho no implica discriminar bien**: son dos cosas distintas.

![](Fig5_ML_pca.png){width=16cm}

*Cómo leerla. A: cada punto chico es un animal (círculo: juvenil; triángulo: adulto) y los símbolos grandes son el promedio de cada grupo. Más a la derecha = explora más; más arriba = discrimina mejor. B: qué medidas forman cada nota (barra larga = pesa mucho).*

Lo que muestra:

- **Sacarosa (rojo)**: queda **abajo** en las dos edades, es decir, discrimina peor. Es lo mismo que dio el ANOVA del DI.
- **Stevia (verde)**: queda **a la altura del control** en discriminación. Se separa del control hacia la derecha, porque explora más (sobre todo los adultos).
- Los juveniles con sacarosa exploraron mucho y aun así discriminaron mal: su problema es de memoria, no de falta de exploración.

## Paso 2. Clustering: ¿los animales se agrupan solos?

Al método no se le dice de qué grupo es cada animal; solo junta a los que se parecen. **Los grupos que armó no coinciden con los grupos experimentales**: los animales de distintos tratamientos quedan mezclados. O sea, ningún tratamiento genera un perfil de conducta claramente aparte.

## Paso 3. Random Forest: ¿se puede adivinar el grupo?

Le mostramos al programa muchos animales con su grupo, para que aprenda. Después le damos animales que nunca vio, **sin decirle el grupo**, y tiene que adivinarlo. Se compara con lo que acertaría tirando una moneda (el azar).

| Pregunta | Acertó | Por azar |
| --- | --- | --- |
| ¿Control o sacarosa? | 67 % | 50 % |
| ¿Control o stevia? | 67 % | 50 % |
| ¿Cuál de los 6 grupos? | 30 % | 17 % |

Las tres diferencias con el azar son significativas.

![](Fig5_ML_rf.png){width=16cm}

*Cómo leerla. A: cada fila es el grupo real y cada columna, lo que dijo el programa. Los números de la diagonal son los aciertos (C: control; S: sacarosa; St: stevia). B: qué medida le sirvió más para adivinar (barra más larga = más útil).*

Lo que muestra:

- La medida que más le sirvió fue el **DI**, otra vez la memoria.
- Los que mejor reconoce son los juveniles con sacarosa (54 %).
- Los juveniles con stevia son los que peor reconoce (6 %): los confunde con todos los demás grupos. Por eso decimos que son **los que menos se diferencian** del resto.

## En pocas palabras

1. **Sacarosa**: se diferencia del control porque discrimina peor (memoria).
2. **Stevia**: se diferencia del control porque explora más, no porque discrimine peor.
3. **Ningún grupo forma un perfil aparte**: hay diferencias, pero los grupos se superponen bastante. Es lo esperable para un efecto nutricional, que es más sutil que el de un fármaco o un cambio genético.
