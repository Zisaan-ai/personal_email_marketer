with open('backend/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re

new_func = '''
# ============================================================
# MODULE-LEVEL: Scheduler job — start scheduled campaigns
# ============================================================
def _scheduler_start_scheduled_campaigns():
    """Every 1 min: check for campaigns with status 'scheduled' where scheduled_at <= now()"""
    db = database.SessionLocal()
    try:
        now = datetime.utcnow()
        scheduled_camps = db.query(database.Campaign).filter(
            database.Campaign.status == 'scheduled',
            database.Campaign.scheduled_at <= now
        ).all()
        for camp in scheduled_camps:
            print(f"[scheduler] Auto-starting scheduled campaign {camp.id}")
            camp.status = 'processing'
            db.commit()
            threading.Thread(
                target=process_isolated_campaign,
                args=(str(camp.id),),
                daemon=True
            ).start()
    except Exception as e:
        print(f"[scheduler] Start scheduled error: {e}")
    finally:
        db.close()
'''

if '_scheduler_start_scheduled_campaigns' not in text:
    text = text.replace('# Register scheduler jobs', new_func + '\n# Register scheduler jobs')

if 'start_scheduled_job' not in text:
    text = text.replace(
        "scheduler.add_job(_scheduler_resume_paused_campaigns, 'interval', minutes=2, id='campaign_resume_job')",
        "scheduler.add_job(_scheduler_resume_paused_campaigns, 'interval', minutes=2, id='campaign_resume_job')\nscheduler.add_job(_scheduler_start_scheduled_campaigns, 'interval', minutes=1, id='start_scheduled_job')"
    )

# Also update the startup routine
startup_old = '''        stuck = db.query(database.Campaign).filter(
            database.Campaign.status == 'processing'
        ).all()'''

startup_new = '''        now = datetime.utcnow()
        stuck = db.query(database.Campaign).filter(
            database.Campaign.status.in_(['processing', 'scheduled'])
        ).all()
        # Only resume scheduled if their time has come
        stuck = [c for c in stuck if c.status == 'processing' or (c.status == 'scheduled' and c.scheduled_at and c.scheduled_at <= now)]'''

text = text.replace(startup_old, startup_new)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done!')
