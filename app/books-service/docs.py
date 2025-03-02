#!/usr/bin/env python3

# API Metadata
API_TITLE = "Book Management API"
API_DESCRIPTION = """
This API allows users to manage a collection of books.  
Each book has a unique identifier, title, author first name, author last name, publisher, and publication date.  

### Endpoints:
- **Create a book**: `POST /books/`
- **Get all books**: `GET /books/`
- **Get a book by ID**: `GET /books/{book_id}`
- **Update a book**: `PUT /books/{book_id}`
- **Delete a book**: `DELETE /books/{book_id}`
"""

API_VERSION = "1.0.0"

# Tags Metadata
books_metadata = [
    {
        "name": "books",
        "description": "Operations related to books collection",
    },
    {
        "name": "book",
        "description": "Operations related to a single book",
    },
]

# Documentation for API Endpoints
create_books_doc = """
## Create a New Book  
This endpoint allows the creation of a new book entry.  
### Request Body:
- `book_id` (int) - Unique identifier of the book
- `title` (str) - Title of the book
- `author_first_name` (str) - First name of the author
- `author_last_name` (str) - Last name of the author
- `publisher` (str) - Publisher of the book
- `publication_date` (str) - Date of publication  

### Response:
- Returns the created book object.
"""

get_books_doc = """
## Retrieve All Books  
This endpoint fetches a list of books.  

### Query Parameters:
- `offset` (int) - Number of items to skip for pagination
- `limit` (int) - Maximum number of items to return  

### Response:
- A JSON object containing a list of books.
- The `X-total-count` header contains the total number of books.
"""

head_books_doc = """
## Get Total Count of Books  
This endpoint returns the total number of books in the database.  
The count is returned in the `X-total-count` header.
"""

put_book_doc = """
## Update a Book  
This endpoint updates a book's details.  

### Request Body:
- All book attributes must be provided in the request body.
- The `book_id` in the path must match the `book_id` in the body.  

### Response:
- Returns the updated book object.
"""

delete_book_doc = """
## Delete a Book  
This endpoint allows the deletion of a book by its ID.  

### Response:
- A success message confirming the deletion.
"""

get_book_doc = """
## Retrieve a Book by ID  
This endpoint fetches the details of a specific book using its ID.  

### Response:
- Returns the book object if found.
"""



