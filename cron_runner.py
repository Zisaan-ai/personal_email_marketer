import os
import sys
import datetime

# Ensure correct working directory so database and config files load correctly
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

print(f"[{datetime.datetime.now()}] --- Starting Cron Runner ---")

try:
    import database
    from bounce_processor import check_bounces
    import warmup_service
    import health_monitor
    import domain_checker
    from main import _auto_resume_stuck_campaigns, _scheduler_start_scheduled_campaigns
except Exception as e:
    print(f"Import Error: {e}")
    sys.exit(1)

# 1. Start scheduled campaigns
try:
    print("1. Running scheduled campaigns check...")
    _scheduler_start_scheduled_campaigns()
except Exception as e:
    print(f"Error checking scheduled campaigns: {e}")

# 2. Check bounces and replies
try:
    print("2. Running bounce & reply checks...")
    check_bounces()
except Exception as e:
    print(f"Error checking bounces: {e}")

# 3. Warmup cycle
try:
    print("3. Running email warmup cycle...")
    warmup_service.run_warmup_cycle()
except Exception as e:
    print(f"Error running warmup cycle: {e}")

# 4. Auto-resume stuck campaigns
try:
    print("4. Auto resuming stuck campaigns...")
    _auto_resume_stuck_campaigns()
except Exception as e:
    print(f"Error auto-resuming campaigns: {e}")

print(f"[{datetime.datetime.now()}] --- Cron Runner Finished Successfully ---")
