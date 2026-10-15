# Arquitectura de la solución y plan de despliegue

Plan de despliegue del modelo en la tienda hipotética Tilde Casa. Lo implementado en este proyecto es el script de predicción ([`Code/Deployment/predict.py`](../../Code/Deployment/predict.py)); el resto es una propuesta.

> **Caso de demostración:** la tienda, el chat proactivo y la arquitectura descrita son hipotéticos. Su propósito es demostrar cómo se planea el despliegue en la fase 4 de TDSP.

## Chat proactivo

La acción que toma la tienda con la predicción es un **chat proactivo**: una ventana que aparece en una esquina de la página por iniciativa de la tienda, con un mensaje como "¿Te ayudo con tu compra?". La atiende un asesor humano. El chat también puede abrirse a petición del cliente; lo que decide el modelo es a quién se le ofrece sin que lo pida.

- **Por qué no a todos:** la tienda tiene pocos asesores, y una ventana no solicitada interrumpe a quien solo está mirando.
- **Plataforma:** la tienda funcionaría sobre una plataforma de comercio electrónico con un complemento de chat. El código de la página consulta la API del modelo y, si la probabilidad supera el umbral, abre la ventana.
- **Complemento futuro:** un chatbot disponible para todos en modo pasivo, para dudas simples, mientras los asesores se concentran en los visitantes que marca el modelo.

## Flujo de la solución

```text
Visitante navega en la tienda
        │
        ▼
Sitio web ── comportamiento acumulado de la sesión ──▶ API de predicción
        ▲                                                  │
        │                                     probabilidad de compra
        │                                                  │
        └── abrir chat proactivo si probabilidad ≥ umbral ◀┘

Al cerrar la sesión:
Sitio web ── sesión + resultado (compró o no) ──▶ Base de datos de sesiones
                                                       │
                                     reentrenamiento periódico
                                                       │
                                                       ▼
                                        Modelo retador ── comparación ──▶ Modelo en uso
```

## Componentes

| Componente | Función | Estado |
| --- | --- | --- |
| Script de predicción | Valida una sesión, aplica la limpieza del notebook 02 y devuelve la probabilidad y la decisión | Implementado |
| Modelo y metadatos | `final_model.joblib` y `model_metadata.json`, con el umbral y las variables esperadas | Implementado |
| API de predicción | Servicio web que recibe sesiones del sitio y responde con el resultado del script | Propuesta |
| Base de datos de sesiones | Guarda cada sesión terminada con su resultado, sin datos personales | Propuesta |
| Reentrenamiento | Proceso periódico que entrena un modelo nuevo y lo compara con el actual | Propuesta |

## Uso del script de predicción

```bash
cd Code/Deployment
python predict.py
```

Sin argumentos usa las tres sesiones de [`sample_sessions.json`](../../Code/Deployment/sample_sessions.json). Con un archivo propio, el formato es una lista JSON con las mismas variables de la base original:

```bash
python predict.py ruta/a/sesiones.json
```

Salida con las sesiones de ejemplo:

```text
{"session_id": "ejemplo_1", "probabilidad_compra": 0.967, "abrir_chat": true}
{"session_id": "ejemplo_2", "probabilidad_compra": 0.0, "abrir_chat": false}
{"session_id": "ejemplo_3", "probabilidad_compra": 0.503, "abrir_chat": false}
```

El script rechaza sesiones con valores imposibles (duraciones negativas, tasas mayores que 1, tipos de visitante desconocidos). Las sesiones de enero o abril, meses ausentes en los datos de entrenamiento, se procesan con una advertencia, porque la tienda opera todo el año.

## Estrategia de arranque en frío

1. **Inicio.** La tienda usa el modelo entrenado con los datos de UCI como referencia.
2. **Recolección.** Cada sesión terminada se guarda con su resultado. Conviene registrar también el estado de la sesión a mitad de la visita (por ejemplo, a los 2 y a los 5 minutos), porque el modelo actual se entrenó con sesiones completas y en tiempo real verá sesiones incompletas.
3. **Primer modelo propio.** Cuando la tienda acumule al menos 1,000 sesiones con compra, se entrena un modelo con sus propios datos y se compara con el de referencia.
4. **Mantenimiento.** Reentrenamiento mensual con los datos de los últimos 12 meses, para cubrir todas las temporadas.

## Reglas de reemplazo del modelo

Un modelo nuevo (retador) solo reemplaza al modelo en uso (campeón) si cumple todas las condiciones:

- Supera al campeón por al menos 0.02 de F1, evaluados ambos con las sesiones más recientes, que ninguno usó para entrenar.
- Mantiene una sensibilidad de al menos 0.70.
- La proporción de compras predichas no se aleja más de 5 puntos porcentuales de la proporción real del periodo.

Si el modelo en uso empeora en producción, la versión anterior queda guardada para restaurarla.

## Monitoreo

- Proporción de sesiones con alerta frente a la proporción real de compras.
- F1 y sensibilidad mensuales, calculados con el resultado real de cada sesión.
- Cambios en las variables de entrada, como un aumento de visitas desde móviles o de un tipo de tráfico nuevo.
- Valor de `PageValues`: si cambia la configuración de Google Analytics, el modelo pierde su variable más importante.

## Seguridad y datos personales

- **Comunicación cifrada.** El sitio y la API se comunican solo por HTTPS.
- **Acceso a la API.** Solo el sitio de la tienda puede consultarla, con una clave de acceso y un límite de consultas por minuto.
- **Credenciales fuera del código.** Las claves se guardan en variables de entorno, nunca en el repositorio.
- **Archivos de modelo.** `joblib.load` puede ejecutar código al cargar un archivo, por lo que el sistema solo carga modelos generados por el propio proyecto.
- **Datos mínimos.** El modelo no usa nombre, correo ni dirección del cliente, y la base de sesiones no los guarda.
- **Marco legal.** Una tienda en México está sujeta a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares. El aviso de privacidad debe mencionar el uso del comportamiento de navegación para ofrecer ayuda durante la visita.
