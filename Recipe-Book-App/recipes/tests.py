from django.test import TestCase
from django.urls import reverse
from .models import Category, Recipe


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(str(self.category), "Test Category")


class RecipeModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Dessert")
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            category=self.category,
            description="Test description",
            ingredients="Ingredient 1\nIngredient 2",
            instructions="Step 1\nStep 2",
            prep_time=10,
            cook_time=20,
            servings=4,
            difficulty="easy"
        )

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.title, "Test Recipe")
        self.assertEqual(str(self.recipe), "Test Recipe")
        self.assertEqual(self.recipe.total_time, 30)


class RecipeViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Breakfast")
        self.recipe = Recipe.objects.create(
            title="Pancakes",
            category=self.category,
            description="Delicious pancakes",
            ingredients="Flour\nEggs\nMilk",
            instructions="Mix and cook",
            prep_time=5,
            cook_time=10,
            servings=2,
            difficulty="easy"
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pancakes")

    def test_recipe_detail(self):
        response = self.client.get(reverse('recipe_detail', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pancakes")
