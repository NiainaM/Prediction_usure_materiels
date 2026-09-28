import sys
from pathlib import Path

# Ajoute la racine du projet au chemin d'accès Python
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient

# Gestion automatique de l'emplacement de app.py
try:
    from src.api.app import app
except ModuleNotFoundError:
    try:
        from src.api.app import app
    except ModuleNotFoundError:
        from api.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    if response.status_code == 404:
        response = client.get("/")
    assert response.status_code == 200

def test_predict():
    payload = {
        "temperature_celsius": 25.5,
        "vibration_mm_s": 1.2,
        "pressure_psi": 101.3,
        "operating_hours": 150.0,
        "temp_roll_mean_3h": 25.1,
        "vib_roll_mean_3h": 1.15,
        "vib_roll_std_3h": 0.05,
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200, (
        f"Détail de l'erreur FastAPI ({response.status_code}) : {response.json()}"
    )