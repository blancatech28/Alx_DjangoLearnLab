from myapp.models import Book  # Import the model

Book.objects.get(title="Nineteen Eighty-Four").delete()  # Deletes the book

Book.objects.all()  # Expected output: <QuerySet []>
