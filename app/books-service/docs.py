#!/usr/bin/env python3

books_metadata = [
    {
        "name": "books",
        "description": "Operations on `books`",
    },
    {
        "name": "book",
        "description": "Operations on `book`",
    },
]

create_books_doc="""
This operation allows to create a new book.
The attributes of the book are given in a JSON object passed in the body of the HTTP Request.
"""

get_books_doc="""
This operation allows to get a list of books.
Since a large number of items could be returned by such a call, a pagination system is used. This
is quite common in REST APIs. The `offset` and `limit` are passed as *query* parameters (see example
below) to limit the number of items returned by a single request.

A JSON object is returned in the body of the HTTP response:
* The `items` key is an array of JSON objects with attributes `title` and `link` (to the book resource).
* The `has_more` key indicates if there are still other items that can be retrieved (by another query).

Moreover, the total count of books is returned in the `X-total-count` header of the HTTP response.
"""

head_books_doc="""
This operation allows to retrieve the total count of books
in the `X-total-count` header of the HTTP response.
"""

put_book_doc="""
This operation allows to update a book.

In accordance with `PUT` semantics, all attributes of a book must be provided.
They will replace the registered attributes.
The `title` path param and the `title` key of the JSON object representing
the attributes must be identical.
"""

delete_book_doc="""
This operation allows to delete a book.
"""

get_book_doc="""
This operation allows to retrieve the attributes of a book.
"""

