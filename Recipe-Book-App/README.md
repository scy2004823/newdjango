# Recipe Book App

A simple Django web application for managing recipes. Made with a fun retro 90s style interface.

## What it does

This is a basic recipe manager where you can add, edit, and delete recipes. You can organize them by categories like Breakfast, Lunch, Dinner, etc. There's also a search feature to find recipes by name or ingredients.

## Features

- Add new recipes with ingredients and cooking instructions
- Edit and delete recipes
- Create categories to organize recipes
- Search recipes by keywords
- Filter by category
- Track prep time, cook time, and servings
- Set difficulty levels

## Tech Stack

- Django 4.2
- SQLite database
- Pure HTML and CSS (no Bootstrap, just 90s vibes)
- Python 3.8+

## How to install

First, clone this repo if you haven't:

```bash
git clone https://github.com/AdityaDwiNugroho/Django-Projects-for-beginners.git
cd Django-Projects-for-beginners/Recipe-Book-App
```

Create a virtual environment (recommended):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Install Django:

```bash
pip install -r requirements.txt
```

Run the migrations to set up the database:

```bash
python manage.py migrate
```

Optionally create an admin user:

```bash
python manage.py createsuperuser
```

Start the server:

```bash
python manage.py runserver
```

Open your browser and go to `http://127.0.0.1:8000/`

That's it. You're done.

## How to use

1. Click "ADD RECIPE" to create your first recipe
2. Fill in the title, description, ingredients, and cooking steps
3. Choose a category or create a new one
4. Set the prep time, cook time, and difficulty
5. Save it

The home page shows all your recipes. Click on any recipe to see the full details. You can edit or delete recipes from the detail page.

## Project Structure

```
Recipe-Book-App/
├── manage.py
├── requirements.txt
├── recipe_project/        # Main project settings
├── recipes/               # Main app with models and views
└── templates/             # HTML templates
```

## What I learned making this

- Django models and relationships (ForeignKey)
- Function-based views
- Template inheritance
- Forms and form validation
- URL routing
- Database queries with filter and search
- The Django admin panel

## Future ideas

If I come back to this, I might add:

- User accounts so everyone can have their own recipes
- Recipe ratings
- Photo uploads
- Print view
- Recipe import/export
- Shopping list generator

## Contributing

Feel free to fork this and make it better. If you find bugs or have suggestions, open an issue.

## License

This project is open source under the MIT License.

## Credits

Made for Hacktoberfest 2025 as part of the Django-Projects-for-beginners collection.

The retro 90s design is intentional and brings back memories of the early web.

