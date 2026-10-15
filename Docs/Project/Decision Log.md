# Registro de decisiones

Decisiones técnicas tomadas durante el proyecto, con su motivo. Las fechas siguen el calendario de referencia del [acta del proyecto](Charter.md).

| Fase | Decisión | Motivo |
| --- | --- | --- |
| 1 | Usar datos públicos de otra tienda como punto de partida | La tienda hipotética no tiene historial propio (arranque en frío) |
| 1 | Usar el modelo para decidir a quién ofrecer un chat proactivo con asesores humanos | Los asesores son pocos y una ventana no solicitada interrumpe; el modelo concentra la atención en los visitantes con mayor intención de compra |
| 1 | F1 y sensibilidad de la clase "compra" como métricas principales | Con 15.5 % de compras, la exactitud no distingue un buen modelo de uno que nunca predice compra |
| 1 | Adoptar la estructura de carpetas de la plantilla oficial de TDSP | Seguir la organización que propone Microsoft para proyectos con esta metodología |
| 2 | División 80/20 estratificada antes de cualquier limpieza | Evitar que las decisiones de limpieza dependan del grupo de prueba |
| 2 | Conservar las filas repetidas | Son visitas de una o dos páginas sin duración, probablemente de usuarios distintos; eliminarlas reduciría los rebotes reales |
| 2 | Conservar `VisitorType = Other` y los códigos poco frecuentes | Son datos válidos; los códigos raros se agrupan dentro del pipeline del modelo |
| 2 | Unificar `June` como `Jun` | Mantener el mismo formato en todos los meses |
| 3 | Evaluar cada modelo con y sin `PageValues` | Medir cuánto depende el modelo de la variable más ligada a la compra |
| 3 | Dos ejecuciones: sin balancear y balanceada | Comparar el efecto de compensar el desbalance de clases |
| 3 | Balanceo solo dentro de cada pliegue de entrenamiento | Evitar que copias de una sesión aparezcan en el pliegue que califica al modelo |
| 3 | Seleccionar el modelo por mayor F1 en validación cruzada | Criterio fijado antes de usar el grupo de prueba |
| 3 | Ajustar el umbral con probabilidades fuera de pliegue | Cumplir la sensibilidad mínima sin usar el grupo de prueba |
| 4 | Aceptar sesiones de enero y abril con una advertencia | La tienda opera todo el año, aunque esos meses no aparezcan en los datos |
| 4 | Guardar el modelo comprimido | Reducir el archivo de 55 MB a 11 MB para el repositorio |
