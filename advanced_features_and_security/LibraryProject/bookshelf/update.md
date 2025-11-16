# update.md

Command:
>>> from bookshelf.models import Book
>>> book = Book.objects.get(id=1)
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> Book.objects.get(id=1)

Output:
<Book: Nineteen Eighty-Four by George Orwell (1949)>

Comment:
The book title was successfully updated from "1984" to "Nineteen Eighty-Four" and saved in the database.
