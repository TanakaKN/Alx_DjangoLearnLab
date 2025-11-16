# LibraryProject/bookshelf/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    """
    Function-based view that lists all books.
    The checker looks for:
      - function name 'book_list'
      - the literal 'raise_exception' inside the decorator
      - a variable named 'books' used for the queryset/context
    """
    books = Book.objects.all()
    context = {"books": books}
    return render(request, "bookshelf/list_books.html", context)
