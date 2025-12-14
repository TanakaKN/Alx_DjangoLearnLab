from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, FeedView, LikePostView, PostUnlikeView

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("feed/", FeedView.as_view(), name="feed"),
    
    path("posts/<int:pk>/unlike/", PostUnlikeView.as_view(), name="post-unlike"),
    path("", include(router.urls)),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='post-like'),
]
