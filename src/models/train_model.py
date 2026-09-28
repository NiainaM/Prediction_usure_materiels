import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, f1_score

def train_and_export():
    print("2/2 - Entraînement du modèle et génération de l'artefact .pkl...")
    
    # Chargement du jeu de données transformé
    df = pd.read_csv("data/processed/telemetry_features.csv")
    
    # Définition des features X et de la cible y
    feature_cols = [
        'temperature_celsius', 'vibration_mm_s', 'pressure_psi', 
        'operating_hours', 'temp_roll_mean_3h', 'vib_roll_mean_3h', 'vib_roll_std_3h'
    ]
    
    X = df[feature_cols]
    y = df['target_wear_risk']
    
    # Séparation Train/Test (Respect de la chronologie ou Split stratifié)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Création d'un Pipeline Scikit-Learn complet
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42))
    ])
    
    # Entraînement
    pipeline.fit(X_train, y_train)
    
    # Évaluation
    predictions = pipeline.predict(X_test)
    print("\n--- Rapport de performance du modèle ---")
    print(classification_report(y_test, predictions))
    
    f1 = f1_score(y_test, predictions)
    print(f"Score F1 global : {f1:.4f}")
    
    # Export de l'artefact model.pkl
    output_dir = "models"
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, "model.pkl")
    
    joblib.dump(pipeline, model_path)
    print(f"\n✅ Modèle exporté avec succès : {model_path}")

if __name__ == "__main__":
    train_and_export()