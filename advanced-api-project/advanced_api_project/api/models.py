from django.db import models

# Author model represents a book writer.
# One Author can have MANY books (One-to-Many relationship).
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Book model represents a book written by an Author.
# Each book belongs to ONE author via ForeignKey.
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()

    # ForeignKey creates the one-to-many relationship
    # related_name='books' allows access like: author.books.all()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return self.title
