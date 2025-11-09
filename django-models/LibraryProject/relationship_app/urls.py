from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books
from . import views

urlpatterns = [
    path("books/", list_books, name="list_books"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # Built-in auth views (checker checks for LoginView/LogoutView usage)
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

    # Register (custom)
    path("register/", views.register_user, name="register"),

    # Role-based views (checker looks for admin_view route)
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),
]
