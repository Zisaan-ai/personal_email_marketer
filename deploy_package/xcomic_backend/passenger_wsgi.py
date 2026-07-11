import sys
import os
import subprocess

# ================================================================
# passenger_wsgi.py — cPanel Passenger Entry Point
# Location: xcomic_backend/passenger_wsgi.py
# Auto-installs missing packages on first run (no SSH needed)
# ================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')

sys.path.insert(0, BACKEND_DIR)
sys.path.insert(0, BASE_DIR)

# ── AUTO PACKAGE INSTALLER ──────────────────────────────────────
REQUIRED_PACKAGES = [
    "fastapi",
    "uvicorn",
    "sqlalchemy",
    "pydantic",
    "python-multipart",
    "python-jose[cryptography]",
    "passlib[bcrypt]",
    "python-dotenv",
    "beautifulsoup4",
    "bcrypt<4.0.0",
    "google-generativeai",
    "apscheduler",
    "pytz",
    "requests",
    "a2wsgi",
]

def install_packages():
    log_file = os.path.join(BASE_DIR, 'install_log.txt')
    try:
        with open(log_file, 'w') as f:
            f.write("Starting package installation...\n")
            for pkg in REQUIRED_PACKAGES:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
                    capture_output=True,
                    text=True
                )
                status = "OK" if result.returncode == 0 else "FAILED"
                f.write(f"[{status}] {pkg}\n")
                if result.stderr:
                    f.write(f"       {result.stderr[:200]}\n")
            f.write("Done!\n")
    except Exception as e:
        with open(log_file, 'w') as f:
            f.write(f"Install error: {e}\n")

# Check if a2wsgi is installed (key package), if not — install all
try:
    import a2wsgi
except ImportError:
    install_packages()
    # Re-add paths after install
    sys.path.insert(0, BACKEND_DIR)
    sys.path.insert(0, BASE_DIR)

# ── LOAD ENV & START APP ────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

# Set database to absolute path (SQLite)
db_path = os.path.join(BACKEND_DIR, 'sql_app.db')
os.environ.setdefault('DATABASE_URL', f'sqlite:///{db_path}')

# Import FastAPI app
from main import app as asgi_app

# Convert ASGI (FastAPI) to WSGI (cPanel Passenger)
from a2wsgi import ASGIMiddleware
application = ASGIMiddleware(asgi_app)
