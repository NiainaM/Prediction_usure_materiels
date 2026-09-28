import pandas as pd
import numpy as np
import os

def create_features(input_path="data/raw/telemetry_export.csv", output_path="data/processed/telemetry_features.csv"):
    print("1/2 - Chargement et ingénierie des caractéristiques (Feature Engineering)...")
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Le fichier d'entrée {input_path} n'existe pas. Assurez-vous d'avoir généré telemetry_export.csv.")
        
    df = pd.read_csv(input_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Tri temporel par machine
    df = df.sort_values(by=['machine_id', 'timestamp'])
    
    # Moyennes glissantes sur 3h
    df['temp_roll_mean_3h'] = df.groupby('machine_id')['temperature_celsius'].transform(lambda x: x.rolling(3, min_periods=1).mean())
    df['vib_roll_mean_3h'] = df.groupby('machine_id')['vibration_mm_s'].transform(lambda x: x.rolling(3, min_periods=1).mean())
    df['vib_roll_std_3h'] = df.groupby('machine_id')['vibration_mm_s'].transform(lambda x: x.rolling(3, min_periods=1).std()).fillna(0)
    
    # Variable cible : 1 si seuil critique dépassé
    df['target_wear_risk'] = np.where(
        (df['temperature_celsius'] > 78.0) | (df['vibration_mm_s'] > 3.3), 1, 0
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Features sauvegardées sous : {output_path}")

if __name__ == "__main__":
    create_features()
