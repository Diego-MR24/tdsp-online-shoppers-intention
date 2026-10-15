# Modelos base: ejecución sin balancear

Primera ejecución del modelado, con la proporción original de clases. Su función es medir qué tan viable es el problema antes de compensar el desbalance. Los cálculos están en [`03_modeling_unbalanced.ipynb`](../../../Code/Modeling/03_modeling_unbalanced.ipynb).

## Enfoque

- **Variable objetivo:** `Revenue`, 1 si la sesión terminó en compra.
- **Entradas:** las 17 variables predictoras de `train_clean.csv`, en dos versiones: con y sin `PageValues`.
- **Tipo de modelo:** clasificación binaria.

## Modelos y parámetros

| Modelo | Descripción | Parámetros probados |
| --- | --- | --- |
| Referencia | Siempre predice "no compra" | Ninguno |
| Árbol de decisión | Un solo árbol de reglas | Profundidad máxima: 3, 5, 8, sin límite. Mínimo de sesiones por hoja: 1, 5, 20 |
| Random Forest | 300 árboles entrenados con muestras distintas y votación | Profundidad máxima: 10, 20, sin límite. Mínimo de sesiones por hoja: 1, 5 |

Cada combinación se evaluó con validación cruzada estratificada de cinco pliegues (`SEED = 1`), y se eligieron los parámetros con mayor F1 de la clase "compra".

## Resultados

| Modelo | Variables | F1 | Sensibilidad | Precisión | Precisión promedio |
| --- | --- | --- | --- | --- | --- |
| Referencia | Todas | 0.000 | 0.000 | 0.000 | 0.155 |
| Árbol de decisión | Con `PageValues` | 0.633 | 0.581 | 0.697 | 0.675 |
| Random Forest | Con `PageValues` | 0.622 | 0.526 | 0.761 | 0.736 |
| Árbol de decisión | Sin `PageValues` | 0.293 | 0.310 | 0.277 | 0.194 |
| Random Forest | Sin `PageValues` | 0.121 | 0.069 | 0.503 | 0.359 |

La **precisión promedio** resume la precisión en todos los umbrales posibles; un modelo que adivina al azar obtiene un valor igual a la proporción de compras (0.155).

## Interpretación

- **El problema es viable.** Con `PageValues`, ambos modelos superan con claridad a la referencia.
- **La sensibilidad es baja.** Sin compensar el desbalance, los modelos detectan entre el 53 % y el 58 % de las compras. No alcanzan la meta de 0.70 del acta con el umbral estándar de 0.5.
- **Sin `PageValues`, el desempeño se desploma.** El Random Forest sin esa variable detecta apenas el 7 % de las compras, porque con tan pocas compras en los datos le resulta más seguro responder "no compra".

## Decisión de control

Continuar con una segunda ejecución que compense el desbalance de clases, manteniendo la comparación con y sin `PageValues`.
