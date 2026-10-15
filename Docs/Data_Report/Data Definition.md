# Definición de datos y variables

Punto central que enlaza la base original, los datos procesados y los conjuntos de variables del proyecto. El detalle de la exploración está en el [reporte de datos](DataSummaryReport.md) y la descripción de cada columna en el [diccionario de datos](../Data_Dictionaries/Raw-Data-Dictionary.md).

## Datos originales

| Nombre | Ubicación original | Ubicación en el proyecto | Script | Reporte |
| --- | --- | --- | --- | --- |
| Online Shoppers Purchasing Intention | [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset) | `Sample_Data/Raw/online_shoppers_intention.csv` | Descarga manual | [Reporte de datos](DataSummaryReport.md) |

La base contiene 12,330 sesiones y 18 columnas, sin valores faltantes. Su licencia es CC BY 4.0.

## Datos procesados

| Nombre | Entrada | Script | Descripción |
| --- | --- | --- | --- |
| `train.csv`, `test.csv` | Base original | [`01_data_acquisition.ipynb`](../../Code/Data_Acquisition_and_Understanding/01_data_acquisition.ipynb) | División 80/20 estratificada por `Revenue`, con la columna `row_id` agregada |
| `train_clean.csv`, `test_clean.csv` | `train.csv`, `test.csv` | [`02_data_understanding.ipynb`](../../Code/Data_Acquisition_and_Understanding/02_data_understanding.ipynb) | Datos limpios: `June` unificado como `Jun`; `Weekend` y `Revenue` como 1 y 0 |

Los grupos de entrenamiento y prueba se separan antes de cualquier limpieza, para que ninguna decisión sobre los datos dependa del grupo de prueba.

## Conjuntos de variables

| Nombre | Variables | Uso |
| --- | --- | --- |
| `con_PageValues` | Las 17 variables predictoras | Conjunto principal |
| `sin_PageValues` | Las 17 variables menos `PageValues` | Comparación para medir la dependencia del modelo en esa variable |

En ambos conjuntos, las variables numéricas entran sin transformar, porque los modelos de árboles no dependen de la escala. `Month`, `VisitorType`, `OperatingSystems`, `Browser`, `Region` y `TrafficType` se codifican en one-hot dentro del pipeline de cada modelo; los códigos con menos de 30 sesiones en entrenamiento se agrupan en una sola columna.
