#!/usr/bin/env python3

from fastapi import Path
from pydantic import BaseModel, Field
from typing import List
from beanie import Document


class Title:
    STR = "The title of the book"
    MAX_LENGTH = 128
    PATH_PARAM = Path(..., title=STR, max_length=MAX_LENGTH, examples="The Catcher in the Rye")


class FirstName:
    STR = "The first name of the author"
    MAX_LENGTH = 32


class LastName:
    STR = "The last name of the author"
    MAX_LENGTH = 32


class Publisher:
    STR = "The publisher of the book"
    MAX_LENGTH = 64


class PublicationDate:
    STR = "The publication date of the book"


class BookDesc(BaseModel):
    title: str = Field(None, title=Title.STR, max_length=Title.MAX_LENGTH)
    author_first_name: str = Field(None, title=FirstName.STR, max_length=FirstName.MAX_LENGTH)
    author_last_name: str = Field(None, title=LastName.STR, max_length=LastName.MAX_LENGTH)
    publisher: str = Field(None, title=Publisher.STR, max_length=Publisher.MAX_LENGTH)
    publication_date: str = Field(None, title=PublicationDate.STR)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "The Catcher in the Rye",
                    "author_first_name": "J.D.",
                    "author_last_name": "Salinger",
                    "publisher": "Little, Brown and Company",
                    "publication_date": "1951-07-16"
                }
            ]
        }
    }


class BookDigest(BaseModel):
    title: str
    link: str


class Books(BaseModel):
    items: List[BookDigest]
    has_more: bool


# Model for Mongo
class Book(Document, BookDesc):
    pass

