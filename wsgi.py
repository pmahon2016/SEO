"""
WSGI configuration for PythonAnywhere deployment
This file is used by WSGI servers to serve the application.
"""

import sys
import os

# Add your project directory to the sys.path
# Replace 'yourusername' with your actual PythonAnywhere username
project_home = '/home/yourusername/SEO-Analyser'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import the Flask app
from app import app as application

# This is required for PythonAnywhere
if __name__ == '__main__':
    application.run()

