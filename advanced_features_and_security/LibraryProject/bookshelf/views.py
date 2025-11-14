from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book

# Views are protected with permission_required decorators
# Users must have the correct permission to access these views

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})



@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        year = request.POST.get('publication_year', '').strip()

        # Basic input validation
        if not title or not author or not year.isdigit():
            return render(request, 'bookshelf/book_form.html', {
                'error': 'Invalid input.'
            })

        Book.objects.create(
            title=title,
            author=author,
            publication_year=int(year)
        )
        return redirect('book_list')

    return render(request, 'bookshelf/book_form.html')



@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        year = request.POST.get('publication_year', '').strip()

        if not title or not author or not year.isdigit():
            return render(request, 'bookshelf/book_form.html', {
                'book': book,
                'error': 'Invalid input.'
            })

        book.title = title
        book.author = author
        book.publication_year = int(year)
        book.save()
        return redirect('book_list')

    return render(request, 'bookshelf/book_form.html', {'book': book})






@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# Create your views here.
