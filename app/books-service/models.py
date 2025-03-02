from pydantic import BaseModel
from datetime import datetime

class Book(BaseModel):
    book_id: int
    title: str
    author_first_name: str
    author_last_name: str
    publisher: str
    publication_date: datetime
