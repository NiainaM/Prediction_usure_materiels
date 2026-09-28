import pandas as pd
import numpy as np
import os

def create_features(input_path="data/raw/telemetry_export.csv", output_path="data/processed/telemetry_features.csv"):
    print("1/2 - Chargement et ingénierie des caractéristiques (Feature Engineering)...")
    df = pd.read_csv(input_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Tri temporel par machine
    df = df.sort_values(by=['machine_id', 'timestamp'])
    
    # 1. Calcul des moyennes glissantes et de la volatilité sur une fenêtre de 3 heures
    df['temp_roll_mean_3h'] = df.groupby('machine_id')['temperature_celsius'].transform(lambda x: x.rolling(3, min_periods=1).mean())
    df['vib_roll_mean_3h'] = df.groupby('machine_id')['vibration_mm_s'].transform(lambda x: x.rolling(3, min_periods=1).mean())
    df['vib_roll_std_3h'] = df.groupby('machine_id')['vibration_mm_s'].transform(lambda x: x.rolling(3, min_periods=1).std()).fillna(0)
    
    # 2. Définition de la variable cible (Target): 1 si la machine dépasse les seuils critiques d'usure
    # Exemple de règle métier : Température > 78°C OU Vibrations > 3.3 mm/s
    df['target_wear_risk'] = np.where(
        (df['temperature_celsius'] > 78.0) | (df['vibration_mm_s'] > 3.3), 1, 0
    )
    
    # Création du dossier processed si inexistant
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Features sauvegardées sous : {output_path}")

if __name__ == "__main__":
    create_features()