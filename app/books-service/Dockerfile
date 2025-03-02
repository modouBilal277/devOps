

FROM python:3.9-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y gcc

# Créer et définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application
COPY . .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application FastAPI fonctionnera
EXPOSE 80
ENV MONGO_HOST 172.17.0.2

# Lancer l'application
CMD ["uvicorn", "book_service:app", "--host", "0.0.0.0", "--port", "80"]

