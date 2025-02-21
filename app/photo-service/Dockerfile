FROM python:3.8
WORKDIR /code

# Copier les fichiers nécessaires
COPY ./requirements.txt /code/requirements.txt
COPY ./proto/tags.proto /code/proto/tags.proto

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install grpcio-tools

# Générer les fichiers Python à partir de tags.proto
RUN python -m grpc_tools.protoc -I/code/proto --python_out=/code --grpc_python_out=/code /code/proto/tags.proto

# Copier le reste des fichiers
COPY ./*.py /code/

# Définir les variables d'environnement
ENV GRACEFUL_TIMEOUT=10
ENV MONGO_HOST=172.17.0.2
ENV PHOTOGRAPHER_HOST=172.17.0.3
ENV TAGS_HOST=172.17.0.4

# Lancer l'application
CMD ["uvicorn", "photo_service:app", "--host", "0.0.0.0", "--port", "80"]


