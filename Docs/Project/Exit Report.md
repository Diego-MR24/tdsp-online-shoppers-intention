# Reporte de cierre

| Campo | Detalle |
| --- | --- |
| Proyecto | Predicción de intención de compra en una tienda en línea |
| Cliente | Tilde Casa (tienda ficticia) |
| Metodología | Team Data Science Process (TDSP) |
| Equipo | Integrante 1 e Integrante 2, con los roles del [acta del proyecto](Charter.md) |

## Resumen

El proyecto entregó un modelo que estima, a partir del comportamiento de un visitante, la probabilidad de que su visita termine en compra. En el grupo de prueba, el modelo detectó el 73 % de las compras, y dos de cada tres de sus alertas correspondieron a visitantes que efectivamente compraron. Cumple cuatro de los cinco criterios de aceptación definidos al inicio; el quinto, la reproducibilidad en otra computadora, queda pendiente de una última verificación.

## Dominio del negocio

Comercio electrónico. La tienda hipotética vende artículos para el hogar y regalos en México y está por iniciar operaciones.

## Problema del negocio

La mayoría de los visitantes de una tienda en línea se van sin comprar. La tienda quiere detectar durante la visita a quienes probablemente van a comprar, para ofrecerles un chat proactivo atendido por un asesor humano y resolver sus dudas antes de que se vayan. Como tiene pocos asesores, no puede ofrecer el chat a todos. Como no tiene historial propio, el modelo parte de datos públicos de otra tienda.

Este caso es hipotético: su propósito es demostrar la aplicación de TDSP de principio a fin.

## Procesamiento de datos

La base [Online Shoppers Purchasing Intention](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset) contiene 12,330 sesiones y 18 columnas, sin valores faltantes. Los datos se dividieron 80/20, estratificados por la variable objetivo, antes de cualquier limpieza. La limpieza solo unificó el formato de junio y convirtió las variables booleanas a 1 y 0; las filas repetidas y las categorías poco frecuentes se conservaron. El detalle está en el [reporte de datos](../Data_Report/DataSummaryReport.md).

## Modelado y validación

El modelado comparó un árbol de decisión y un Random Forest en dos ejecuciones, sin balancear y con clases rebalanceadas, cada una con y sin `PageValues`. El modelo elegido, un Random Forest con pesos de clase, obtuvo el mayor F1 en validación cruzada (0.671). Su umbral de decisión se ajustó a 0.513 con probabilidades fuera de pliegue. El detalle está en el [reporte del modelo final](../Model/FinalReport.md).

## Verificación de los criterios de aceptación

| Criterio | Meta | Resultado | ¿Cumple? |
| --- | --- | --- | --- |
| C1. F1 de la clase "compra" | Al menos 0.60 | 0.695 | Sí |
| C2. Sensibilidad de la clase "compra" | Al menos 0.70 | 0.728 | Sí |
| C3. Mejora sobre el modelo de referencia | F1 mayor que 0.000 | 0.695 | Sí |
| C4. Script de predicción | Devuelve una probabilidad por sesión de ejemplo | Tres sesiones procesadas | Sí |
| C5. Reproducibilidad | Mismos resultados siguiendo el README | Ejecución desde cero con resultados idénticos; falta repetirla en la computadora del integrante 2 | Parcial |

**Decisión del propietario de producto:** solución aceptada, con la condición de completar la verificación del criterio C5 y con las limitaciones descritas más adelante.

## Arquitectura de la solución

Implementado: el script de predicción y el modelo guardado con sus metadatos. Propuesto: la API de predicción, la base de sesiones y el reentrenamiento periódico con reglas de reemplazo. El detalle está en la [arquitectura de la solución](<System Architecture.md>).

## Beneficios

### Beneficio para el cliente

Con el umbral elegido, 2 de cada 3 chats proactivos llegarían a un visitante con intención de compra. El modelo permite que un equipo pequeño de asesores atienda a la mayoría de los compradores potenciales sin interrumpir a quienes solo están mirando.

### Beneficio para el equipo

Experiencia con el ciclo completo de TDSP, desde la definición del problema hasta el plan de despliegue, y con el manejo de clases desbalanceadas.

## Aprendizajes

### Ejecución del proyecto

Fijar las métricas y las metas en el acta, antes de entrenar, evitó ajustar los criterios a los resultados. El registro de decisiones facilitó explicar cada paso.

### Ciencia de datos

- El balanceo de clases subió la sensibilidad de alrededor de 0.55 a más de 0.70.
- Aplicar el balanceo y ajustar el umbral sin tocar el grupo de prueba fue clave para que la evaluación final fuera confiable.

### Dominio

`PageValues` concentra el 35 % de la importancia del modelo. Sin ella, el F1 cae de 0.695 a 0.419.

### Retos particulares

Los datos son de otra tienda, de otro país, y describen sesiones terminadas, mientras que el despliegue predice durante la visita. Además, enero y abril no aparecen en los datos.

## Limitaciones

- El modelo depende de que la tienda tenga Google Analytics configurado con el valor de sus transacciones, para calcular `PageValues`.
- Las fechas especiales de la tienda original pueden no coincidir con las de México.
- El modelo no conoce enero ni abril.
- El desempeño real en Tilde Casa solo se conocerá con sus propios datos.

## Siguientes pasos

| Acción | Responsable |
| --- | --- |
| Configurar Google Analytics con el valor de las transacciones | Equipo técnico de la tienda |
| Guardar sesiones propias, incluido su estado a mitad de la visita | Ingeniero de datos |
| Entrenar el primer modelo propio al reunir 1,000 sesiones con compra | Científico de datos |
| Revisión mensual de las métricas del modelo en uso | Propietario de producto |

## Enlaces

- Repositorio: `tdsp-online-shoppers-intention`
- Datos: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset)
