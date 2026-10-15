# Diccionario de datos

Descripción de las 18 columnas de `online_shoppers_intention.csv`, basada en la ficha del UCI Machine Learning Repository (Sakar y Kastro, 2018). Cada fila del archivo es una sesión de navegación de un usuario distinto en un sitio de comercio electrónico, durante un periodo de un año.

## Navegación por tipo de página

| Variable | Tipo | Descripción |
| --- | --- | --- |
| `Administrative` | Entero | Número de páginas administrativas visitadas (cuenta, contacto, ayuda) |
| `Administrative_Duration` | Decimal | Tiempo total en páginas administrativas, en segundos |
| `Informational` | Entero | Número de páginas informativas visitadas (sobre la tienda, políticas) |
| `Informational_Duration` | Decimal | Tiempo total en páginas informativas, en segundos |
| `ProductRelated` | Entero | Número de páginas de productos visitadas |
| `ProductRelated_Duration` | Decimal | Tiempo total en páginas de productos, en segundos |

## Métricas de Google Analytics

| Variable | Tipo | Descripción |
| --- | --- | --- |
| `BounceRates` | Decimal | Tasa de rebote promedio de las páginas visitadas: proporción de visitantes que entraron por esa página y salieron sin hacer nada más |
| `ExitRates` | Decimal | Tasa de salida promedio de las páginas visitadas: proporción de vistas de esa página que fueron la última de la sesión |
| `PageValues` | Decimal | Valor promedio de las páginas visitadas, calculado a partir de las páginas que preceden a una compra |

## Contexto de la visita

| Variable | Tipo | Descripción |
| --- | --- | --- |
| `SpecialDay` | Decimal | Cercanía a una fecha especial, como San Valentín o el Día de las Madres. Vale 0 lejos de la fecha y llega a 1 en el punto de mayor cercanía |
| `Month` | Texto | Mes de la visita, abreviado en inglés. Junio aparece como `June` |
| `Weekend` | Booleano | Indica si la visita ocurrió en fin de semana |
| `VisitorType` | Texto | `New_Visitor` (visitante nuevo), `Returning_Visitor` (recurrente) u `Other` (sin descripción en la ficha) |

## Datos técnicos

| Variable | Tipo | Descripción |
| --- | --- | --- |
| `OperatingSystems` | Entero (código) | Sistema operativo del visitante |
| `Browser` | Entero (código) | Navegador del visitante |
| `Region` | Entero (código) | Región desde donde se hizo la visita |
| `TrafficType` | Entero (código) | Origen del tráfico (por ejemplo, anuncio, buscador o enlace directo) |

Los cuatro códigos técnicos no tienen significado publicado: se sabe que dos valores distintos son categorías distintas, pero no a qué corresponde cada número. Por eso se tratan como variables categóricas, no como números.

## Variable objetivo

| Variable | Tipo | Descripción |
| --- | --- | --- |
| `Revenue` | Booleano | Indica si la sesión terminó en compra |

## Referencia

Sakar, C. O. y Kastro, Y. (2018). *Online shoppers purchasing intention dataset* [Conjunto de datos]. UCI Machine Learning Repository. <https://doi.org/10.24432/C5F88Q>
