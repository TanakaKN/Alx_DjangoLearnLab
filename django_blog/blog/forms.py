from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

class PostForm(forms.ModelForm):
    # Not stored directly – we will parse it in the view
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas, e.g.: django, backend, APIs"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']   # author & date are set in the view

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']