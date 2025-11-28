from django.shortcuts import render
from .serializers import BookSerializer, AuthorSerializer
from .models import Book, Author
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

# -----------------------------
# Custom Pagination Class
# -----------------------------
class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination settings:
    - Default page size: 10
    - Allow clients to set custom page size using 'page_size' query parameter
    - Maximum page size limit: 100
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# -----------------------------
# List All Books
# -----------------------------
class BooklistView(generics.ListAPIView):
    """
    API endpoint to list all books with support for:
    - Search by title or author's name
    - Ordering by title or publication year
    - Filtering by publication year
    - Filtering by publication year range (min_year and max_year query params)
    - Pagination with custom settings
    - Open access (AllowAny)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'author']
    ordering_fields = ['publication_year', 'title']
    filterset_fields = ['title', 'author','publication_year']
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        """
        Optionally restrict the returned books based on:
        - author__name: partial case-insensitive match
        - min_year: books published after or in this year
        - max_year: books published before or in this year
        Query params:
        ?author__name=<name>&min_year=<year>&max_year=<year>
        """
        queryset = super().get_queryset()

        # Filter by author name if provided
        author_name = self.request.query_params.get('author__name', None)
        if author_name:
            queryset = queryset.filter(author__name__icontains=author_name)

        # Filter by minimum publication year if provided
        min_year = self.request.query_params.get('min_year', None)
        if min_year:
            queryset = queryset.filter(publication_year__gte=min_year)

        # Filter by maximum publication year if provided
        max_year = self.request.query_params.get('max_year', None)
        if max_year:
            queryset = queryset.filter(publication_year__lte=max_year)

        return queryset


# -----------------------------
# Create a New Book
# -----------------------------
class BookCreateView(generics.CreateAPIView):
    """
    API endpoint to create a new Book record.
    - Only accessible to authenticated users
    - Uses BookSerializer for validation and serialization
    - Returns a custom success message with created book data
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Override default create() to return a custom success message.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Book created successfully!",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


# -----------------------------
# Update an Existing Book
# -----------------------------
class BookUpdateView(generics.UpdateAPIView):
    """
    API endpoint to update an existing Book.
    - Only accessible to authenticated users
    - Supports partial updates (PATCH)
    - Uses BookSerializer for validation
    - Uses 'id' field as lookup instead of default 'pk'
    - Returns a custom success message with updated book data
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        Override default update() to include a custom message.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": "Book updated successfully!",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# -----------------------------
# Delete a Book
# -----------------------------
class BookDeleteView(generics.DestroyAPIView):
    """
    API endpoint to delete a Book.
    - Only accessible to authenticated users
    - Uses 'id' field for lookup
    - Returns a custom success message after deletion
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """
        Override default destroy() to return a custom message.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Book deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT
        )
