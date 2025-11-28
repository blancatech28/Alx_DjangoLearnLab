from .views import BooklistView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView
from django.urls import path

urlpatterns = [
    path('books/', BooklistView.as_view(), name='book-list'),
    path('books/<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:id>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:id>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
