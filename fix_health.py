import sys

with open('xcomic_backend/health_monitor.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We will replace calculate_health_score and check_auto_pause
new_calc = '''def calculate_health_score(account) -> int:
    \"\"\"
    Calculate health score (0-100) based on account metrics.
    Starts at 100 and reduces based on bounces.
    \"\"\"
    total_sent = account.total_sent or 0
    total_bounced = account.total_bounced or 0
    total_opened = account.total_opened or 0
    total_replied = account.total_replied or 0
    bounce_streak = account.bounce_streak or 0

    base_score = 100

    if total_sent > 0:
        bounce_rate = total_bounced / total_sent
        bounce_penalty = bounce_rate * 100  # e.g., 20% bounce rate = -20 points

        streak_penalty = min(bounce_streak * 5, 30)

        open_rate = total_opened / total_sent
        open_bonus = min(open_rate * 20, 10)

        reply_rate = total_replied / total_sent
        reply_bonus = min(reply_rate * 50, 15)

        score = base_score - bounce_penalty - streak_penalty + open_bonus + reply_bonus
    else:
        score = base_score

    return max(0, min(100, int(round(score))))'''

old_calc_pattern = re.compile(r'def calculate_health_score\(account\) -> int:.*?(?=\n\n\n# ============================================================|\n\n# ============================================================)', re.DOTALL)
content = old_calc_pattern.sub(new_calc, content)

new_check = '''def check_auto_pause(db, account) -> bool:
    \"\"\"
    Check if an account should be auto-paused.
    \"\"\"
    if account.auto_paused:
        return False  # Already paused
        
    reason = None
    
    if (account.health_score or 100) < 50:
        reason = f"Health score critically low ({account.health_score}/100)"
    elif (account.bounce_streak or 0) >= 5:
        reason = f"5+ consecutive bounces (streak: {account.bounce_streak})"
        
    if reason:
        account.auto_paused = True
        account.auto_paused_reason = reason
        account.is_active = False
        db.commit()
        print(f"[Health Monitor] ⚠️ Auto-paused account {account.email}: {reason}")
        return True
        
    return False'''

old_check_pattern = re.compile(r'def check_auto_pause\(db, account\) -> bool:.*?(?=\n\n\ndef reactivate_account|\n\ndef reactivate_account)', re.DOTALL)
content = old_check_pattern.sub(new_check, content)

with open('xcomic_backend/health_monitor.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated health_monitor.py")
