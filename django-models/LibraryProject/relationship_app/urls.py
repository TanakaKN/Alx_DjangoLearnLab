from django.urls import path
from . import views
from .views import list_books   

urlpatterns = [
    # Function-based view route
    path("books/", list_books, name="list_books"),

    # Class-based DetailView route
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),
]
