from django.contrib.contenttypes.models import ContentType
from .models import Notification


def create_notification(recipient, actor, verb, target=None):
    """
    Utility to create a notification.

    - recipient: User who gets the notification
    - actor: User who triggered it
    - verb: description, e.g. "liked your post"
    - target: optional model instance (Post, Comment, etc.)
    """

    notification = Notification(
        recipient=recipient,
        actor=actor,
        verb=verb,
    )

    if target is not None:
        notification.content_type = ContentType.objects.get_for_model(target)
        notification.object_id = target.pk

    notification.save()
    return notification
