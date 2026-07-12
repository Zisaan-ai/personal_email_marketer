import sys

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to schemas
if "smart_limit_enabled: bool = False" not in content:
    content = content.replace(
        "    warmup_increment_per_day: int = 2",
        "    warmup_increment_per_day: int = 2\n    smart_limit_enabled: bool = False"
    )
    
# Add to endpoint responses
if '"smart_limit_enabled": acc.smart_limit_enabled,' not in content:
    content = content.replace(
        '            "warmup_sent_today": acc.warmup_sent_today,',
        '            "warmup_sent_today": acc.warmup_sent_today,\n            "smart_limit_enabled": getattr(acc, "smart_limit_enabled", False),'
    )

# Add to create endpoint
if 'smart_limit_enabled=acc.smart_limit_enabled' not in content:
    content = content.replace(
        "            warmup_increment_per_day=acc.warmup_increment_per_day",
        "            warmup_increment_per_day=acc.warmup_increment_per_day,\n            smart_limit_enabled=acc.smart_limit_enabled"
    )

# Add to update endpoint
if 'existing_acc.smart_limit_enabled = acc.smart_limit_enabled' not in content:
    content = content.replace(
        "        existing_acc.warmup_increment_per_day = acc.warmup_increment_per_day",
        "        existing_acc.warmup_increment_per_day = acc.warmup_increment_per_day\n        if hasattr(acc, 'smart_limit_enabled'):\n            existing_acc.smart_limit_enabled = acc.smart_limit_enabled"
    )

# Fix get_available_account logic
old_logic = """            # Enforce warmup limits
            if acc_doc.warmup_enabled:
                effective_limit = acc_doc.warmup_daily_limit or 5
                if acc_doc.warmup_sent_today >= effective_limit:
                    last_reason = f"Warmup limit reached ({effective_limit}/day) for {acc_doc.email}"
                    continue
            # Use smart suggested limit instead of raw daily_limit
            smart_limit = health_monitor.suggest_daily_limit(acc_doc)
            effective_daily = min(acc_doc.daily_limit or 500, smart_limit)
            if acc_doc.sent_today >= effective_daily:
                last_reason = f"Daily limit reached ({effective_daily}/day) for {acc_doc.email}"
                continue"""

new_logic = """            # Use smart suggested limit if enabled
            effective_daily = acc_doc.daily_limit or 500
            if getattr(acc_doc, 'smart_limit_enabled', False):
                smart_limit = health_monitor.suggest_daily_limit(acc_doc)
                effective_daily = min(effective_daily, smart_limit)
                
            if acc_doc.sent_today >= effective_daily:
                last_reason = f"Daily limit reached ({effective_daily}/day) for {acc_doc.email}"
                continue"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)

# Fix send_to_lead logic
old_send = """                if acc.warmup_enabled:
                    acc.warmup_sent_today += 1
                    db.commit()"""

new_send = """                # Warmup sent today is for the warmup cycle, not campaigns"""

if old_send in content:
    content = content.replace(old_send, new_send)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Pass 4 done")
