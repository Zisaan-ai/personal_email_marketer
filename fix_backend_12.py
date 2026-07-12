import sys

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_leads = """    if campaign.leads:
        for lead_in in campaign.leads:
            db_lead = database.CampaignLead(campaign_id=str(new_campaign.id), name=lead_in.name, email=lead_in.email, company=lead_in.company)
            db.add(db_lead)
            db.commit()"""

new_leads = """    if campaign.leads:
        for lead_in in campaign.leads:
            db_lead = database.CampaignLead(campaign_id=str(new_campaign.id), name=lead_in.name, email=lead_in.email, company=lead_in.company)
            db.add(db_lead)
        db.commit()"""

if old_leads in content:
    content = content.replace(old_leads, new_leads)
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed bulk leads insertion performance")
else:
    print("Could not find leads block")
