import os

with open('backend/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_code = """    # Only mark completed if not paused
    c = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
    if c and c.status != "paused":
        c.status = "completed"
        c.sent_count_a = (c.sent_count_a or 0) + success_count_a
        c.sent_count_b = (c.sent_count_b or 0) + success_count_b
        c.sent_count = (c.sent_count or 0) + success_count_a + success_count_b
        db.commit()
        trigger_webhook(c.user_id or "", "campaign_completed", {"campaign_id": str(c.id), "status": "completed"})"""

new_code = """    # Final check of lead status to update campaign status
    c = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
    if c and c.status != "paused":
        all_leads = list(db.query(database.CampaignLead).filter(database.CampaignLead.campaign_id == campaign_id).all())
        pending_count = sum(1 for l in all_leads if l.status == "pending")
        
        if pending_count == 0:
            c.status = "completed"
        else:
            # We stopped early (due to limits or pause or no active accounts)
            # DO NOT mark as completed if there are still pending leads!
            c.status = "processing"
            
        c.sent_count_a = (c.sent_count_a or 0) + success_count_a
        c.sent_count_b = (c.sent_count_b or 0) + success_count_b
        c.sent_count = (c.sent_count or 0) + success_count_a + success_count_b
        db.commit()
        
        if pending_count == 0:
            trigger_webhook(c.user_id or "", "campaign_completed", {"campaign_id": str(c.id), "status": "completed"})"""

if old_code in text:
    text = text.replace(old_code, new_code)
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed!")
else:
    print("Not found!")
