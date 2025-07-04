import os
from fastapi import FastAPI, HTTPException
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from models import Book

# Variables d'environnement
MONGO_HOST = os.getenv("MONGO_HOST", "mongodb-service")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
DATABASE_NAME = os.getenv("MONGO_DB", "books_db")
AUTH_DATABASE_NAME = os.getenv("AUTH_DATABASE_NAME", "admin")  # Base de données d'authentification

# Récupérer les informations d'utilisateur et mot de passe de MongoDB
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

app = FastAPI(title="Book Service")

# Création du client MongoDB dans l'événement startup
@app.on_event("startup")
async def startup_db_client():
    if MONGO_USER and MONGO_PASSWORD:
        # Si les identifiants sont fournis, on les utilise dans la chaîne de connexion
        mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{DATABASE_NAME}?authSource={AUTH_DATABASE_NAME}"
    else:
        # Sinon, on se connecte sans utilisateur/mot de passe
        mongo_uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{DATABASE_NAME}"

    # Connexion à la base de données MongoDB
    app.state.mongo_client = AsyncIOMotorClient(mongo_uri)
    app.state.db = app.state.mongo_client[DATABASE_NAME]

# Fermeture du client MongoDB lors du shutdown de l'application
@app.on_event("shutdown")
async def shutdown_db_client():
    app.state.mongo_client.close()

def get_collection():
    return app.state.db["books"]

@app.post("/books/", response_model=Book)
async def create_book(book: Book):
    collection = get_collection()
    existing_book = await collection.find_one({"book_id": book.book_id})
    if existing_book:
        raise HTTPException(status_code=400, detail="Book ID already exists")
    book_dict = book.dict()
    await collection.insert_one(book_dict)
    return book

@app.get("/books/", response_model=List[Book])
async def get_books():
    collection = get_collection()
    books = await collection.find().to_list(length=100)
    return books

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    collection = get_collection()
    book = await collection.find_one({"book_id": book_id})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(**book)

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update: Book):
    collection = get_collection()
    existing_book = await collection.find_one({"book_id": book_id})
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    update_data = book_update.dict(exclude_unset=True)
    await collection.update_one({"book_id": book_id}, {"$set": update_data})
    updated_book = await collection.find_one({"book_id": book_id})
    return Book(**updated_book)

@app.delete("/books/{book_id}", response_model=Book)
async def delete_book(book_id: int):
    collection = get_collection()
    book = await collection.find_one({"book_id": book_id})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    await collection.delete_one({"book_id": book_id})
    return Book(**book)
