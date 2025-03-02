import os
from fastapi import FastAPI, HTTPException
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from models import Book  # Import du modèle

# Configuration MongoDB via les variables d'environnement
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
DATABASE_NAME = os.getenv("MONGO_DB", "books_db")

# Initialisation de la connexion MongoDB
client = AsyncIOMotorClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}")
db = client[DATABASE_NAME]
collection = db["books"]

app = FastAPI(title="Book Service")

# Route pour créer un livre
@app.post("/books/", response_model=Book)
async def create_book(book: Book):
    existing_book = await collection.find_one({"book_id": book.book_id})
    if existing_book:
        raise HTTPException(status_code=400, detail="Book ID already exists")

    book_dict = book.dict()
    await collection.insert_one(book_dict)
    return book

# Route pour récupérer tous les livres
@app.get("/books/", response_model=List[Book])
async def get_books():
    books = await collection.find().to_list(length=100)
    return books

# Route pour récupérer un livre par ID
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    book = await collection.find_one({"book_id": book_id})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(**book)

# Route pour mettre à jour un livre
@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update: Book):
    existing_book = await collection.find_one({"book_id": book_id})
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_update.dict(exclude_unset=True)
    await collection.update_one({"book_id": book_id}, {"$set": update_data})
    
    updated_book = await collection.find_one({"book_id": book_id})
    return Book(**updated_book)

# Route pour supprimer un livre
@app.delete("/books/{book_id}", response_model=Book)
async def delete_book(book_id: int):
    book = await collection.find_one({"book_id": book_id})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await collection.delete_one({"book_id": book_id})
    return Book(**book)
