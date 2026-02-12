from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Post model represents a blog article written by a user.
    Each user can write multiple posts.
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    tags = TaggableManager()  # Using django-taggit for tagging functionality


    def __str__(self):
        return self.title

class Comment(models.Model):
    """
    Model representing a comment made on a blog post.
    Each comment belongs to a post and a user.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

