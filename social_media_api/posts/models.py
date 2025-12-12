from django.db import models
from django.conf import settings


class Post(models.Model):
    """
    A social media post made by a user.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)       

    def __str__(self):
        return f"{self.title} by {self.author.username}"


class Comment(models.Model):
    """
    A comment on a post, made by a user.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

