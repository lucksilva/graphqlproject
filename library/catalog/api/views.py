from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django_filters import rest_framework as filters
from catalog.models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from catalog.filters import BookFilter

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter   
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
