from datetime import date
from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """Serializer for creating and listing Book instances.

    Includes custom validation to ensure the publication_year
    is not set in the future.
    """

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value


class NestedBookSerializer(serializers.ModelSerializer):
    """Simplified Book serializer used inside AuthorSerializer.

    It is read-only and does not expose the author field because
    the book is already nested under a specific author.
    """

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year']


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author instances.

    Includes a nested, read-only list of books using
    NestedBookSerializer to demonstrate handling of a
    one-to-many relationship.
    """

    books = NestedBookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
