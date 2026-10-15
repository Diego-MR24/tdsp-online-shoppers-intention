# Reporte del modelo: ejecución con clases rebalanceadas

Segunda ejecución del modelado, con dos formas de compensar el desbalance de clases. Los cálculos están en [`04_modeling_balanced.ipynb`](../../../Code/Modeling/04_modeling_balanced.ipynb).

## Enfoque

Las mismas variables, conjuntos y validación cruzada que la [primera ejecución](<../Baseline/Baseline Models.md>), con dos estrategias de balanceo:

- **Sobremuestreo** (`RandomOverSampler`): duplica sesiones con compra elegidas al azar hasta igualar ambas clases. Se aplica dentro de cada pliegue de entrenamiento, nunca a los datos con que se califica el modelo.
- **Pesos de clase** (`class_weight="balanced"`): no modifica los datos; hace que cada error en la clase "compra" cuente más durante el entrenamiento.

## Modelos y parámetros

| Modelo | Estrategia | Parámetros elegidos (con `PageValues`) |
| --- | --- | --- |
| Árbol de decisión | Sobremuestreo | Profundidad máxima 3, mínimo 1 sesión por hoja |
| Random Forest | Sobremuestreo | Profundidad máxima 20, mínimo 5 sesiones por hoja |
| Random Forest | Pesos de clase | Sin límite de profundidad, mínimo 1 sesión por hoja |

## Resultados

| Modelo | Variables | F1 | Sensibilidad | Precisión | Precisión promedio |
| --- | --- | --- | --- | --- | --- |
| Random Forest con pesos de clase | Con `PageValues` | 0.671 | 0.718 | 0.630 | 0.723 |
| Random Forest con sobremuestreo | Con `PageValues` | 0.669 | 0.787 | 0.582 | 0.727 |
| Árbol con sobremuestreo | Con `PageValues` | 0.640 | 0.858 | 0.510 | 0.641 |
| Random Forest con pesos de clase | Sin `PageValues` | 0.430 | 0.636 | 0.325 | 0.379 |
| Random Forest con sobremuestreo | Sin `PageValues` | 0.426 | 0.517 | 0.362 | 0.375 |
| Árbol con sobremuestreo | Sin `PageValues` | 0.380 | 0.750 | 0.255 | 0.322 |

## Interpretación

- **El balanceo mejora la sensibilidad.** Frente a la primera ejecución, la sensibilidad sube de alrededor de 0.55 a valores entre 0.72 y 0.86, a cambio de una precisión menor. El F1 mejora de 0.63 a 0.67.
- **Las dos estrategias empatan en F1.** La diferencia entre pesos de clase (0.671) y sobremuestreo (0.669) es menor que la variación entre pliegues, así que no es concluyente.
- **El árbol simple tiene la mayor sensibilidad** (0.86), pero con una precisión de 0.51: casi la mitad de sus alertas serían visitantes que no iban a comprar.
- **Sin `PageValues`, el balanceo ayuda pero no alcanza.** El F1 sube de 0.29 a 0.43, todavía lejos de la meta de 0.60.

## Decisión de control

Avanzar a la selección del modelo final, con el criterio fijado de antemano: la configuración con mayor F1 en validación cruzada.
