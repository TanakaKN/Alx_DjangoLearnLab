from rest_framework import viewsets, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.generics import ListAPIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.utils import create_notification

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
        comment = serializer.save(author=self.request.user)
        post = comment.post

        # Notify post author (if not same user)
        if post.author != self.request.user:
            create_notification(
                recipient=post.author,
                actor=self.request.user,
                verb="commented on your post",
                target=post,
            )
class FeedView(generics.GenericAPIView):
    """
    GET /feed/
    Returns posts from users the current user follows.
    """

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
class PostLikeView(generics.GenericAPIView):
    """
    POST /posts/<pk>/like/
    - Authenticated user likes the given post.
    - Prevent multiple likes by the same user.
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def post(self, request, pk):
        post = get_object_or_404(self.get_queryset(), pk=pk)

        # Check if user already liked this post
        like_exists = Like.objects.filter(user=request.user, post=post).exists()
        if like_exists:
            return Response(
                {"detail": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create like
        Like.objects.create(user=request.user, post=post)

        # Create notification for the post author (if not the same user)
        if post.author != request.user:
            create_notification(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post,
            )

        return Response(
            {"detail": "Post liked."},
            status=status.HTTP_200_OK,
        )


class PostUnlikeView(generics.GenericAPIView):
    """
    POST /posts/<pk>/unlike/
    - Authenticated user removes their like from the given post.
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def post(self, request, pk):
        post = get_object_or_404(self.get_queryset(), pk=pk)

        like_qs = Like.objects.filter(user=request.user, post=post)
        if not like_qs.exists():
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like_qs.delete()
        return Response(
            {"detail": "Like removed."},
            status=status.HTTP_200_OK,
        )
