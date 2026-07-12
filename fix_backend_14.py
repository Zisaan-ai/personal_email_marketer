import sys
import re

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_1 = """        target_campaign.scheduled_at = campaign.scheduled_at
        target_campaign.timezone = campaign.timezone
        target_campaign.delay_min = campaign.delay_min
        target_campaign.delay_max = campaign.delay_max
        db.commit()"""

new_1 = """        target_campaign.scheduled_at = campaign.scheduled_at
        target_campaign.timezone = campaign.timezone
        target_campaign.delay_min = campaign.delay_min
        target_campaign.delay_max = campaign.delay_max
        target_campaign.sending_days = campaign.sending_days
        target_campaign.start_hour = campaign.start_hour
        target_campaign.end_hour = campaign.end_hour
        db.commit()"""
content = content.replace(old_1, new_1)

old_2 = """            scheduled_at=campaign.scheduled_at,
            timezone=campaign.timezone,
            delay_min=campaign.delay_min,
            delay_max=campaign.delay_max
        )"""

new_2 = """            scheduled_at=campaign.scheduled_at,
            timezone=campaign.timezone,
            delay_min=campaign.delay_min,
            delay_max=campaign.delay_max,
            sending_days=campaign.sending_days,
            start_hour=campaign.start_hour,
            end_hour=campaign.end_hour
        )"""
content = content.replace(old_2, new_2)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed sending schedule reset bug in send_campaign")
