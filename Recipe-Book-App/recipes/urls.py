from django.urls import path
from . import views

urlpatterns = [
    # Home/Recipe List
    path('', views.home, name='home'),
    
    # Recipe URLs
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/create/', views.recipe_create, name='recipe_create'),
    path('recipe/<int:pk>/update/', views.recipe_update, name='recipe_update'),
    path('recipe/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/<int:pk>/update/', views.category_update, name='category_update'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
