# Acta del proyecto

> **Estado:** aprobada. El calendario es un plan de referencia, porque el proyecto es un caso de práctica.

| Campo | Detalle |
| --- | --- |
| Proyecto | Predicción de intención de compra en una tienda en línea |
| Metodología | Team Data Science Process (TDSP) |
| Fase | 1. Comprensión del negocio |
| Versión | 1.0 |

## 1. Situación del negocio

Tilde Casa es una tienda en línea mexicana, ficticia, que vende artículos para el hogar y regalos. Su nombre juega con la tilde: el detalle pequeño que cambia una palabra, como los objetos que cambian una casa. La tienda está por iniciar operaciones y quiere aumentar la proporción de visitas que terminan en compra desde el primer día.

> **Caso de demostración:** la tienda, su forma de usar el modelo y el plan de despliegue son hipotéticos. Su propósito es demostrar la aplicación de TDSP de principio a fin con un caso que tenga sentido de negocio.

La mayoría de las personas que entran a una tienda en línea se van sin comprar. La tienda busca reconocer, mientras el cliente todavía navega, qué visitas tienen alta probabilidad de terminar en compra, para ofrecerles ayuda en el momento oportuno.

Una tienda nueva no tiene historial propio de visitas. Por eso el proyecto usa como punto de partida los datos públicos de otra tienda en línea. A esta estrategia se le conoce como **arranque en frío**: el primer modelo sirve de referencia mientras la tienda junta sus propios datos, y más adelante se reemplaza por un modelo entrenado con ellos.

## 2. Objetivo

Construir un modelo que, a partir del comportamiento de un visitante durante su sesión, estime la probabilidad de que esa sesión termine en compra.

**Pregunta de negocio:** ¿esta visita va a terminar en compra?

**Tipo de problema:** clasificación binaria. La variable objetivo es `Revenue`, con dos valores: compró (`True`) o no compró (`False`).

**Uso del resultado:** cuando el modelo detecta una visita con alta probabilidad de compra, la tienda le ofrece un **chat proactivo**: una ventana que aparece en la página por iniciativa de la tienda, sin que el cliente la pida, donde un asesor humano ofrece resolver dudas sobre productos, envíos o pagos.

**Por qué no abrir el chat a todos:** la tienda tiene un equipo pequeño de asesores, y una ventana no solicitada interrumpe a quien solo está mirando. El modelo concentra la atención de los asesores en los visitantes con mayor intención de compra. Usar modelos predictivos para decidir a quién invitar al chat es una práctica recomendada en la industria por la capacidad limitada de los asesores (Forrester, s. f.), y hay evidencia de que el chat con una persona aumenta la proporción de visitantes que compran (Sun et al., 2021).

Si el chat lo atendiera un bot automático, el argumento de la capacidad limitada se debilita, porque un bot puede atender a todos a la vez. Un chatbot disponible para todos, en modo pasivo, queda como posible complemento futuro.

## 3. Alcance

### 3.1 Incluye

- Exploración y reporte de calidad de los datos.
- Entrenamiento y comparación de modelos en dos ejecuciones: con los datos tal como vienen y con las clases rebalanceadas.
- Selección del modelo final con base en los criterios de la sección 6.
- Un script de predicción que recibe los datos de una sesión y devuelve la probabilidad de compra.
- Un plan de despliegue en tiempo real, con reentrenamiento periódico y medidas básicas de seguridad.
- Un reporte de cierre con la verificación de los criterios de aceptación.

### 3.2 No incluye

- La conexión real con una tienda en línea ni con su sitio web.
- Un servidor en producción. El despliegue se entrega como plan y como script local.
- Datos personales de los clientes. El modelo solo usa el comportamiento de navegación.

## 4. Datos

| Campo | Detalle |
| --- | --- |
| Nombre | Online Shoppers Purchasing Intention Dataset |
| Fuente | UCI Machine Learning Repository (Sakar y Kastro, 2018) |
| Licencia | CC BY 4.0 |
| Registros | 12,330 sesiones, cada una de un usuario distinto |
| Variables | 17 predictoras y 1 objetivo (`Revenue`) |
| Valores faltantes | Ninguno, según la ficha de UCI |
| Proporción de compras | 15.5 % (1,908 sesiones) |
| Periodo | Un año, sin fechas exactas publicadas |

### 4.1 Limitaciones conocidas

- **Otra tienda, otro país.** Los datos provienen de un sitio de comercio electrónico que no se identifica. Los productos, los clientes y el país no coinciden con los de Tilde Casa.
- **Fechas especiales.** La variable `SpecialDay` mide la cercanía a fechas como San Valentín o el Día de las Madres según el calendario de la tienda original. En México, el Día de las Madres es el 10 de mayo, así que estas fechas pueden no coincidir.
- **Sesiones completas.** Las variables describen la sesión al terminar, pero el despliegue predice durante la navegación. Un modelo entrenado con sesiones completas puede comportarse distinto con sesiones a medias.
- **Códigos sin significado.** Sistema operativo, navegador, región y tipo de tráfico vienen como números sin descripción publicada.
- **Variable `PageValues`.** Es la más relacionada con la compra, porque Google Analytics la calcula a partir de las páginas previas a una transacción. Los modelos se evaluarán con y sin ella para conocer su efecto.

## 5. Equipo y roles

| Rol | Responsable | Tareas principales | Fases |
| --- | --- | --- | --- |
| Jefe de equipo | Integrante 1 | Asignar tareas y coordinar al equipo | Todas |
| Gestor de proyecto | Integrante 1 | Calendario, entregables y control de avance | Todas |
| Ingeniero de datos | Integrante 1 | Carga, limpieza y división de los datos | 2 |
| Ingeniero de aprendizaje automático | Integrante 1 | Script de predicción y plan de despliegue | 4 |
| Propietario de producto | Integrante 2 | Objetivo, criterios de aceptación y aceptación final | 1 y 5 |
| Experto en procesos | Integrante 2 | Interpretación de las variables de navegación | 1 y 2 |
| Analista de datos | Integrante 2 | Exploración y reporte de calidad de datos | 2 |
| Científico de datos | Integrante 2 | Entrenamiento y evaluación de modelos | 3 |

La lista de roles corresponde a la del curso. La documentación de TDSP de Microsoft define seis roles distintos; esta adaptación conserva su idea de separar responsabilidades.

## 6. Métricas de éxito y criterios de aceptación

Solo el 15.5 % de las sesiones termina en compra. Un modelo que responda siempre "no compra" acertaría el 84.5 % de las veces sin aprender nada, así que la exactitud no sirve como métrica principal.

La métrica principal es el **F1 de la clase "compra"**, que combina dos ideas. La **precisión** indica, de las visitas que el modelo marcó como compra, cuántas compraron de verdad. La **sensibilidad** indica, de todas las visitas que compraron, cuántas detectó el modelo. La sensibilidad tiene un criterio propio por el tipo de acción: si el modelo abre el chat a alguien que no iba a comprar, el costo es un poco del tiempo de un asesor y una ventana que el visitante cierra; si no detecta a alguien que sí iba a comprar, ese cliente se queda sin ayuda. Es preferible equivocarse de la primera forma.

El propietario de producto verificará estos criterios en la fase 5.

| Criterio | Meta | Cómo se mide |
| --- | --- | --- |
| C1. F1 de la clase "compra" | Al menos 0.60 | Grupo de prueba |
| C2. Sensibilidad de la clase "compra" | Al menos 0.70 | Grupo de prueba |
| C3. Mejora sobre el modelo de referencia | F1 mayor que el de un modelo que siempre predice "no compra" | Grupo de prueba |
| C4. Script de predicción | Devuelve una probabilidad para cada sesión de ejemplo | Ejecución de `Code/Deployment/predict.py` |
| C5. Reproducibilidad | Otra persona obtiene los mismos resultados siguiendo solo el README | Ejecución en la computadora del otro integrante |

Las metas se fijan antes de entrenar cualquier modelo. Si el resultado final no las alcanza, el reporte de cierre lo documenta y propone qué haría falta para lograrlo.

## 7. Plan de trabajo

| Fase TDSP | Entregables | Responsable | Fecha límite |
| --- | --- | --- | --- |
| 1. Comprensión del negocio | Acta del proyecto | Integrantes 1 y 2 | 16 de octubre de 2026 |
| 2. Adquisición y comprensión de los datos | Diccionario de datos, reporte de datos, notebooks 01 y 02 | Integrantes 1 y 2 | 30 de octubre de 2026 |
| 3. Modelado | Notebooks 03, 04 y 05, reportes de modelos | Integrante 2 | 20 de noviembre de 2026 |
| 4. Despliegue | Script de predicción, arquitectura de la solución | Integrante 1 | 4 de diciembre de 2026 |
| 5. Aceptación del cliente | Reporte de cierre | Integrante 2 | 11 de diciembre de 2026 |

Las fases 2 y 3 pueden repetirse. Al final de cada una, el equipo decide si avanza, regresa a la fase anterior o replantea el objetivo.

### 7.1 Decisiones técnicas iniciales

- **División de los datos:** 80 % entrenamiento y 20 % prueba, estratificada por `Revenue`. El grupo de prueba conserva la proporción real de compras y no se usa hasta la evaluación final.
- **Modelos:** Random Forest como modelo principal y árbol de decisión como comparación. Un modelo que siempre predice "no compra" sirve como referencia mínima.
- **Desbalance:** la primera ejecución usa los datos sin balancear. La segunda aplica un rebalanceo solo al grupo de entrenamiento y dentro de cada pliegue de la validación cruzada.
- **Reproducibilidad:** cada notebook con procesos aleatorios define su propia semilla (`SEED = 1`).

## 8. Arquitectura de la solución

1. **Arranque.** El modelo entrenado con los datos de UCI se instala detrás de una API.
2. **Predicción en tiempo real.** Durante cada visita, el sitio envía a la API el comportamiento acumulado de la sesión y recibe la probabilidad de compra. Si supera el umbral acordado, el sitio abre el chat proactivo.
3. **Recolección.** Cada sesión terminada se guarda con su resultado, sin datos personales del cliente.
4. **Reentrenamiento.** Cuando la tienda acumula suficientes compras propias, se entrena un modelo nuevo y se compara con el actual. Solo reemplaza al actual si lo supera por un margen claro.

El detalle de este plan, junto con las medidas de seguridad, está en [Arquitectura de la solución](<System Architecture.md>).

## 9. Riesgos y supuestos

| Riesgo | Efecto | Medida |
| --- | --- | --- |
| Los datos de otra tienda no representan a Tilde Casa | El modelo inicial funciona peor en la tienda real | Reentrenar con datos propios en cuanto sea posible |
| `PageValues` concentra la capacidad de predicción | Resultados optimistas que no se repiten en otra tienda | Evaluar modelos con y sin esta variable |
| Desbalance de clases | El modelo ignora la clase "compra" | F1 y sensibilidad como métricas; rebalanceo en la segunda ejecución |
| Rebalanceo mal aplicado | Métricas infladas por fuga de información | Rebalancear solo el entrenamiento y dentro de cada pliegue |

## 10. Comunicación del equipo

- **Repositorio:** GitHub, con un commit por avance y mensajes que indiquen la fase.
- **Notebooks:** cada integrante trabaja en notebooks distintos para evitar conflictos al combinar cambios.
- **Revisiones:** al cerrar cada fase, ambos integrantes revisan los entregables antes de avanzar.

## 11. Referencias

Sakar, C. O., Polat, S. O., Katircioglu, M. y Kastro, Y. (2019). Real-time prediction of online shoppers' purchasing intention using multilayer perceptron and LSTM recurrent neural networks. *Neural Computing and Applications*, *31*(10), 6893-6908. <https://doi.org/10.1007/s00521-018-3523-0>

Sakar, C. O. y Kastro, Y. (2018). *Online shoppers purchasing intention dataset* [Conjunto de datos]. UCI Machine Learning Repository. <https://doi.org/10.24432/C5F88Q>

Forrester. (s. f.). *Leverage the power of proactive chat for predictive engagement* [Entrada de blog]. <https://go.forrester.com/blogs/14-10-03-leverage_the_power_of_proactive_chat_for_predictive_engagement>

Sun, H., Chen, J. y Fan, M. (2021). Effect of live chat on traffic-to-sales conversion: Evidence from an online marketplace. *Production and Operations Management*, 1201-1219. <https://doi.org/10.1111/poms.13320>
