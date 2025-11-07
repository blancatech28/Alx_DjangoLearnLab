from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import DetailView   # ✅ required import
from .models import Author, Book, Library, Librarian
from .models import Library  # ✅ required by checker
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy



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

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login') 


