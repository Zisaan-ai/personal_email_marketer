import os
import sys

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add _auto_resume_stuck_campaigns and _scheduler_start_scheduled_campaigns
new_jobs = """
def _auto_resume_stuck_campaigns():
    db = database.SessionLocal()
    try:
        campaigns = db.query(database.Campaign).filter(database.Campaign.status == "processing").all()
        for c in campaigns:
            print(f"Auto-resuming stuck campaign {c.id}")
            import threading
            threading.Thread(target=process_isolated_campaign, args=(str(c.id),)).start()
    finally:
        db.close()

def _scheduler_start_scheduled_campaigns():
    db = database.SessionLocal()
    try:
        campaigns = db.query(database.Campaign).filter(database.Campaign.status.in_(["scheduled", "processing"])).all()
        for c in campaigns:
            if is_campaign_within_schedule(c):
                if c.status == "scheduled":
                    c.status = "processing"
                    db.commit()
                print(f"Scheduler starting campaign {c.id}")
                import threading
                threading.Thread(target=process_isolated_campaign, args=(str(c.id),)).start()
    finally:
        db.close()

def is_campaign_within_schedule(campaign):
    import pytz
    from datetime import datetime
    import json
    
    # If no schedule is set, it's always valid
    if not campaign.sending_days and campaign.start_hour is None and campaign.end_hour is None:
        return True
        
    try:
        tz = pytz.timezone(campaign.timezone or "Asia/Dhaka")
        now_local = datetime.now(pytz.utc).astimezone(tz)
        
        # Check day
        if campaign.sending_days:
            try:
                allowed_days = json.loads(campaign.sending_days)
            except:
                allowed_days = []
            
            day_map = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
            current_day = day_map[now_local.weekday()]
            if current_day not in allowed_days:
                return False
                
        # Check time
        if campaign.start_hour is not None and campaign.end_hour is not None:
            now_hour = now_local.hour
            start = campaign.start_hour
            end = campaign.end_hour
            if start == 0 and end == 24:
                return True
            if start <= end:
                if not (start <= now_hour < end):
                    return False
            else: # cross midnight
                if not (now_hour >= start or now_hour < end):
                    return False
        return True
    except Exception as e:
        print(f"Error checking schedule for {campaign.id}: {e}")
        return True # Fallback

def check_bounces():
"""

if "_auto_resume_stuck_campaigns" not in content:
    content = content.replace("def check_bounces():", new_jobs)


# 2. Add scheduler jobs
scheduler_jobs = """
scheduler.add_job(domain_checker.run_domain_health_check, 'cron', hour=6, minute=0, id='domain_check_job')
scheduler.add_job(_auto_resume_stuck_campaigns, 'interval', minutes=30, id='auto_resume_job')
scheduler.add_job(_scheduler_start_scheduled_campaigns, 'interval', minutes=5, id='scheduled_campaigns_job')
"""
if "_auto_resume_stuck_campaigns" not in content and "auto_resume_job" not in content:
    content = content.replace("scheduler.add_job(domain_checker.run_domain_health_check, 'cron', hour=6, minute=0, id='domain_check_job')", scheduler_jobs)


# 3. Add schedule check in _run_campaign
run_campaign_check = """
    # BUG FIX: Build unsubscribe set for fast lookup
    unsub_emails = set(u.email.lower() for u in db.query(database.UnsubscribeList).all())
    
    # Check if campaign is within its schedule window
    if not is_campaign_within_schedule(campaign):
        print(f"Campaign {campaign.id} is outside its scheduled window. Pausing/Scheduling.")
        campaign.status = "scheduled"
        db.commit()
        return
"""

if "is_campaign_within_schedule(campaign)" not in content:
    content = content.replace("# BUG FIX: Build unsubscribe set for fast lookup\n    unsub_emails = set(u.email.lower() for u in db.query(database.UnsubscribeList).all())", run_campaign_check)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied scheduling logic to main.py")
