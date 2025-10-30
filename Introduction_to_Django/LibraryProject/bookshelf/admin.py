from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_year')
    search_fields = ('title', 'author')
    list_filter = ('published_year',)

    
admin.site.register(Book, BookAdmin)



# Register your models here.
