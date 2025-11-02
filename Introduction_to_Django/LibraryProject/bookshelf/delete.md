# delete.md

Command:
>>> from bookshelf.models import Book
>>> book = Book.objects.get(id=1)
>>> book.delete()

Output:
(1, {'bookshelf.Book': 1})
>>> Book.objects.all()
<QuerySet []>

Comment:
The book was successfully deleted from the database. The delete() method returned the number of objects removed and confirmed no books remain.
