from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),                 # /
    path("posts/", views.post_list, name="posts"),    # /posts/
    path("login/", views.BlogLoginView.as_view(), name="login"),
    path("logout/", views.BlogLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
]