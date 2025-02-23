#!/usr/bin/env python3

import uvicorn

from fastapi import Body, FastAPI, HTTPException, Path
from starlette.responses import Response
from fastapi.logger import logger

from contextlib import asynccontextmanager
from pydantic_settings import BaseSettings
import pymongo
from models import Book, BookDesc, Books, BookDigest
import docs

from beanie import init_beanie
import motor


class Settings(BaseSettings):
    mongo_host: str = "mongo"
    mongo_port: str = "27017"
    mongo_user: str = ""
    mongo_password: str = ""
    database_name: str = "books"
    auth_database_name: str = "books"


settings = Settings()


@asynccontextmanager
async def startup_event(application: FastAPI):
    conn = f"mongodb://"
    if settings.mongo_user:
        conn += f"{settings.mongo_user}:{settings.mongo_password}@"
    conn += f"{settings.mongo_host}:{settings.mongo_port}"
    conn += f"/{settings.database_name}?authSource={settings.auth_database_name}"
    client = motor.motor_asyncio.AsyncIOMotorClient(conn)
    await init_beanie(
        database=client[settings.database_name], document_models=[Book]
    )
    yield


app = FastAPI(
    title="Book Service",
    openapi_tags=docs.books_metadata,
    lifespan=startup_event,
)


@app.post(
    "/books",
    status_code=201,
    summary="Upload a new Book",
    description=docs.create_books_doc,
    tags=["books"],
)
async def create_book(
    response: Response,
    book_desc: BookDesc = Body(
        example={
            "title": "1984",
            "author_first_name": "George",
            "author_last_name": "Orwell",
            "publisher": "Secker & Warburg",
            "publication_date": "1949-06-08",
        }
    ),
):
    try:
        check = await Book.find_one(Book.title == book_desc.title)
        if check is None:
            await Book(**dict(book_desc)).insert()
            response.headers["Location"] = "/books/" + str(book_desc.title)
        else:
            raise HTTPException(status_code=409, detail="Conflict")
    except pymongo.errors.ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="Mongo unavailable")


@app.get(
    "/books",
    status_code=200,
    summary="Get a list of Books",
    description=docs.get_books_doc,
    tags=["books"],
)
async def get_books(
    response: Response, offset: int = 0, limit: int = 10
) -> Books:
    book_digests = list()
    last_id = 0
    try:
        response.headers["X-Total-Count"] = str(await Book.count())
        async for result in Book.find().sort("_id").skip(offset).limit(limit):
            digest = BookDigest(
                title=result.title,
                link="/books/" + result.title,
            )
            last_id = result.id
            book_digests.append(digest)
    except pymongo.errors.ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="Mongo unavailable")
    has_more = await Book.find(Book.id > last_id).to_list()
    return {"items": book_digests, "has_more": True if len(has_more) else False}


@app.get(
    "/books/{title}",
    response_model=BookDesc,
    status_code=200,
    summary="Get a Book",
    description=docs.get_book_doc,
    tags=["books"],
)
async def get_book(
    title: str = Path(
        title="The title of the book",
        max_length=256,
        examples="1984",
    )
):
    try:
        book = await Book.find_one(Book.title == title)
        if book is not None:
            return book
        else:
            raise HTTPException(status_code=404, detail="Book does not exist")
    except pymongo.errors.ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="Mongo unavailable")


@app.put(
    "/books/{title}",
    status_code=200,
    summary="Update a Book",
    description=docs.put_book_doc,
    tags=["books"],
)
async def update_book(
    title: str = Path(
        title="The title of the book",
        max_length=256,
        examples="1984",
    ),
    book: BookDesc = Body(
        example={
            "title": "1984",
            "author_first_name": "George",
            "author_last_name": "Orwell",
            "publisher": "Secker & Warburg",
            "publication_date": "1949-06-08",
        }
    ),
) -> None:
    try:
        found = await Book.find_one(Book.title == title)
        if found is None:
            raise HTTPException(status_code=404, detail="Not Found")
        elif title != book.title:
            raise HTTPException(
                status_code=422,
                detail="Path param and body title must be identical",
            )
        else:
            await found.set(dict(book))
    except pymongo.errors.ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="Mongo unavailable")

@app.delete("/book/{title}", status_code=200)
async def delete_book(title: str = Path(title="Title of the book")):
    try:
        book = await Book.find_one(Book.title == title)
        if book is not None:
            await book.delete()
            return {"message": f"Book '{title}' deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    except pymongo.errors.ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="Mongo unavailable")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

