import pytest
import json
from books_service import app
from httpx import AsyncClient, ASGITransport

data1 = {
    "title": "1984",
    "author_first_name": "George",
    "author_last_name": "Orwell",
    "publisher": "Secker & Warburg",
    "publication_date": "1949-06-08"
}

data2 = {
    "title": "Brave New World",
    "author_first_name": "Aldous",
    "author_last_name": "Huxley",
    "publisher": "Chatto & Windus",
    "publication_date": "1932-08-01"
}

headers_content = {"Content-Type": "application/json"}
headers_accept = {"Accept": "application/json"}


@pytest.mark.asyncio
@pytest.mark.usefixtures("clearBooks")
@pytest.mark.usefixtures("initDB")
async def test_post_once():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/books", headers=headers_content, content=json.dumps(data1)
        )
        assert response.headers["Location"]
        assert response.status_code == 201


@pytest.mark.asyncio
@pytest.mark.usefixtures("clearBooks")
@pytest.mark.usefixtures("initDB")
async def test_post_twice():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response1 = await ac.post(
            "/books", headers=headers_content, content=json.dumps(data1)
        )
        assert response1.status_code == 201

        response2 = await ac.post(
            "/books", headers=headers_content, content=json.dumps(data1)
        )
        assert response2.status_code == 409


@pytest.mark.asyncio
@pytest.mark.usefixtures("clearBooks")
@pytest.mark.usefixtures("initDB")
async def test_has_more_false_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/books", headers=headers_content, content=json.dumps(data1)
        )
        assert response.headers["Location"]
        assert response.status_code == 201

        response2 = await ac.get("/books?offset=0&limit=10")
        assert response2.status_code == 200
        assert response2.json()["has_more"] == False


@pytest.mark.asyncio
@pytest.mark.usefixtures("clearBooks")
@pytest.mark.usefixtures("initDB")
async def test_has_more_true_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response1 = await ac.post(
            "/books", headers=headers_content, content=json.dumps(data1)
        )

        assert response1.headers["Location"]
        assert response1.status_code == 201

        response2 = await ac.post(
            "/books", headers=headers_content, content=json.dumps(data2)
        )
        assert response2.headers["Location"]
        assert response2.status_code == 201

        response3 = await ac.get("/books?offset=0&limit=1")
        assert response3.status_code == 200
        assert response3.json()["has_more"] == True

@pytest.mark.asyncio
@pytest.mark.usefixtures("clearBooks")
@pytest.mark.usefixtures("initDB")
async def test_delete_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Créer un livre avant de le supprimer
        response = await ac.post("/books", headers=headers_content, content=json.dumps(data1))
        assert response.status_code == 201
        book_id = response.headers["Location"].split("/")[-1]

        # Supprimer le livre
        delete_response = await ac.delete(f"/books/{book_id}")
        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == f"Book {book_id} deleted successfully."

        # Vérifier que le livre n'existe plus
        get_response = await ac.get(f"/books/{book_id}")
        assert get_response.status_code == 404
