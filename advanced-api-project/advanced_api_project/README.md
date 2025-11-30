# Advanced API Project - Django REST Framework

This project implements a simple book library API using Django and Django REST Framework.

## Models
- Author: represents a book author.
- Book: represents a book and is linked to an author via a ForeignKey.

## Endpoints
- /api/authors/
- /api/authors/<id>/
- /api/books/
- /api/books/<id>/

The BookSerializer includes validation to ensure the publication_year
is not set in the future. The AuthorSerializer nests a read-only list
of the author's books.
