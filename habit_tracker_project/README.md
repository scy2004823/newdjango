# Habit Tracker (Django)
Simple Django app to create and log daily habits. Features:
- Create, update, delete habits
- Log habit completion for dates
- Simple dashboard with streak and recent logs

## Run locally
1. python -m venv .venv
2. source .venv/bin/activate   # or .venv\Scripts\activate on Windows
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py createsuperuser
6. python manage.py runserver

Open http://127.0.0.1:8000/