import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, ".env"))

db_path = os.path.join(BASE_DIR, "sql_app.db")
os.environ.setdefault("DATABASE_URL", f"sqlite:///{db_path}")

import database
import json

def check_db():
    db = database.SessionLocal()
    accounts = db.query(database.SendingAccount).all()
    out = []
    for a in accounts:
        out.append({
            "email": a.email,
            "is_active": a.is_active,
            "auto_paused": a.auto_paused,
            "auto_paused_reason": getattr(a, 'auto_paused_reason', 'N/A'),
            "health_score": a.health_score,
            "sent_today": a.sent_today,
            "daily_limit": a.daily_limit
        })
    print(json.dumps(out, indent=2))
    
    camps = db.query(database.Campaign).all()
    for c in camps:
        pending = db.query(database.CampaignLead).filter(database.CampaignLead.campaign_id == str(c.id), database.CampaignLead.status == "pending").count()
        print(f"Camp {c.id} - status: {c.status} - pending leads: {pending}")

if __name__ == "__main__":
    check_db()
