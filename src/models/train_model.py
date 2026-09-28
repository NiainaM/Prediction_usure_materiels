%%writefile src/models/train_model.py
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score

def train_and_export():
    print("2/2 - Entraînement du modèle et génération de l'artefact .pkl...")
    
    input_path = "data/processed/telemetry_features.csv"
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Fichier introuvable: {input_path}. Exécutez d'abord build_features.py.")
        
    df = pd.read_csv(input_path)
    
    feature_cols = [
        'temperature_celsius', 'vibration_mm_s', 'pressure_psi', 
        'operating_hours', 'temp_roll_mean_3h', 'vib_roll_mean_3h', 'vib_roll_std_3h'
    ]
    
    X = df[feature_cols]
    y = df['target_wear_risk']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    print("\n--- Rapport de performance du modèle ---")
    print(classification_report(y_test, predictions))
    
    os.makedirs("models", exist_ok=True)
    model_path = "models/model.pkl"
    joblib.dump(model, model_path)
    print(f"\n✅ Modèle exporté avec succès : {model_path}")

if __name__ == "__main__":
    train_and_export()