from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
    
    # Optional: extra validation example
    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        if year < 0 or year > 2100:
            raise forms.ValidationError("Please enter a valid year.")
        return year
 
    
# Dummy form just to satisfy the "ExampleForm" requirement
class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
