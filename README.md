# TDSP: intención de compra en una tienda en línea

Aplicación de la metodología Team Data Science Process (TDSP) a un problema de clasificación: estimar si una visita a una tienda en línea terminará en compra.

## Situación

Tilde Casa, una tienda en línea ficticia que está por abrir, quiere detectar durante la navegación qué visitas tienen alta probabilidad de compra. A esos visitantes les ofrece un **chat proactivo**: una ventana que aparece por iniciativa de la tienda, atendida por un asesor humano, para resolver dudas antes de que el cliente se vaya. Como la tienda tiene pocos asesores, el modelo decide a quién mostrarle esa ventana. Como no tiene historial propio, el proyecto parte de datos públicos de otra tienda (arranque en frío). El planteamiento completo está en el [acta del proyecto](Docs/Project/Charter.md).

> **Nota:** la tienda, el chat proactivo y el plan de despliegue son un caso hipotético. Su único propósito es demostrar cómo se aplica la metodología TDSP de principio a fin; no corresponden a un negocio ni a un sistema real.

## Resultado

El modelo final es un Random Forest con pesos de clase. En el grupo de prueba obtuvo un F1 de 0.695 y una sensibilidad de 0.728 en la clase "compra", por encima de las metas del acta (0.60 y 0.70). El detalle está en el [reporte del modelo final](Docs/Model/FinalReport.md) y en el [reporte de cierre](<Docs/Project/Exit Report.md>).

## Datos

[Online Shoppers Purchasing Intention Dataset](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset), UCI Machine Learning Repository. Contiene 12,330 sesiones, 17 variables predictoras y la variable objetivo `Revenue`. Licencia CC BY 4.0.

El archivo completo, `online_shoppers_intention.csv`, está en `Sample_Data/Raw/`.

## Metodología

El proyecto sigue el Team Data Science Process (TDSP), una metodología ágil e iterativa que Microsoft publicó en 2016 para equipos de ciencia de datos (Microsoft, s. f.). TDSP combina cuatro elementos: un ciclo de vida del proyecto, roles para cada integrante del equipo, plantillas de documentos y una estructura estándar de carpetas.

El ciclo de vida tiene cinco fases:

1. **Comprensión del negocio:** definir el problema, las métricas de éxito y el equipo.
2. **Adquisición y comprensión de los datos:** cargar, revisar, explorar y limpiar los datos.
3. **Modelado:** preparar las variables, entrenar y evaluar los modelos.
4. **Despliegue:** poner el modelo a disposición de quien lo va a usar.
5. **Aceptación del cliente:** verificar que el resultado cumple lo acordado y entregarlo.

Las fases no son lineales: al final de las fases 2 y 3, el equipo decide si avanza, repite la fase o replantea el objetivo. Los roles del equipo siguen la lista de ocho roles del curso, adaptada a dos integrantes; el reparto está en el [acta del proyecto](Docs/Project/Charter.md).

Microsoft ya no mantiene la documentación de TDSP: su plantilla oficial fue archivada en 2023 y la metodología ya no forma parte de la documentación de Microsoft Learn. La plantilla sigue disponible como referencia, y este proyecto la usa como base.

## Estructura del repositorio

El repositorio sigue la estructura de la [plantilla oficial de TDSP](https://github.com/Azure/Azure-TDSP-ProjectTemplate) publicada por Microsoft.

```text
tdsp-online-shoppers-intention/
├── Code/
│   ├── Data_Acquisition_and_Understanding/   # Notebooks 01 y 02
│   ├── Modeling/                             # Notebooks 03 a 05
│   │   ├── models/                           # Modelo final y metadatos
│   │   └── results/                          # Resultados de validación y prueba
│   └── Deployment/                           # Script de predicción y sesiones de ejemplo
├── Docs/
│   ├── Project/                              # Acta, arquitectura, decisiones y reporte de cierre
│   ├── Data_Dictionaries/                    # Descripción de cada variable
│   ├── Data_Report/                          # Definición de datos y reporte de datos
│   └── Model/                                # Reportes de los modelos
├── Sample_Data/
│   ├── Raw/                                  # Datos originales (solo lectura)
│   ├── Processed/                            # Grupos de entrenamiento y prueba
│   └── For_Modeling/                         # Datos limpios para modelar
├── requirements.txt
└── README.md
```

### Diferencias con la plantilla oficial

- **Datos completos en `Sample_Data/`.** La plantilla indica que esta carpeta debe guardar solo muestras pequeñas, porque en un proyecto real los datos completos viven en un almacenamiento externo. En este proyecto la base completa pesa alrededor de 1 MB y es pública, así que se incluye entera para que cualquiera pueda reproducir los resultados.
- **Ubicación de modelos, resultados y figuras.** La plantilla no define carpetas para ellos. Los modelos y resultados se guardan en `Code/Modeling/`, y cada figura junto al reporte que la usa, en una subcarpeta `figures/`.
- **Nombres de archivo.** Los documentos conservan los nombres de la plantilla, con una excepción: `Data Defintion.md` aparece en la plantilla con una errata, y aquí se escribe `Data Definition.md`. La arquitectura de la solución está en Markdown (`System Architecture.md`) en lugar de Word.
- **Idioma.** Los documentos están en español; las carpetas conservan sus nombres originales en inglés.

## Documentos por fase

| Fase TDSP | Documentos |
| --- | --- |
| 1. Comprensión del negocio | [Acta del proyecto](Docs/Project/Charter.md) |
| 2. Adquisición y comprensión de los datos | [Diccionario de datos](Docs/Data_Dictionaries/Raw-Data-Dictionary.md), [definición de datos](<Docs/Data_Report/Data Definition.md>), [reporte de datos](Docs/Data_Report/DataSummaryReport.md) |
| 3. Modelado | [Modelos base](<Docs/Model/Baseline/Baseline Models.md>), [modelos rebalanceados](<Docs/Model/Model 1/Model Report.md>), [modelo final](Docs/Model/FinalReport.md) |
| 4. Despliegue | [Arquitectura de la solución](<Docs/Project/System Architecture.md>) |
| 5. Aceptación del cliente | [Reporte de cierre](<Docs/Project/Exit Report.md>) |

Las decisiones técnicas de todas las fases están en el [registro de decisiones](<Docs/Project/Decision Log.md>).

## Ejecución

```bash
pip install -r requirements.txt
```

Los notebooks se ejecutan en este orden, cada uno desde su propia carpeta:

| Orden | Notebook | Carpeta |
| --- | --- | --- |
| 1 | `01_data_acquisition.ipynb` | `Code/Data_Acquisition_and_Understanding/` |
| 2 | `02_data_understanding.ipynb` | `Code/Data_Acquisition_and_Understanding/` |
| 3 | `03_modeling_unbalanced.ipynb` | `Code/Modeling/` |
| 4 | `04_modeling_balanced.ipynb` | `Code/Modeling/` |
| 5 | `05_model_evaluation.ipynb` | `Code/Modeling/` |

Cada notebook con procesos aleatorios define su propia semilla (`SEED = 1`). Los notebooks 03 y 04 tardan varios minutos por la validación cruzada.

Para probar el modelo con las sesiones de ejemplo:

```bash
cd Code/Deployment
python predict.py
```

## Autores

| Integrante | Perfil de GitHub | Roles |
| --- | --- | --- |
| Diego Morales Ripalda | [@Diego-MR24](https://github.com/Diego-MR24) | Jefe de equipo, gestor de proyecto, ingeniero de datos, ingeniero de aprendizaje automático |
| Mariano de Jesús Ruiz Madrid | [@RMadridMariano25](https://github.com/RMadridMariano25) | Propietario de producto, experto en procesos, analista de datos, científico de datos |

## Uso de inteligencia artificial

El código y la redacción de los documentos se generaron con apoyo de un asistente de inteligencia artificial. El equipo definió el planteamiento, tomó las decisiones del proyecto y revisó y validó todo el contenido.

## Referencias

Microsoft. (s. f.). *Azure-TDSP-ProjectTemplate* [Repositorio]. GitHub. <https://github.com/Azure/Azure-TDSP-ProjectTemplate>

Sakar, C. O., Polat, S. O., Katircioglu, M. y Kastro, Y. (2019). Real-time prediction of online shoppers' purchasing intention using multilayer perceptron and LSTM recurrent neural networks. *Neural Computing and Applications*, *31*(10), 6893-6908. <https://doi.org/10.1007/s00521-018-3523-0>

Sakar, C. O. y Kastro, Y. (2018). *Online shoppers purchasing intention dataset* [Conjunto de datos]. UCI Machine Learning Repository. <https://doi.org/10.24432/C5F88Q>
