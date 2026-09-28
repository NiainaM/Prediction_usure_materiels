from fastapi.testclient import TestClient
from src.api.app import app  # Adaptez l'import selon la structure de votre projet

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

def test_predict():
    payload = {
        # Vos fonctionnalités d'entrée modèle
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200