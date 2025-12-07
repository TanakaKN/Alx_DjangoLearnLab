from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

        # Post Section
    path('post/', views.PostListView.as_view(), name='posts'),  
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path("posts/", views.post_list, name="posts"),


        # Comments section
    path(
        'post/<int:pk>/comments/new/',
        views.CommentCreateView.as_view(),
        name='comment-create'
    ),
    path(
        'comment/<int:pk>/update/',
        views.CommentUpdateView.as_view(),
        name='comment-update'
    ),
    path(
        'comment/<int:pk>/delete/',
        views.CommentDeleteView.as_view(),
        name='comment-delete'
    ),

    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
]
