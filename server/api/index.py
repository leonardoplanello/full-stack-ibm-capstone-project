"""
Vercel serverless function entry point for Django application.
"""
import os
import sys

# Get the directory paths
current_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(server_dir)

# Add server directory to Python path
if server_dir not in sys.path:
    sys.path.insert(0, server_dir)

# Set environment variables BEFORE importing Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')
os.environ.setdefault('VERCEL', '1')
os.environ.setdefault('PYTHONPATH', server_dir)

# Change to server directory to ensure relative imports work
os.chdir(server_dir)

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Initialize Django
application = get_wsgi_application()


