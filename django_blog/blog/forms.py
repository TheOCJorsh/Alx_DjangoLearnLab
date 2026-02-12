from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Post

class UserRegisterForm(UserCreationForm):
    """
    Extends Django's UserCreationForm to include email field.
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """

    class Meta:
        model = User
        fields = ['username', 'email']


class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts.
    Author is set automatically from logged-in user.
    """
    class Meta:
        model = Post
        fields = ['title', 'content']