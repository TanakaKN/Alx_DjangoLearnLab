from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for the Social Media API.

    Inherits:
      - username, password, email, first_name, last_name, etc. from AbstractUser
    Adds:
      - bio: short text about the user
      - profile_picture: URL to a profile image
      - followers: users who follow this user (many-to-many self relation)
    """

    bio = models.TextField(blank=True)
    profile_picture = models.URLField(blank=True)

    # Users who follow THIS user
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True,
    )

    def __str__(self):
        return self.username
