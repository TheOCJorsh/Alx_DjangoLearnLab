from django.shortcuts import render,redirect
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib import messages



def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})

# Role base functions
def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and user.userprofile.role == 'Member'

# Role-based views
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# permission protection to add book
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    return render(request, 'relationship_app/add_book.html')

# permission protection to edit book
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    return render(request, 'relationship_app/edit_book.html', {'book_id': book_id})

# permission protection to delete book
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    return render(request, 'relationship_app/delete_book.html', {'book_id': book_id})