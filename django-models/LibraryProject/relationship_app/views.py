import django
from django.shortcuts import render
from .models import Author, Book, Library, Librarian
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView


def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)


class DetailListView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['librarian'] = Librarian.objects.get(library=self.object)
        return context
