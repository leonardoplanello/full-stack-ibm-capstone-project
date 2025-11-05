"""
Vercel serverless function entry point for Django application.
This file must be named index.py and be in the api/ directory.
"""
import os
import sys
import traceback

# Set environment variables BEFORE any Django imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')
os.environ.setdefault('VERCEL', '1')

# Get the server directory path
api_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.dirname(api_dir)

# Add server directory to Python path
if server_dir not in sys.path:
    sys.path.insert(0, server_dir)

# Change to server directory to ensure relative paths work
os.chdir(server_dir)

# Now import Django with error handling
try:
    from django.core.wsgi import get_wsgi_application
    # Initialize Django application
    application = get_wsgi_application()
except Exception as e:
    # Fallback error handler with detailed error message
    error_trace = traceback.format_exc()
    
    def application(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, response_headers)
        error_html = f"""
        <html>
        <head><title>Django Initialization Error</title></head>
        <body>
        <h1>Django Initialization Error</h1>
        <pre>{str(e)}</pre>
        <h2>Traceback:</h2>
        <pre>{error_trace}</pre>
        </body>
        </html>
        """
        return [error_html.encode('utf-8')]
