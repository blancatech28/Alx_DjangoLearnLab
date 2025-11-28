from rest_framework import serializers
from .models import Book, Author

# -----------------------------
# BookSerializer
# -----------------------------
class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    What it does:
    - Converts Book model instances into JSON (and vice versa) so we can send them over the API.
    - Includes all fields from the Book model like title, author, and publication_year.
    
    Special feature:
    - Checks that the publication_year is not in the future.
      If someone tries to add a book with a year beyond 2025, it raises an error.
    """
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        """
        Simple check to make sure the year isn't in the future.
        """
        if value > 2025:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value



# -----------------------------
# AuthorSerializer
# -----------------------------
class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.

    What it does:
    - Shows the author's name.
    - Also includes all books written by this author using the nested BookSerializer.

    How it works:
    - The 'related_books' field grabs all Book objects linked to this author.
      This works because the Book model has a ForeignKey to Author.
    - 'many=True' means there can be multiple books.
    - 'read_only=True' makes sure we’re just displaying books here,
      not creating or changing them through the AuthorSerializer.
    """
    related_books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'related_books']
