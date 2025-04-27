from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'BirdCareSecretKey123'  # Secret key for session management
    
    # Import and register blueprints
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # Create directories for images if they don't exist
    ensure_directories()
    
    return app

def ensure_directories():
    """Ensure all necessary directories exist"""
    # Define paths relative to this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Directories to ensure
    directories = [
        os.path.join(base_dir, 'static', 'img'),
        os.path.join(base_dir, 'static', 'img', 'banner'),
        os.path.join(base_dir, 'static', 'img', 'mfp'),
        os.path.join(base_dir, 'static', 'css')
    ]
    
    # Create directories if they don't exist
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

