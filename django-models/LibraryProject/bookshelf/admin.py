from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    # Columns to display in the list view
    list_display = ('title', 'author', 'publication_year')

    # Add filters on the right sidebar
    list_filter = ('author', 'publication_year')

    # Enable search functionality
    search_fields = ('title', 'author')
admin.site.register(Book, BookAdmin)