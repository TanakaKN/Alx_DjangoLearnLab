from django.db import models



from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Notification(models.Model):
    """
    Generic notification model.

    Example:
      - actor: bob
      - recipient: alice
      - verb: "liked your post"
      - target: Post object that was liked
    """

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications_from_me",
    )
    verb = models.CharField(max_length=255)

    # Generic relation to any model (Post, Comment, User, etc.)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("content_type", "object_id")

    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ["read", "-timestamp"]  # unread first, then newest

    def __str__(self):
        return f"To {self.recipient} - {self.actor} {self.verb}"

