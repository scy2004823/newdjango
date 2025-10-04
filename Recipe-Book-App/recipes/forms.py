from django import forms
from .models import Recipe, Category


class RecipeForm(forms.ModelForm):
    """
    Form for creating and editing recipes
    """
    class Meta:
        model = Recipe
        fields = ['title', 'category', 'description', 'ingredients', 'instructions', 
                  'prep_time', 'cook_time', 'servings', 'difficulty']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter recipe title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'List ingredients (one per line)'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Step-by-step instructions'}),
            'prep_time': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'cook_time': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    """
    Form for creating and editing categories
    """
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}),
        }
