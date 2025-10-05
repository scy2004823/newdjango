# Rock Paper Scissors Django Game

A clean, minimal, and fun Rock Paper Scissors web game built with Django. Features both manual play and autoplay modes with comprehensive statistics tracking.

![Game Preview](game_preview.png)

## Features

- 🎮 **Manual Play Mode**: Play against the computer
- 🤖 **Autoplay Mode**: Watch computer vs computer simulation
- 📊 **Statistics Tracking**: Win/loss/draw ratios and percentages
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- 🎨 **Clean UI**: Flat design with custom SVG icons
- ⚡ **Real-time Updates**: AJAX-powered gameplay
- 🔄 **Game History**: Track recent games
- 📈 **Admin Interface**: Manage games through Django admin

## Project Structure

```
rock_paper_scissors/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── rps_game/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── game/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── migrations/
    ├── templates/game/
    │   └── index.html
    └── static/game/
        ├── css/
        │   └── style.css
        └── icons/
            ├── rock.svg
            ├── paper.svg
            └── scissors.svg
```

## Prerequisites

Before running this project, make sure you have:

- **Python 3.8+** installed on your system
- **pip** (Python package installer)
- **Git** (optional, for cloning)

### Check if Python is installed:
```bash
python --version
# or
python3 --version
```

### Check if pip is installed:
```bash
pip --version
# or
pip3 --version
```

## Installation & Setup

### Quick Start (Recommended for Beginners)

**On Windows:**
1. Download the project
2. Double-click `setup_and_run.bat`
3. Wait for the setup to complete
4. Your browser will open automatically at `http://127.0.0.1:8000/`

**On macOS/Linux:**
1. Download the project
2. Open terminal in the project folder
3. Run: `chmod +x setup_and_run.sh && ./setup_and_run.sh`
4. Your browser will open automatically at `http://127.0.0.1:8000/`

### Manual Setup

### 1. Clone or Download the Project

**Option A: Clone with Git**
```bash
git clone <repository-url>
cd rock_paper_scissors
```

**Option B: Download ZIP**
- Download the project ZIP file
- Extract it to your desired location
- Navigate to the project folder

### 2. Create a Virtual Environment (Recommended)

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

```bash
# Create database tables
python manage.py migrate

# Create an admin user (optional)
python manage.py createsuperuser
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

The game will be available at: **http://127.0.0.1:8000/**

## How to Play

### Manual Mode
1. Open your web browser and go to `http://127.0.0.1:8000/`
2. Click on **"Manual Play"** tab (default)
3. Choose your weapon: Rock, Paper, or Scissors
4. See the computer's choice and the result
5. Click **"Play Again"** to continue

### Autoplay Mode
1. Click on the **"Autoplay Mode"** tab
2. Set the number of rounds (1-100)
3. Set the speed in milliseconds (100-5000ms)
4. Click **"Start Autoplay"** to watch computer vs computer
5. Click **"Stop Autoplay"** to halt the simulation

### Game Rules
- **Rock** beats **Scissors**
- **Scissors** beats **Paper** 
- **Paper** beats **Rock**
- Same choices result in a **Draw**

## Features Explained

### Statistics Tracking
- **Total Games**: Number of games played
- **Wins**: Games won by player/computer1
- **Losses**: Games lost by player/computer1
- **Draws**: Tied games
- **Win Rate**: Percentage of games won

### Reset Statistics
Click the **"Reset Statistics"** button to clear all game history and statistics.

### Admin Interface
Access the Django admin at `http://127.0.0.1:8000/admin/` to:
- View detailed game sessions
- Manage statistics
- Monitor game history

## Customization

### Changing Colors
Edit `game/static/game/css/style.css` to modify colors:
```css
/* Example: Change primary button color */
.choice-btn:hover {
    border-color: #your-color;
    background-color: #your-bg-color;
}
```

### Modifying Icons
Replace SVG files in `game/static/game/icons/` with your own designs.

### Adding Features
- Models: Edit `game/models.py`
- Views: Edit `game/views.py`
- Templates: Edit `game/templates/game/index.html`
- URLs: Edit `game/urls.py`

## Troubleshooting

### Common Issues

**1. "django-admin not found" error:**
```bash
# Install Django first
pip install django
```

**2. "Port already in use" error:**
```bash
# Use a different port
python manage.py runserver 8001
```

**3. "No module named 'game'" error:**
```bash
# Make sure you're in the correct directory
cd rock_paper_scissors
python manage.py runserver
```

**4. Database errors:**
```bash
# Reset database
python manage.py migrate --run-syncdb
```

**5. Static files not loading:**
```bash
# Collect static files (for production)
python manage.py collectstatic
```

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed: `pip list`
2. Ensure you're in the correct directory
3. Verify Python version compatibility
4. Check the Django documentation: https://docs.djangoproject.com/

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Checking for Issues
```bash
python manage.py check
```

## Deployment

For production deployment:

1. **Set DEBUG to False** in `settings.py`
2. **Configure ALLOWED_HOSTS** in `settings.py`
3. **Use a production database** (PostgreSQL, MySQL)
4. **Collect static files**: `python manage.py collectstatic`
5. **Use a WSGI server** like Gunicorn
6. **Set up a reverse proxy** with Nginx

## Technologies Used

- **Backend**: Django 5.2.7
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite (development)
- **Icons**: Custom SVG graphics
- **Styling**: CSS Grid, Flexbox

## File Descriptions

- `manage.py`: Django's command-line utility
- `requirements.txt`: Python dependencies
- `rps_game/settings.py`: Django configuration
- `game/models.py`: Database models
- `game/views.py`: Game logic and API endpoints
- `game/templates/game/index.html`: Main game interface
- `game/static/game/css/style.css`: Styling and layout
- `game/static/game/icons/`: SVG game icons

## License

This project is open-source and available under the MIT License.

## Contributing

Feel free to contribute by:
1. Forking the repository
2. Creating a feature branch
3. Making your changes
4. Submitting a pull request

## Author

Created as a beginner-friendly Django project for learning web development.

---

**Happy Gaming! 🎮**