import sys

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 5. send_to_lead
old_send = """        # Deliverability: Validate email format & MX record before sending
        validation = email_service.validate_email_address(lead.email)
        if not validation['valid']:
            lead.status = "invalid"
            db.commit()
            print(f"Skipping invalid email {lead.email}: {validation['reason']}")
            return True
            
        acc = get_available_account()
        if not acc:
            print("All accounts reached daily limit or outside sending window.")
            return False  # signal to stop"""

new_send = """        # Deliverability: Validate email format & MX record before sending
        validation = email_service.validate_email_address(lead.email)
        if not validation['valid']:
            lead.status = "invalid"
            db.commit()
            print(f"Skipping invalid email {lead.email}: {validation['reason']}")
            return True, None
            
        acc, reason = get_available_account()
        if not acc:
            print("All accounts reached daily limit or outside sending window.")
            return False, reason  # signal to stop"""

if old_send in content:
    content = content.replace(old_send, new_send)

# 5b. Fix returns in send_to_lead
content = content.replace(
    "            return False  # Signal to abort loop",
    "            return False, \"Campaign was paused by user\"  # Signal to abort loop"
)
content = content.replace(
    "            return True\n\n        # REPLY AUTO-STOP:",
    "            return True, None\n\n        # REPLY AUTO-STOP:"
)
content = content.replace(
    "            print(f\"Skipping replied lead: {lead.email}\")\n            return True",
    "            print(f\"Skipping replied lead: {lead.email}\")\n            return True, None"
)
content = content.replace(
    "        db.commit()\n        return True\n\n    if campaign.is_ab_test:",
    "        db.commit()\n        return True, None\n\n    if campaign.is_ab_test:"
)

# 6. Modify the _run_campaign loops
old_loop_a = """        for lead in leads_a:
            result = send_to_lead(lead, campaign.subject, campaign.body, 'A')
            if result is False: break
            time.sleep(random.randint(delay_min, delay_max))"""

new_loop_a = """        for lead in leads_a:
            result, stop_reason = send_to_lead(lead, campaign.subject, campaign.body, 'A')
            if result is False:
                campaign.status = "paused"
                campaign.paused_reason = stop_reason
                db.commit()
                break
            time.sleep(random.randint(delay_min, delay_max))"""
            
if old_loop_a in content: content = content.replace(old_loop_a, new_loop_a)

old_loop_b = """        for lead in leads_b:
            subj_b = campaign.subject_b or campaign.subject
            body_b = campaign.body_b or campaign.body
            result = send_to_lead(lead, subj_b, body_b, 'B')
            if result is False: break
            time.sleep(random.randint(delay_min, delay_max))"""

new_loop_b = """        for lead in leads_b:
            subj_b = campaign.subject_b or campaign.subject
            body_b = campaign.body_b or campaign.body
            result, stop_reason = send_to_lead(lead, subj_b, body_b, 'B')
            if result is False:
                campaign.status = "paused"
                campaign.paused_reason = stop_reason
                db.commit()
                break
            time.sleep(random.randint(delay_min, delay_max))"""

if old_loop_b in content: content = content.replace(old_loop_b, new_loop_b)

old_loop_norm = """        for lead in leads:
            result = send_to_lead(lead, campaign.subject, campaign.body)
            if result is False: break
            time.sleep(random.randint(delay_min, delay_max))"""

new_loop_norm = """        for lead in leads:
            result, stop_reason = send_to_lead(lead, campaign.subject, campaign.body)
            if result is False:
                campaign.status = "paused"
                campaign.paused_reason = stop_reason
                db.commit()
                break
            time.sleep(random.randint(delay_min, delay_max))"""

if old_loop_norm in content: content = content.replace(old_loop_norm, new_loop_norm)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Pass 3 done")
