from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")  # ou "/"
    assert response.status_code == 200

def test_predict():
    # Remplacez les clés/valeurs ci-dessous par le schéma exact de votre classe Pydantic (ex: PredictRequest)
    payload = {
        "air_temperature": 298.1,
        "process_temperature": 308.6,
        "rotational_speed": 1500,
        "torque": 40.0,
        "tool_wear": 5
    }

    response = client.post("/predict", json=payload)

    # Affiche le détail de l'erreur FastAPI dans Pytest si la validation échoue
    assert response.status_code == 200, f"Détail de l'erreur de validation : {response.json()}"
    
    # Vérification de la structure de la réponse
    data = response.json()
    assert "prediction" in data or "target" in data