from fastapi.testclient import TestClient
from datetime import datetime
from book_service import app  # Assurez-vous que le module book_service est accessible

# Initialisation du client de test
client = TestClient(app)

# Données de test
book_data = {
    "book_id": 1,
    "title": "DevOps Essentials",
    "author_first_name": "Jane",
    "author_last_name": "Doe",
    "publisher": "Tech Books",
    "publication_date": datetime(2022, 6, 10).isoformat()
}

def test_create_book():
    """Test pour la création d'un livre"""
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    assert response.json()["book_id"] == book_data["book_id"]
    assert response.json()["title"] == book_data["title"]

def test_get_books():
    """Test pour récupérer la liste des livres"""
    client.post("/books/", json=book_data)  # Ajouter un livre pour tester
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) > 0  # Vérifier que la liste des livres n'est pas vide

def test_get_book():
    """Test pour récupérer un livre par ID"""
    client.post("/books/", json=book_data)  # Ajouter un livre
    response = client.get(f"/books/{book_data['book_id']}")
    assert response.status_code == 200
    assert response.json()["book_id"] == book_data["book_id"]
    assert response.json()["title"] == book_data["title"]

def test_update_book():
    """Test pour mettre à jour un livre"""
    updated_book_data = {**book_data, "title": "Advanced DevOps"}
    client.post("/books/", json=book_data)  # Ajouter un livre
    response = client.put(f"/books/{book_data['book_id']}", json=updated_book_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Advanced DevOps"

def test_delete_book():
    """Test pour supprimer un livre"""
    client.post("/books/", json=book_data)  # Ajouter un livre
    response = client.delete(f"/books/{book_data['book_id']}")
    assert response.status_code == 200
    assert response.json()["book_id"] == book_data["book_id"]
    assert response.json()["title"] == book_data["title"]
