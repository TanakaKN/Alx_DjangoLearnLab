# delete.md

Commands:
>>> b = Book.objects.get(id=1)
>>> b.delete()

Output:
(1, {'bookshelf.Book': 1})
>>> Book.objects.all()
<QuerySet []>

Comment: Deletion returns (rows_deleted, details). Confirmed no rows left.
