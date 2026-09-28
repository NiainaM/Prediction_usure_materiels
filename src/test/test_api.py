import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient

try:
    import src.api.app as app_module
except ModuleNotFoundError:
    try:
        import src.api.app as app_module
    except ModuleNotFoundError:
        import api.app as app_module

client = TestClient(app_module.app)

def test_health_check():
    response = client.get("/health")
    if response.status_code == 404:
        response = client.get("/")
    assert response.status_code == 200

@patch.object(app_module, "model")
def test_predict(mock_model):
    # Configuration du comportement simulé du modèle
    mock_model.predict.return_value = [1]
    
    # Si votre API utilise predict_proba, décommentez la ligne suivante :
    # mock_model.predict_proba.return_value = [[0.1, 0.9]]

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