from .views import list_books, DetailListView
from django.urls import path

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('books/<int:pk>/', DetailListView.as_view(), name='library_detail'),
]
