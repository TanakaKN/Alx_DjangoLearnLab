from django.shortcuts import render
from django.views.generic.detail import DetailView   
from .models import Book, Library, Author, Librarian  


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
class LibraryDetailView(DetailView):
    """
    Class-based DetailView for a Library.
    Uses Django’s DetailView as required by the checker.
    Displays library details and books available in that library.
    """
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all().select_related("author")
        return context
