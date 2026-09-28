# Image Python légère pour optimiser la taille du conteneur
FROM python:3.11-slim

# Éviter l'écriture de fichiers .pyc et forcer l'affichage immédiat des logs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source de l'API et de l'artefact entraîné
COPY src/ ./src/
COPY models/ ./models/

# Exposition du port
EXPOSE 8000

# Commande de démarrage sur l'interface 0.0.0.0 pour écouter hors du conteneur
CMD ["python", "-m", "uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]