from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book-list'),  # get all books
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),  # get one book
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),  # create new book
    path('books/update/', views.BookUpdateView.as_view(), name='book-update'),  # update book
    path('books/delete/', views.BookDeleteView.as_view(), name='book-delete'),  # delete book
]
