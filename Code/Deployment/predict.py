"""Estima la probabilidad de compra de una o varias sesiones de navegación.

Uso:
    python predict.py                          # usa sample_sessions.json
    python predict.py ruta/a/sesiones.json

El archivo de entrada es una lista de sesiones en formato JSON, con las mismas
variables que la base de datos original (sin ``Revenue``). Cada sesión puede
incluir un ``session_id`` para identificarla en la salida.

Seguridad: ``joblib.load`` puede ejecutar código al cargar un archivo. Solo se
carga el modelo generado por este proyecto (``Code/Modeling/models``).
"""

import json
import sys
import warnings
from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / "Modeling" / "models"
DEFAULT_INPUT = BASE_DIR / "sample_sessions.json"

VALID_MONTHS = {"Feb", "Mar", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"}
VALID_VISITOR_TYPES = {"New_Visitor", "Returning_Visitor", "Other"}
NON_NEGATIVE = [
    "Administrative", "Administrative_Duration",
    "Informational", "Informational_Duration",
    "ProductRelated", "ProductRelated_Duration", "PageValues",
]
BETWEEN_0_AND_1 = ["BounceRates", "ExitRates", "SpecialDay"]


def load_model():
    """Carga el modelo final y sus metadatos (umbral y variables)."""
    model = joblib.load(MODEL_DIR / "final_model.joblib")
    metadata = json.loads((MODEL_DIR / "model_metadata.json").read_text(encoding="utf-8"))
    return model, metadata


def prepare(sessions, features):
    """Valida las sesiones y aplica la misma limpieza que el notebook 02."""
    df = pd.DataFrame(sessions)

    missing = [c for c in features if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan variables: {missing}")

    df["Month"] = df["Month"].replace({"June": "Jun"})
    df["Weekend"] = df["Weekend"].astype(int)

    errors = []
    if (df[NON_NEGATIVE] < 0).any().any():
        errors.append("hay conteos, duraciones o PageValues negativos")
    if ((df[BETWEEN_0_AND_1] < 0) | (df[BETWEEN_0_AND_1] > 1)).any().any():
        errors.append("BounceRates, ExitRates o SpecialDay fuera del rango 0 a 1")
    unknown_visitors = set(df["VisitorType"]) - VALID_VISITOR_TYPES
    if unknown_visitors:
        errors.append(f"tipos de visitante no válidos: {sorted(unknown_visitors)}")
    if errors:
        raise ValueError("Datos no válidos: " + "; ".join(errors))

    # Enero y abril no aparecen en los datos de entrenamiento. El modelo puede
    # predecir esas sesiones, pero sin información del mes.
    unknown_months = set(df["Month"]) - VALID_MONTHS
    if unknown_months:
        warnings.warn(f"Meses sin datos de entrenamiento: {sorted(unknown_months)}", stacklevel=2)

    return df[features]


def predict(sessions):
    """Devuelve la probabilidad de compra y la decisión para cada sesión."""
    model, metadata = load_model()
    X = prepare(sessions, metadata["variables"])
    proba = model.predict_proba(X)[:, 1]
    threshold = metadata["umbral"]

    return [
        {
            "session_id": s.get("session_id", f"sesion_{i + 1}"),
            "probabilidad_compra": round(float(p), 3),
            "abrir_chat": bool(p >= threshold),
        }
        for i, (s, p) in enumerate(zip(sessions, proba))
    ]


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    sessions = json.loads(input_path.read_text(encoding="utf-8"))
    for result in predict(sessions):
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
