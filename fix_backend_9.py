import sys

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_send = """    def send_to_lead(lead, subject, body, variant_label=None):
        # Check campaign window first
        is_valid, reason = is_campaign_within_window(campaign)
        if not is_valid:
            return "WAIT", reason
            
        # Prevent duplicate sends"""

new_send = """    def send_to_lead(lead, subject, body, variant_label=None):
        # Check campaign window first
        is_valid, reason = is_campaign_within_window(campaign)
        if not is_valid:
            return "WAIT", reason
            
        # Prevent duplicate sends"""
if old_send in content: content = content.replace(old_send, new_send) # No change needed here

# Fix the acc loop inside send_to_lead
old_acc_check = """        acc, reason = get_available_account()
        if not acc:
            print("All accounts reached daily limit or outside sending window.")
            return False, reason  # signal to stop"""

new_acc_check = """        acc, reason = get_available_account()
        if not acc:
            print("All accounts reached daily limit or outside sending window.")
            return "WAIT", reason  # signal to sleep instead of failing"""
if old_acc_check in content: content = content.replace(old_acc_check, new_acc_check)


# Fix the loop A
old_loop_a = """        for lead in leads_a:
            result, stop_reason = send_to_lead(lead, campaign.subject, campaign.body, 'A')
            if result == "WAIT":
                print(f"Campaign {campaign.id} sleeping for 30 mins: {stop_reason}")
                time.sleep(30 * 60)
                continue
            if result is False:
                campaign.status = "paused"
                campaign.paused_reason = stop_reason
                db.commit()
                break
            time.sleep(random.randint(delay_min, delay_max))"""

new_loop_a = """        i = 0
        while i < len(leads_a):
            lead = leads_a[i]
            result, stop_reason = send_to_lead(lead, campaign.subject, campaign.body, 'A')
            if result == "WAIT":
                print(f"Campaign {campaign.id} sleeping for 30 mins: {stop_reason}")
                campaign.paused_reason = f"Sleeping: {stop_reason}"
                db.commit()
                time.sleep(30 * 60)
                db.refresh(campaign)
                if campaign.status == 'paused': break
                continue # Retry the same lead
            
            if campaign.paused_reason:
                campaign.paused_reason = None
                db.commit()
                
            if result is False:
                campaign.status = "paused"
                campaign.paused_reason = stop_reason
                db.commit()
                break
            time.sleep(random.randint(delay_min, delay_max))
            i += 1"""
if old_loop_a in content: content = content.replace(old_loop_a, new_loop_a)

# Fix loop B
old_loop_b = """        for lead in leads_b:
            subj_b = campaign.subject_b or campaign.subject
            body_b = campaign.body_b or campaign.body
            result, stop_reason = send_to_lead(lead, subj_b, body_b, 'B')
            if result == "WAIT":
                print(f"Campaign {campaign.id} sleeping for 30 mins: {stop_reason}")
                time.sleep(30 * 60)
                continue
            if result is False:
                campaign.status = "paused"
                campaign.paused_reason = stop_reason
                db.commit()
                break
            time.sleep(random.randint(delay_min, delay_max))"""

new_loop_b = """        i = 0
        while i < len(leads_b):
            lead = leads_b[i]
            subj_b = campaign.subject_b or campaign.subject
            body_b = campaign.body_b or campaign.body
            result, stop_reason = send_to_lead(lead, subj_b, body_b, 'B')
            if result == "WAIT":
                print(f"Campaign {campaign.id} sleeping for 30 mins: {stop_reason}")
                campaign.paused_reason = f"Sleeping: {stop_reason}"
                db.commit()
                time.sleep(30 * 60)
                db.refresh(campaign)
                if campaign.status == 'paused': break
                continue
                
            if campaign.paused_reason:
                campaign.paused_reason = None
                db.commit()
                
            if result is False:
                campaign.status = "paused"
                campaign.paused_reason = stop_reason
                db.commit()
                break
            time.sleep(random.randint(delay_min, delay_max))
            i += 1"""
if old_loop_b in content: content = content.replace(old_loop_b, new_loop_b)

# Fix norm loop
old_loop_norm = """        for lead in leads:
            result, stop_reason = send_to_lead(lead, campaign.subject, campaign.body)
            if result == "WAIT":
                print(f"Campaign {campaign.id} sleeping for 30 mins: {stop_reason}")
                time.sleep(30 * 60)
                continue
            if result is False:
                campaign.status = "paused"
                campaign.paused_reason = stop_reason
                db.commit()
                break
            time.sleep(random.randint(delay_min, delay_max))"""

new_loop_norm = """        i = 0
        while i < len(leads):
            lead = leads[i]
            result, stop_reason = send_to_lead(lead, campaign.subject, campaign.body)
            if result == "WAIT":
                print(f"Campaign {campaign.id} sleeping for 30 mins: {stop_reason}")
                campaign.paused_reason = f"Sleeping: {stop_reason}"
                db.commit()
                time.sleep(30 * 60)
                db.refresh(campaign)
                if campaign.status == 'paused': break
                continue
                
            if campaign.paused_reason:
                campaign.paused_reason = None
                db.commit()
                
            if result is False:
                campaign.status = "paused"
                campaign.paused_reason = stop_reason
                db.commit()
                break
            time.sleep(random.randint(delay_min, delay_max))
            i += 1"""
if old_loop_norm in content: content = content.replace(old_loop_norm, new_loop_norm)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Pass 9 backend done")
