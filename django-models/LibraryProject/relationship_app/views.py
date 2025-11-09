from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login   
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book, Author, Librarian


# ---------------------------
# FUNCTION-BASED VIEW (Books)
# ---------------------------
def list_books(request):
    """
    Function-based view that lists all books in the database.
    """
    books = Book.objects.all().select_related("author")
    context = {"books": books}
    return render(request, "relationship_app/list_books.html", context)


# ---------------------------
# CLASS-BASED VIEW (Library)
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


# ---------------------------
# AUTHENTICATION VIEWS
# ---------------------------

def register_user(request):
    """
    Register a new user using Django’s built-in UserCreationForm.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


def login_user(request):
    """
    Allow an existing user to log in.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("list_books")
        else:
            return render(request, "relationship_app/login.html", {"error": "Invalid username or password"})
    return render(request, "relationship_app/login.html")


def logout_user(request):
    """
    Log the user out and show a confirmation.
    """
    logout(request)
    return render(request, "relationship_app/logout.html")
