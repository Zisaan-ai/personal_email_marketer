import sys
import os
sys.path.append(os.path.abspath('C:/Users/higan/.gemini/antigravity/scratch/xcomic_sync/xcomic_backend'))
os.environ['DATABASE_URL'] = 'sqlite:///C:/Users/higan/.gemini/antigravity/scratch/xcomic_sync/sql_app_live.db'

from sqlalchemy.orm import Session
import database

def test():
    db = database.SessionLocal()
    accounts = db.query(database.SendingAccount).filter(database.SendingAccount.user_id == 'fe8b7aa0-5028-4091-8220-2cf526f79662').all()
    result = []
    for acc in accounts:
        domain = acc.email.split('@')[-1] if '@' in acc.email else ''
        domain_cache = db.query(database.DomainHealthCache).filter(database.DomainHealthCache.domain == domain).first() if domain else None

        result.append({
            "id": str(acc.id),
            "name": acc.name,
            "email": acc.email,
            "health_score": acc.health_score,
            "daily_limit": acc.daily_limit,
            "sent_today": acc.sent_today,
            "is_active": acc.is_active,
            "provider": acc.provider,
            "smart_warmup_enabled": getattr(acc, "smart_warmup_enabled", False),
            "smart_limit_enabled": getattr(acc, "smart_limit_enabled", False),
            "warmup_enabled": getattr(acc, "warmup_enabled", False),
            "domain_health": domain_cache.domain_health if domain_cache else 100,
            "domain_spam_rate": domain_cache.spam_rate if domain_cache else 0.0,
            "domain_inbox_rate": domain_cache.inbox_rate if domain_cache else 100.0,
            "domain_placement": domain_cache.inbox_placement if domain_cache else "Good"
        })
    print('Result length:', len(result))
    
test()
