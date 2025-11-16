# LibraryProject/relationship_app/models.py
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Author / Book / Library / Librarian models (keep minimal but present)
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        )


class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name="libraries", blank=True)

    def __str__(self):
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name="librarian")

    def __str__(self):
        return f"{self.name} ({self.library})"


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Member")

    def __str__(self):
        username = getattr(self.user, "username", str(self.user))
        return f"{username} - {self.role}"


@receiver(post_save)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile when a new user of the active AUTH_USER_MODEL is created.
    Import get_user_model() inside handler to avoid app registry problems.
    """
    if not created:
        return

    from django.contrib.auth import get_user_model
    User = get_user_model()
    if sender is not User:
        return

    if not hasattr(instance, "userprofile"):
        UserProfile.objects.create(user=instance)
