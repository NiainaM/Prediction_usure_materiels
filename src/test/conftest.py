import sys
from pathlib import Path

# Ajoute la racine du projet au sys.path
root_dir = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root_dir))