from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

# serializer for books
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # get all fields

    # custom validation so publication year is not in future
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("publication year cannot be in the future")  # error message
        return value

# serializer for authors with nested books
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # nested books, many=True means multiple books

    class Meta:
        model = Author
        fields = ['name', 'books']  # include name and books