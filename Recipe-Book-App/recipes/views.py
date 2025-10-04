from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Recipe, Category
from .forms import RecipeForm, CategoryForm


def home(request):
    """
    Home page view - displays all recipes with search functionality
    """
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    recipes = Recipe.objects.all()
    
    # Search functionality
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(ingredients__icontains=search_query)
        )
    
    # Category filter
    if category_filter:
        recipes = recipes.filter(category__id=category_filter)
    
    categories = Category.objects.all()
    
    context = {
        'recipes': recipes,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_filter,
    }
    return render(request, 'recipes/home.html', context)


def recipe_detail(request, pk):
    """
    Display detailed view of a single recipe
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    # Split ingredients by newline for better display
    ingredients_list = recipe.ingredients.split('\n')
    context = {
        'recipe': recipe,
        'ingredients_list': ingredients_list,
    }
    return render(request, 'recipes/recipe_detail.html', context)


def recipe_create(request):
    """
    Create a new recipe
    """
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            messages.success(request, f'Recipe "{recipe.title}" created successfully!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/recipe_form.html', {'form': form, 'action': 'Create'})


def recipe_update(request, pk):
    """
    Update an existing recipe
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            recipe = form.save()
            messages.success(request, f'Recipe "{recipe.title}" updated successfully!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'recipes/recipe_form.html', {'form': form, 'action': 'Update', 'recipe': recipe})


def recipe_delete(request, pk):
    """
    Delete a recipe
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    
    if request.method == 'POST':
        recipe_title = recipe.title
        recipe.delete()
        messages.success(request, f'Recipe "{recipe_title}" deleted successfully!')
        return redirect('home')
    
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})


def category_list(request):
    """
    Display all categories
    """
    categories = Category.objects.all()
    return render(request, 'recipes/category_list.html', {'categories': categories})


def category_create(request):
    """
    Create a new category
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'recipes/category_form.html', {'form': form, 'action': 'Create'})


def category_update(request, pk):
    """
    Update an existing category
    """
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'recipes/category_form.html', {'form': form, 'action': 'Update', 'category': category})


def category_delete(request, pk):
    """
    Delete a category
    """
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('category_list')
    
    return render(request, 'recipes/category_confirm_delete.html', {'category': category})
