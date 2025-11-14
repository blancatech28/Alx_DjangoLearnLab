from myapp.models import Book

# Retrieve the book with title "1984"
book = Book.objects.get(title="1984")
book

# Expected output: 1984 George Orwell 1949

