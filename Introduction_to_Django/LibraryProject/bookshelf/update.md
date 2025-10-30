# Update Operation

```python
from bookshelf.models import Book

# Retrieve the book with title "1984"
book = Book.objects.get(title="1984")

# Update its title
book.title = "Nineteen Eighty-Four"
book.save()


