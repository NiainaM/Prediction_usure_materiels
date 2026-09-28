import requests

# URL de l'API FastAPI
url = "http://127.0.0.1:8000/predict"

# Payload simulant une machine présentant un risque d'usure élevé (forte température et vibrations)
payload_risk = {
    "temperature_celsius": 82.5,
    "vibration_mm_s": 3.6,
    "pressure_psi": 98.4,
    "operating_hours": 2450.0,
    "temp_roll_mean_3h": 80.1,
    "vib_roll_mean_3h": 3.4,
    "vib_roll_std_3h": 0.42
}

# Payload simulant une machine en état normal
payload_normal = {
    "temperature_celsius": 68.2,
    "vibration_mm_s": 2.1,
    "pressure_psi": 101.2,
    "operating_hours": 1200.0,
    "temp_roll_mean_3h": 67.5,
    "vib_roll_mean_3h": 2.0,
    "vib_roll_std_3h": 0.15
}

print("--- Test 1 : Cas de risque d'usure ---")
res_risk = requests.post(url, json=payload_risk)
print("Code HTTP :", res_risk.status_code)
print("Réponse   :", res_risk.json())

print("\n--- Test 2 : Cas fonctionnement normal ---")
res_normal = requests.post(url, json=payload_normal)
print("Code HTTP :", res_normal.status_code)
print("Réponse   :", res_normal.json())