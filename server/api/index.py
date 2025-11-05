"""
Vercel serverless function entry point for Django application.
"""
import os
import sys

# Add server directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')
os.environ.setdefault('VERCEL', '1')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

