from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),


    path('posts/', views.PostListView.as_view(), name='posts'),              # list
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),  # create
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),  # detail
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-edit'),  # update
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),  # delete


    path("posts/", views.post_list, name="posts"),

    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
]
