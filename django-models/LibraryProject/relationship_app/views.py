from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book, Author, Librarian

# Function-based view to list books
def list_books(request):
    books = Book.objects.all().select_related("author")
    context = {"books": books}
    return render(request, "relationship_app/list_books.html", context)

# Class-based view to show library details
class LibraryDetailView(DetailView):
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
    """Allow a new user to register."""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            return redirect("login")
        else:
            return render(request, "relationship_app/register.html", {"error": "Username already exists"})
    return render(request, "relationship_app/register.html")


def login_user(request):
    """Allow a user to log in."""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("list_books")
        else:
            return render(request, "relationship_app/login.html", {"error": "Invalid credentials"})
    return render(request, "relationship_app/login.html")


def logout_user(request):
    """Log the current user out."""
    logout(request)
    return render(request, "relationship_app/logout.html")
