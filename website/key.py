"""
This file contains placeholder keys and configuration values.
In a real application, sensitive values like these would be stored in environment variables.
"""

# API key for image hosting service
def get_imgbb_api_key():
    # In production, this should be retrieved from environment variables
    # Example: return os.environ.get('IMGBB_API_KEY')
    return 'placeholder_api_key'

# Additional configuration values
DB_CONFIG = {
    'host': 'localhost',
    'user': 'dummy_user',
    'password': 'dummy_password',
    'database': 'pet_zilla'
}

# Secret key for Flask session
SECRET_KEY = "petzilla_secret_key_123"
