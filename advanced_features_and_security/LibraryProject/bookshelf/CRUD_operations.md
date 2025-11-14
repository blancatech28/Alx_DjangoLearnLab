from myapp.models import Book 


# Create Operation

# Create a new Book instance
book = Book.objects.create(title="1984", author="George Orwell", published_year=1949)
book



# Retrieve Operation

# Retrieve all Book instances as dictionaries
books = Book.objects.all().values()
books


# Update Operation

# Retrieve the book with title "1984"
book = Book.objects.get(title="1984")
# Update its title
book.title = "Nineteen Eighty-Four"
book.save()

# Confirm the update
updated_book = Book.objects.get(title="Nineteen Eighty-Four")
print(updated_book.title)
# Expected output: Nineteen Eighty-Four


# --- Delete ---
# Delete the book
Book.objects.get(title="Nineteen Eighty-Four").delete()
# Confirm deletion
books = Book.objects.all()
print(books)
# Expected output: <QuerySet []>
