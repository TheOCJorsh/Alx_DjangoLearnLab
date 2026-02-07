from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


# Serializer for Book model
# Converts Book objects to JSON and validates input data
class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'

    # Custom validation to ensure publication year is not in the future
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# Serializer for Author model
# Includes nested books written by the author
class AuthorSerializer(serializers.ModelSerializer):

    # Nested serializer — shows all books written by this author
    # many=True because one author has many books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
