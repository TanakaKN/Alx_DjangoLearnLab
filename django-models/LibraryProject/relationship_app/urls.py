from django.urls import path
from . import views

urlpatterns = [
     path("books/", views.list_books, name="list_books"),

    # class-based view (DetailView) - uses <int:pk> which DetailView expects by default
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),
]


