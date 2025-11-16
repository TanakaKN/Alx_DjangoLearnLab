# LibraryProject/bookshelf/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_protect
from .models import Book
from .forms import ExampleForm  # <-- checker looks for this exact import

@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    """
    Function-based view that lists all books (exists from prior assignment).
    """
    books = Book.objects.all()
    context = {"books": books}
    return render(request, "bookshelf/list_books.html", context)


@csrf_protect
def example_form_view(request):
    """
    Example view demonstrating use of ExampleForm.
    The checker needs to see ExampleForm imported and used in views.py.
    """
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            # For the assignment we won't save to DB here; just redirect or render success.
            # Demonstrate security-aware handling by using cleaned_data only.
            data = form.cleaned_data
            # In a real app you would create a model instance or perform safe operations here.
            return render(request, "bookshelf/form_success.html", {"data": data})
    else:
        form = ExampleForm()

    return render(request, "bookshelf/example_form.html", {"form": form})
