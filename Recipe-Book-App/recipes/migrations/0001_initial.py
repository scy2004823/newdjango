# Generated migration file
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(help_text='Brief description of the recipe')),
                ('ingredients', models.TextField(help_text='List all ingredients (one per line)')),
                ('instructions', models.TextField(help_text='Step-by-step cooking instructions')),
                ('prep_time', models.IntegerField(help_text='Preparation time in minutes')),
                ('cook_time', models.IntegerField(help_text='Cooking time in minutes')),
                ('servings', models.IntegerField(default=4, help_text='Number of servings')),
                ('difficulty', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium', max_length=10)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='recipes.category')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
