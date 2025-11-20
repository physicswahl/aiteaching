from django.apps import AppConfig


class SpeciesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'species'
    
    def ready(self):
        """Pre-load the model when Django starts"""
        import os
        if os.environ.get('RUN_MAIN') == 'true':  # Only run once in development server
            try:
                from .views import load_model_and_scalers
                print("Pre-loading species classification model...")
                load_model_and_scalers()
                print("Model loaded successfully!")
            except Exception as e:
                print(f"Warning: Could not pre-load model: {e}")

