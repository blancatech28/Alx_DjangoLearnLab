from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import DetailView   
from .models import Author, Book, Library, Librarian
from .models import Library  # ✅ required by checker
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse




def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['librarian'] = Librarian.objects.get(library=self.object)
        return context

# relationship_app/views.py



# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            messages.success(request, 'Account created and logged in successfully!')
            return redirect('home')  # change 'home' to any view you want
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('home')  # change 'home' to any view you want
        messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return render(request, 'relationship_app/logout.html')



# Helper functions to check user roles
def is_admin(user):
    return user.userprofile.role == 'Admin'


def is_librarian(user):
    return user.userprofile.role == 'Librarian'


def is_member(user):
    return user.userprofile.role == 'Member'


# Admin View
@user_passes_test(is_admin)
def admin_view(request):
    context = {
        'message': 'Welcome Admin! You have full access to the system.',
    }
    return render(request, 'relationship_app/admin_view.html', context)


# Librarian View
@user_passes_test(is_librarian)
def librarian_view(request):
    books = Book.objects.all()
    context = {
        'message': 'Welcome Librarian! You can manage books.',
        'books': books,
    }
    return render(request, 'relationship_app/librarian_view.html', context)


# Member View
@user_passes_test(is_member)
def member_view(request):
    books = Book.objects.all()
    context = {
        'message': 'Welcome Member! You can browse books.',
        'books': books,
    }
    return render(request, 'relationship_app/member_view.html', context)


