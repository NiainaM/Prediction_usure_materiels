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
    # Remplacez ces clés par les champs exacts définis dans le schéma Pydantic de votre app.py
    payload = {
        "air_temperature": 298.1,
        "process_temperature": 308.6,
        "rotational_speed": 1500,
        "torque": 40.0,
        "tool_wear": 5
    }
    
    response = client.post("/predict", json=payload)
    assert response.status_code == 200, f"Détail de l'erreur FastAPI (422) : {response.json()}"