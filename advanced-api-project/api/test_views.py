from django.urls import reverse
from .models import Book, Author
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class BookTest(APITestCase):
    def setUp(self):
        #  Create initial Author instance
        self.author = Author.objects.create(name="John Buddy")
        
        # Create initial Book linked to the Author instance
        Book.objects.create(title="Book One", author=self.author, publication_year=2001)

        #  Create a user for authenticated tests
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def authenticate(self):
        self.client.force_authenticate(user=self.user)
    
    #  Test that initial book exists
    def test_books_created(self):
        self.assertEqual(Book.objects.count(), 1)

    #  Test listing all books
    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Book One")
        self.assertEqual(response.data[0]['author'], "John Buddy")  # DRF serializer should return author name
        self.assertEqual(response.data[0]['publication_year'], 2001)

    # ✅ Test retrieving a single book
    def test_retrieve_book(self):
        book = Book.objects.first()
        url = reverse('book-detail', args=[book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Book One")
        self.assertEqual(response.data['author'], "John Buddy")
        self.assertEqual(response.data['publication_year'], 2001)

    # ✅ Test unauthenticated creation fails
    def test_create_book_unauthenticated(self):
        url = reverse('book-create')
        new_author = Author.objects.create(name="Jane Doe")  # Author must exist
        data = {
            'title': 'Book Two',
            'author': new_author.id,  # ✅ Pass ID
            'publication_year': 2020
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ✅ Test authenticated creation works
    def test_create_book_authenticated(self):
        self.authenticate()
        new_author = Author.objects.create(name="Jane Doe")  # Create new Author
        url = reverse('book-create')
        data = {
            'title': 'Book Two',
            'author': new_author.id,  # ✅ Pass ID
            'publication_year': 2020
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        book = Book.objects.get(title='Book Two')
        self.assertEqual(book.title, 'Book Two')
        self.assertEqual(book.author.name, 'Jane Doe')  # ✅ Compare author name
        self.assertEqual(book.publication_year, 2020)

    # ✅ Test unauthenticated update fails
    def test_update_book_unauthenticated(self):
        book = Book.objects.first()
        url = reverse('book-update', args=[book.id])
        data = {
            'title': 'Updated Book One',
            'author': self.author.id,  # ✅ Pass ID
            'publication_year': 2001
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ✅ Test authenticated update works
    def test_update_book_authenticated(self):
        self.authenticate()
        book = Book.objects.get(title="Book One")
        url = reverse('book-update', args=[book.id])
        data = {
            'title': 'Updated Book One',
            'author': self.author.id,  # ✅ Pass ID
            'publication_year': 2001
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, 'Updated Book One')
        self.assertEqual(book.author.name, 'John Buddy')  # ✅ Compare author name
        self.assertEqual(book.publication_year, 2001)

    # ✅ Test authenticated partial update works
    def test_partial_update_book_authenticated(self):
        self.authenticate()
        book = Book.objects.get(title="Book One")
        url = reverse('book-update', args=[book.id])
        data = {'title': 'Partially Updated Book One'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, 'Partially Updated Book One')
        self.assertEqual(book.author.name, 'John Buddy')  # ✅ Author unchanged
        self.assertEqual(book.publication_year, 2001)

    # ✅ Test unauthenticated delete fails
    def test_delete_book_unauthenticated(self):
        book = Book.objects.first()
        url = reverse('book-delete', args=[book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ✅ Test authenticated delete works
    def test_delete_book_authenticated(self):
        self.authenticate()
        book = Book.objects.first()
        url = reverse('book-delete', args=[book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
