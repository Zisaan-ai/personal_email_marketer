import os

with open('backend/health_monitor.py', 'r', encoding='utf-8') as f:
    text = f.read()

# BUG: suggest_daily_limit() returns warmup_daily_limit when warmup is enabled
# This makes the CAMPAIGN sending limit = warmup limit (e.g. 7)
# But warmup and campaign are INDEPENDENT modules!
# Campaign should use the user's daily_limit (e.g. 15), NOT warmup_daily_limit

old_code = """    # If warmup is enabled, use warmup limit
    if account.warmup_enabled:
        return account.warmup_daily_limit or 5"""

new_code = """    # NOTE: Warmup and Campaign are INDEPENDENT modules.
    # Warmup has its own limit (warmup_daily_limit) tracked by warmup_sent_today.
    # Campaign has its own limit (daily_limit) tracked by sent_today.
    # DO NOT reduce campaign limit based on warmup status."""

if old_code in text:
    text = text.replace(old_code, new_code)
    with open('backend/health_monitor.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed health_monitor.py!")
else:
    print("ERROR: Could not find the warmup block")
