import requests
import base64
import json
import os

def check_is_float_and_convert(value):
    """
    Check if a string can be converted to a float and if so, return the float value.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def upload_image_to_imgbb(base64_image):
    """
    Mock function to simulate uploading an image to imgbb.
    In a real application, this would upload the image to imgbb and return the URL.
    
    For testing, we just return one of our sample urls.
    """
    # Sample pet-related image URLs to use as fallbacks
    sample_urls = [
        "https://images.unsplash.com/photo-1587559070757-f72a388edbba?w=300&h=300&fit=crop",
        "https://images.unsplash.com/photo-1561948955-570b270e7c36?w=300&h=300&fit=crop",
        "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=300&h=300&fit=crop",
        "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=300&h=300&fit=crop",
        "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=300&h=300&fit=crop"
    ]
    
    # Return a random sample URL
    import random
    return random.choice(sample_urls)

def is_url_valid(url):
    """
    Check if a URL is valid and accessible.
    """
    try:
        response = requests.head(url, timeout=3)
        return response.status_code == 200
    except:
        return False

def get_fallback_image_url(category=None):
    """
    Provide a fallback image URL for a specific category.
    """
    category_fallbacks = {
        'dog-food': 'https://images.unsplash.com/photo-1585846888097-620867d3149d?w=300&h=300&fit=crop',
        'cat-food': 'https://images.unsplash.com/photo-1604542031658-5799ca5d7936?w=300&h=300&fit=crop',
        'dog-toy': 'https://images.unsplash.com/photo-1546975490-e8b92a360b24?w=300&h=300&fit=crop',
        'cat-toy': 'https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=300&h=300&fit=crop',
        'dog-medicine': 'https://images.unsplash.com/photo-1598133894008-61f7fdb8cc3a?w=300&h=300&fit=crop',
        'cat-medicine': 'https://images.unsplash.com/photo-1606851091851-e8c8c0fca5ba?w=300&h=300&fit=crop',
    }
    
    if category and category in category_fallbacks:
        return category_fallbacks[category]
    else:
        # Generic pet product image
        return 'https://images.unsplash.com/photo-1535930891776-0c2dfb7fda1a?w=300&h=300&fit=crop'