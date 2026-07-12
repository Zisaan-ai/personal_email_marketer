import os

with open('backend/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.startswith("def is_campaign_within_schedule(campaign):"):
        skip = True
    elif skip and line.startswith("from bounce_processor import check_bounces"):
        skip = False
        new_lines.append(line)
        continue
        
    if not skip:
        new_lines.append(line)

content = "".join(new_lines)

# Now inject the definitions right before scheduler.add_job
functions = """
def is_campaign_within_schedule(campaign):
    import pytz
    from datetime import datetime
    import json
    
    if not campaign.sending_days and campaign.start_hour is None and campaign.end_hour is None:
        return True
        
    try:
        tz = pytz.timezone(campaign.timezone or "Asia/Dhaka")
        now_local = datetime.now(pytz.utc).astimezone(tz)
        
        if campaign.sending_days:
            try:
                allowed_days = json.loads(campaign.sending_days)
            except:
                allowed_days = []
            
            day_map = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
            current_day = day_map[now_local.weekday()]
            if current_day not in allowed_days:
                return False
                
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
        return True

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

"""

content = content.replace("scheduler.add_job(domain_checker.run_domain_health_check", functions + "\nscheduler.add_job(domain_checker.run_domain_health_check")

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed main.py")
