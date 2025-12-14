from rest_framework import viewsets, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.generics import ListAPIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.utils import create_notification
from notifications.models import Notification
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post, Like

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
    
class LikePostView(generics.GenericAPIView):
    """
    Allow an authenticated user to like or unlike a post.

    - POST /posts/<pk>/like/ will:
        * create a Like if it doesn't exist (like the post)
        * delete the Like if it already exists (unlike the post)
        * create a Notification when the post is liked
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # 1) Safely get the Post or return 404 if it doesn't exist
        post = generics.get_object_or_404(Post, pk=pk)

        # 2) Either get the existing Like or create a new one
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if created:
            # 3) If it's a new like, create a notification for the post author
            Notification.objects.create(
                recipient=post.author,      # who receives the notification
                actor=request.user,         # who performed the action
                verb="liked your post",     # message/description
                target=post                 # the post that was liked
            )
            return Response(
                {"detail": "Post liked"},
                status=status.HTTP_201_CREATED
            )

        # If the like already existed, treat this as "unlike"
        like.delete()
        return Response(
            {"detail": "Like removed"},
            status=status.HTTP_204_NO_CONTENT
        )



class PostUnlikeView(generics.GenericAPIView):
    """
    POST /posts/<pk>/unlike/
    - Authenticated user removes their like from the given post.
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def post(self, request, pk):
        post = generics.get_object_or_404(self.get_queryset(), pk=pk)

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
