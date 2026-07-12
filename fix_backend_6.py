import sys

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 5. Add campaign window checking in _run_campaign
old_run_logic = """    def get_available_account():
        # SMART SELECTION: Health-based ordering, skip auto-paused, check sending window
        all_accounts = db.query(database.SendingAccount).filter("""

new_run_logic = """    def is_campaign_within_window(camp):
        if not camp.sending_days and (camp.start_hour is None or camp.start_hour == 0) and (camp.end_hour is None or camp.end_hour == 24):
            return True, None
            
        import pytz, json
        from datetime import datetime
        tz_str = camp.timezone or "UTC"
        try:
            tz = pytz.timezone(tz_str)
        except:
            tz = pytz.UTC
            
        now = datetime.now(tz)
        
        # Check day
        if camp.sending_days:
            try:
                days = json.parse(camp.sending_days)
            except:
                try:
                    import json
                    days = json.loads(camp.sending_days)
                except:
                    days = []
            if days:
                day_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
                current_day = day_map[now.weekday()]
                if current_day not in days:
                    return False, f"Today ({current_day}) is not an allowed sending day"
                    
        # Check time
        start = camp.start_hour if camp.start_hour is not None else 0
        end = camp.end_hour if camp.end_hour is not None else 24
        
        if start == 0 and end == 24:
            pass
        elif not (start <= now.hour < end):
            return False, f"Current time ({now.strftime('%H:%M')} {tz_str}) is outside allowed window ({start}:00 - {end}:00)"
            
        return True, None

    def get_available_account():
        # SMART SELECTION: Health-based ordering, skip auto-paused, check sending window
        all_accounts = db.query(database.SendingAccount).filter("""

if "def is_campaign_within_window(camp):" not in content:
    content = content.replace(old_run_logic, new_run_logic)

# Insert the check into the send_to_lead function
old_send = """    def send_to_lead(lead, subject, body, variant_label=None):
        # Prevent duplicate sends
        if lead.status != 'pending':"""

new_send = """    def send_to_lead(lead, subject, body, variant_label=None):
        # Check campaign window first
        is_valid, reason = is_campaign_within_window(campaign)
        if not is_valid:
            return "WAIT", reason
            
        # Prevent duplicate sends
        if lead.status != 'pending':"""

if "is_campaign_within_window(campaign)" not in content:
    content = content.replace(old_send, new_send)

# Update loops to handle "WAIT"
old_loop_a = """        for lead in leads_a:
            result, stop_reason = send_to_lead(lead, campaign.subject, campaign.body, 'A')
            if result is False:"""

new_loop_a = """        for lead in leads_a:
            result, stop_reason = send_to_lead(lead, campaign.subject, campaign.body, 'A')
            if result == "WAIT":
                print(f"Campaign {campaign.id} sleeping for 30 mins: {stop_reason}")
                time.sleep(30 * 60)
                continue
            if result is False:"""
if old_loop_a in content: content = content.replace(old_loop_a, new_loop_a)

old_loop_b = """        for lead in leads_b:
            subj_b = campaign.subject_b or campaign.subject
            body_b = campaign.body_b or campaign.body
            result, stop_reason = send_to_lead(lead, subj_b, body_b, 'B')
            if result is False:"""

new_loop_b = """        for lead in leads_b:
            subj_b = campaign.subject_b or campaign.subject
            body_b = campaign.body_b or campaign.body
            result, stop_reason = send_to_lead(lead, subj_b, body_b, 'B')
            if result == "WAIT":
                print(f"Campaign {campaign.id} sleeping for 30 mins: {stop_reason}")
                time.sleep(30 * 60)
                continue
            if result is False:"""
if old_loop_b in content: content = content.replace(old_loop_b, new_loop_b)

old_loop_norm = """        for lead in leads:
            result, stop_reason = send_to_lead(lead, campaign.subject, campaign.body)
            if result is False:"""

new_loop_norm = """        for lead in leads:
            result, stop_reason = send_to_lead(lead, campaign.subject, campaign.body)
            if result == "WAIT":
                print(f"Campaign {campaign.id} sleeping for 30 mins: {stop_reason}")
                time.sleep(30 * 60)
                continue
            if result is False:"""
if old_loop_norm in content: content = content.replace(old_loop_norm, new_loop_norm)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Pass 6 done")
