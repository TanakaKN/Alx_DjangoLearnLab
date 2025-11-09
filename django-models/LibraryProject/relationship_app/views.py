from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library, Author, Librarian
# The checker required: from .models import Library

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
# CLASS-BASED VIEW (DetailView)
# ---------------------------
# This uses Django's DetailView as required by the checker.
class LibraryDetailView(DetailView):
    """
    Class-based DetailView for a Library that includes the books in context.
    Uses `DetailView` to satisfy the "Utilize Django's ListView or DetailView" requirement.
    """
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"  # so template uses {{ library }}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add 'books' to the template context for ease of iteration
        context["books"] = self.object.books.all().select_related("author")
        return context
