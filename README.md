# AI Teaching Platform

An interactive educational website demonstrating AI and machine learning concepts through visualizations and animations.

## Features

- Interactive neural network visualizations
- Student classification demonstrations
- Species classification with real data
- Word embeddings visualization
- Large Language Model concepts
- OCR neural network applications

## Tech Stack

- **Backend**: Django 5.2.8
- **ML/AI**: TensorFlow, Keras, scikit-learn
- **Animations**: Manim Community Edition
- **Database**: SQLite (suitable for educational/demo purposes)
- **Frontend**: HTML5, CSS3, JavaScript (Canvas API)

## Prerequisites

- Python 3.10 or higher
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Manim
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Unix/MacOS:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py migrate
```

5. Load initial data (student data for demonstrations):
```bash
python manage.py loaddata demo/fixtures/students.json
```

6. Download the pre-trained species classification model:
   - Place the model files in `species/model/` directory:
     - `species_classification_model.keras`
     - `scaler1.pkl`
     - `scaler2.pkl`

## Development vs Production

### Development (Local):
- `.env`: `DEBUG=True`, `ALLOWED_HOSTS=localhost,127.0.0.1`
- Run: `python manage.py runserver`
- Database: Local `db.sqlite3`

### Production:
- `.env`: `DEBUG=False`, `ALLOWED_HOSTS=yourdomain.com`
- Run: `gunicorn aiteaching.wsgi`
- HTTPS enforced automatically
- Security headers enabled
- Static files served from `staticfiles/`

## Running the Application

### Development Server
Start the development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Project Structure

```
Manim/
├── aiteaching/          # Main Django project settings
├── demo/                # Demo app with visualizations
│   ├── manim_animations/    # Manim animation scripts
│   ├── static/demo/         # Static files (videos, images)
│   └── templates/demo/      # HTML templates
├── species/             # Species classification app
│   ├── model/              # ML model files
│   └── templates/species/  # Species visualization templates
├── manage.py
└── requirements.txt
```

## Production Deployment

### Security Checklist ✓

**Completed:**
1. ✓ Environment variables configured (`.env` file)
2. ✓ SECRET_KEY uses environment variable
3. ✓ DEBUG controlled by environment variable
4. ✓ ALLOWED_HOSTS configured
5. ✓ STATIC_ROOT configured for static file collection
6. ✓ Security headers enabled (HTTPS, HSTS, XSS protection)
7. ✓ Database file in `.gitignore`
8. ✓ `.env` file in `.gitignore`
9. ✓ Gunicorn added for production server
10. ✓ python-dotenv added for environment variables

**Before deploying:**

1. **Generate a new SECRET_KEY:**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Copy the output and update `SECRET_KEY` in your `.env` file.

2. **Update `.env` for production:**
   ```
   SECRET_KEY=<paste-new-key-here>
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

3. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

4. **Run migrations on production:**
   ```bash
   python manage.py migrate
   ```

5. **Create admin user (optional):**
   ```bash
   python manage.py createsuperuser
   ```
   **Note:** If you don't need admin access, consider disabling the admin URL in production.

6. **Test with Gunicorn locally:**
   ```bash
   gunicorn aiteaching.wsgi
   ```

### Deployment Options

**Heroku:**
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

**Railway/Render/DigitalOcean:**
- Connect your GitHub repository
- Set environment variables in their dashboard
- Add build command: `pip install -r requirements.txt`
- Add start command: `gunicorn aiteaching.wsgi`

### Database
SQLite is suitable for this application with ~30 concurrent users because:
- Database writes are minimal (read-heavy workload)
- Student data is static/demonstration only
- No complex transactions or concurrent writes
- Simple deployment without separate database server

For higher concurrent usage (100+ users), consider PostgreSQL.

### Admin Panel Security

The Django admin is enabled at `/admin/`. For production:
- **Option 1:** Change the admin URL to something obscure in `urls.py`
- **Option 2:** Remove admin URL entirely if not needed
- **Option 3:** Use strong passwords and limit access by IP

### Static Files
In production, static files are collected to `staticfiles/` directory:
```bash
python manage.py collectstatic
```

Consider using a CDN or cloud storage (AWS S3, Cloudflare) for better performance.

## Development vs Production

### Development (Local):


## Navigation Flow

1. Start → Student Plot → Two Nodes → Video Explanation
2. Conclusions One → Five Nodes → Species Classifier
3. OCR Image → Transition → Word Vectors
4. Anthropic → LLM → Conclusions Two → Teaching

## Contributing

This is an educational project. Feel free to fork and adapt for your teaching needs.

## License

[Specify your license here]

## Acknowledgments

- Manim Community for animation library
- TensorFlow/Keras teams
- Educational resources and datasets used
