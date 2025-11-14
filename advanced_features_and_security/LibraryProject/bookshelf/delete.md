from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book.delete()

Book.objects.all()  # Expected output: <QuerySet []>
