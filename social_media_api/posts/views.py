from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.generics import ListAPIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


class DefaultPagination(PageNumberPagination):
    """
    Simple page number pagination:
    - ?page=1, ?page=2
    - default page size: 10 items
    """
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on posts.

    Endpoints (through router):
      - GET    /posts/           -> list posts (with pagination + search)
      - POST   /posts/           -> create new post (auth required)
      - GET    /posts/{id}/      -> retrieve one post
      - PUT    /posts/{id}/      -> update post (only author)
      - PATCH  /posts/{id}/      -> partial update (only author)
      - DELETE /posts/{id}/      -> delete post (only author)
    """

    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination

    # DRF filtering: allow searching by title or content
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        """
        When a post is created, set the author to the current user.
        """
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on comments.

    Endpoints (through router):
      - GET    /comments/           -> list comments (paginated)
      - POST   /comments/           -> create comment
      - GET    /comments/{id}/      -> retrieve one comment
      - PUT    /comments/{id}/      -> update comment (only author)
      - PATCH  /comments/{id}/      -> partial update (only author)
      - DELETE /comments/{id}/      -> delete comment (only author)
    """

    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination

    def perform_create(self, serializer):
        """
        When a comment is created, set the author to the current user.
        """
        serializer.save(author=self.request.user)

class FeedView(ListAPIView):
    """
    GET /feed/
    - Returns posts from users the current user is following,
      ordered by newest first, with pagination.
    """

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = self.request.user
        # all users that this user follows
        following_users = user.following.all()
        # posts whose author is in that set
        return Post.objects.filter(author__in=following_users).order_by("-created_at")
