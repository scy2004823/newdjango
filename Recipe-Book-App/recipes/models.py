from django.db import models
from django.utils import timezone


class Category(models.Model):
    """
    Model for recipe categories (e.g., Breakfast, Lunch, Dinner, Dessert)
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Model for storing recipe information
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes')
    description = models.TextField(help_text="Brief description of the recipe")
    ingredients = models.TextField(help_text="List all ingredients (one per line)")
    instructions = models.TextField(help_text="Step-by-step cooking instructions")
    prep_time = models.IntegerField(help_text="Preparation time in minutes")
    cook_time = models.IntegerField(help_text="Cooking time in minutes")
    servings = models.IntegerField(default=4, help_text="Number of servings")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def total_time(self):
        """Calculate total cooking time"""
        return self.prep_time + self.cook_time
