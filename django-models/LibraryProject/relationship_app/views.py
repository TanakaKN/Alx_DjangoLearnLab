from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Book, Library

# ---------------------------
# FUNCTION-BASED VIEW
# ---------------------------
def list_books(request):
    """
    Function-based view that lists all books in the database.
    """
    books = Book.objects.all().select_related("author")
    context = {"books": books}
    return render(request, "relationship_app/list_books.html", context)


# ---------------------------
# CLASS-BASED VIEW
# ---------------------------
class LibraryDetailView(View):
    """
    Class-based view that displays details for a specific library,
    including all books available in that library.
    """

    def get(self, request, library_id):
        library = get_object_or_404(Library, id=library_id)
        books = library.books.all().select_related("author")
        context = {
            "library": library,
            "books": books,
        }
        return render(request, "relationship_app/library_detail.html", context)
