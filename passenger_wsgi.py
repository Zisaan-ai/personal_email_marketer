import sys
import os

# ================================================================
# passenger_wsgi.py — cPanel Passenger Entry Point
# Location: xcomic_backend/passenger_wsgi.py
# ================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')

sys.path.insert(0, BACKEND_DIR)
sys.path.insert(0, BASE_DIR)

# Load .env from root folder
from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Set database to absolute path (SQLite)
db_path = os.path.join(BASE_DIR, 'mailclone.db')
os.environ.setdefault('DATABASE_URL', f'sqlite:///{db_path}')

# Import FastAPI app
from main import app as asgi_app

# Convert ASGI (FastAPI) to WSGI (cPanel Passenger)
from a2wsgi import ASGIMiddleware
application = ASGIMiddleware(asgi_app)
