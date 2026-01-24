"""
Custom Permissions & Groups (bookshelf app)
Permissions:
- can_view
- can_create
- can_edit
- can_delete
Groups:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: all permissions
Views are protected using @permission_required.
"""

from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
]