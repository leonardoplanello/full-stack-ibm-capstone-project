"""
Vercel serverless function entry point for Django application.
This file must be named index.py and be in the api/ directory.
"""
import os
import sys

# Set environment variables BEFORE any Django imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')
os.environ.setdefault('VERCEL', '1')

# Get the server directory path
api_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.dirname(api_dir)

# Add server directory to Python path
if server_dir not in sys.path:
    sys.path.insert(0, server_dir)

# Now import Django with error handling
try:
    from django.core.wsgi import get_wsgi_application
    # Initialize Django application
    application = get_wsgi_application()
except Exception as e:
    # Fallback error handler
    import logging
    logging.basicConfig(level=logging.ERROR)
    logging.error(f"Django initialization error: {str(e)}")
    
    def application(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [f'Django initialization error: {str(e)}'.encode()]
