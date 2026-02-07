from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from django_filters import rest_framework as filters  # for exact filtering
from rest_framework import filters as drf_filters  # for search and ordering

class BookListView(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    Anyone can access (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer  # use BookSerializer to convert to json

    # filtering stuff - not sure how all this works but it does
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]

    # these let you filter by exact values
    filterset_fields = ['title', 'author', 'publication_year']

    # these let you search with partial matches
    search_fields = ['title', 'author__name']  # author__name goes to related model

    # these let you sort the results
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # books sorted by title by default
    
class BookDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve details of a single book by ID.
    Anyone can access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    """
    API view to create a new book.
    Only authenticated users can create.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing book.
    Only authenticated users can update.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    """
    API view to delete a book.
    Only authenticated users can delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
