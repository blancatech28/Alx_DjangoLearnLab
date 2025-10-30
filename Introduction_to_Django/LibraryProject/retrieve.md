# Retrieve Operation

```python
from bookshelf.models import Book

# Retrieve all Book instances as dictionaries
books = Book.objects.all().values()
books
