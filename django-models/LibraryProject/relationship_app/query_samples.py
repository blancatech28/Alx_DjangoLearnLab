from relationship_app.models import Author, Book, Library

# 1️ All books by a specific author
for book in Book.objects.filter(author__name="J.K. Rowling"):
    print(book.title)

# 2️ All books in a library
library = Library.objects.get(name="Central Library") 
for book in library.books.all():
    print(book.title)

# 3️ Librarian for a library (via library object)
print(library.librarian.name)
