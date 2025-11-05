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

# Store error for later use
_init_error = None
_init_traceback = None

# Now import Django with error handling
try:
    from django.core.wsgi import get_wsgi_application
    # Initialize Django application
    application = get_wsgi_application()
except Exception as e:
    # Store error details
    _init_error = str(e)
    _init_traceback = traceback.format_exc()
    
    # Log error
    import logging
    logging.basicConfig(level=logging.ERROR)
    logging.error(f"Django initialization error: {_init_error}")
    logging.error(_init_traceback)
    
    # Create error handler
    def application(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, response_headers)
        error_html = f"""
        <html>
        <head><title>Django Initialization Error</title></head>
        <body>
        <h1>Django Initialization Error</h1>
        <p><strong>Error:</strong> {_init_error}</p>
        <h2>Traceback:</h2>
        <pre>{_init_traceback}</pre>
        </body>
        </html>
        """
        return [error_html.encode('utf-8')]
