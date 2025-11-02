# retrieve.md

Commands:
>>> Book.objects.all()
>>> Book.objects.get(id=1)
>>> Book.objects.filter(author="George Orwell")

Output:
[<Book: 1984 by George Orwell (1949)>]
<Book: 1984 by George Orwell (1949)>
<QuerySet [<Book: 1984 by George Orwell (1949)>]>

Comment: Verified the created record can be retrieved by id and filters.
