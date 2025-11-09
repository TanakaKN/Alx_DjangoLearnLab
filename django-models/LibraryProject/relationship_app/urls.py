from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books
from . import views

urlpatterns = [
    path("books/", list_books, name="list_books"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register_user, name="register"),

    # Role-based views
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),

    # ✅ Permission-based book management
    path("add-book/", views.add_book, name="add_book"),
    path("edit-book/<int:pk>/", views.edit_book, name="edit_book"),
    path("delete-book/<int:pk>/", views.delete_book, name="delete_book"),
]

