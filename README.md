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

## Running the Application

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

## Production Considerations

### Database
SQLite is suitable for this application with ~30 concurrent users because:
- Database writes are minimal (read-heavy workload)
- Student data is static/demonstration only
- No complex transactions or concurrent writes
- Simple deployment without separate database server

For higher concurrent usage (100+ users), consider PostgreSQL.

### Static Files
In production, collect static files:
```bash
python manage.py collectstatic
```

### Security
Before deploying:
1. Set `DEBUG = False` in settings
2. Configure `ALLOWED_HOSTS`
3. Use environment variables for sensitive settings
4. Generate a new `SECRET_KEY`
5. Use HTTPS

### Recommended Hosting
- Heroku (with SQLite addon or PostgreSQL)
- PythonAnywhere
- Railway
- DigitalOcean App Platform

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
