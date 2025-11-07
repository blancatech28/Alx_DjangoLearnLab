from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
books = Book.objects.filter(author__name="Author Name")
for b in books: 
    print(b.title) 

# List all books in a library
library = Library.objects.get(name="Library Name") 
for b in library.books.all(): 
    print(b.title) 

# Retrieve the librarian for a library
library = Library.objects.get(name="Library Name")
librarian = library.librarian
print(librarian.name)



