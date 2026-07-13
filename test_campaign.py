import os
import sys

# setup django/fastapi environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))
os.environ.setdefault('DATABASE_URL', f"sqlite:///{os.path.join(BACKEND_DIR, 'sql_app.db')}")

import database
from main import process_isolated_campaign

campaign_id = 'a30c4150-1f85-438a-a303-bacd36ab07ef'
process_isolated_campaign(campaign_id)
