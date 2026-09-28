import os
from contextlib import asynccontextmanager
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Variable globale pour stocker le modèle en mémoire
model = None
MODEL_PATH = "models/model.pkl"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionnaire de cycle de vie de l'application FastAPI.
    Charge le modèle binaire `.pkl` au démarrage de l'API.
    """
    global model
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Le fichier de modèle '{MODEL_PATH}' est introuvable. Veuillez exécuter 'train_model.py' d'abord."
        )
    model = joblib.load(MODEL_PATH)
    print(f"✅ Modèle chargé avec succès depuis {MODEL_PATH}")
    yield
    model = None


app = FastAPI(
    title="API de Maintenance Prédictive",
    description="Inférence en temps réel du risque d'usure matérielle à partir de données de télémétrie.",
    version="1.0.0",
    lifespan=lifespan,
)


class TelemetryInput(BaseModel):
    """Schéma Pydantic pour valider le payload JSON entrant."""

    temperature_celsius: float = Field(
        ..., json_schema_extra={"example": 82.5}, description="Température du moteur en °C"
    )
    vibration_mm_s: float = Field(
        ..., json_schema_extra={"example": 3.6}, description="Vibrations mesurées en mm/s"
    )
    pressure_psi: float = Field(
        ..., json_schema_extra={"example": 98.4}, description="Pression hydraulique en PSI"
    )
    operating_hours: float = Field(
        ..., json_schema_extra={"example": 2450.0}, description="Heures de fonctionnement cumulées"
    )
    temp_roll_mean_3h: float = Field(
        ..., json_schema_extra={"example": 80.1}, description="Moyenne glissante de la température sur 3h"
    )
    vib_roll_mean_3h: float = Field(
        ..., json_schema_extra={"example": 3.4}, description="Moyenne glissante des vibrations sur 3h"
    )
    vib_roll_std_3h: float = Field(
        ..., json_schema_extra={"example": 0.42}, description="Écart-type glissant des vibrations sur 3h"
    )


class PredictionOutput(BaseModel):
    """Schéma de réponse renvoyé par l'API."""

    wear_risk: int = Field(..., description="0 = Normal, 1 = Risque d'usure critique")
    risk_label: str = Field(..., description="Description lisible de la prédiction")
    confidence_score: float = Field(..., description="Probabilité estimée pour la classe prédite")


@app.get("/health", summary="Vérification de l'état de l'API")
def health_check():
    """Vérifie que l'API est active et que le modèle est bien chargé en mémoire."""
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict", response_model=PredictionOutput, summary="Prédire le risque d'usure")
def predict(data: TelemetryInput):
    """Effectue une prédiction d'usure à partir des caractéristiques de télémétrie fournies."""
    if model is None:
        raise HTTPException(status_code=500, detail="Le modèle n'est pas chargé en mémoire.")

    # Conversion de l'objet Pydantic en DataFrame pandas avec les bons noms de colonnes
    input_data = pd.DataFrame([data.model_dump()])

    # Calcul de la prédiction et des probabilités
    prediction = int(model.predict(input_data)[0])

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_data)[0]
        confidence = float(probabilities[prediction])
    else:
        confidence = 1.0

    risk_label = "Risque d'usure élevé" if prediction == 1 else "Normal"

    return PredictionOutput(
        wear_risk=prediction,
        risk_label=risk_label,
        confidence_score=round(confidence, 4),
    )

@app.get("/")
def read_root():
    return {"message": "API de maintenance prédictive opérationnelle"}