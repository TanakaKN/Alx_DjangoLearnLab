from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for the Social Media API.

    Inherits:
      - username, password, email, first_name, last_name, etc.
    Adds:
      - bio: short text about the user
      - profile_picture: an optional image upload
      - followers: users who follow this user (many-to-many self relation)
    """

    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True,
    )

    def __str__(self):
        return self.username
