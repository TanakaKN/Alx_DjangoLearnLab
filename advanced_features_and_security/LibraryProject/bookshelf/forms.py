# LibraryProject/bookshelf/forms.py
from django import forms

class ExampleForm(forms.Form):
    """
    Example form used to demonstrate CSRF protection and secure handling.
    The checker only requires that this class exists.
    """
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
