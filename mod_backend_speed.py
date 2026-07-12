with open('backend/main.py', encoding='utf-8') as f:
    text = f.read()

orig_loop = '''    if campaign.leads:
        for lead_in in campaign.leads:
            db_lead = database.CampaignLead(campaign_id=str(new_campaign.id), name=lead_in.name, email=lead_in.email, company=lead_in.company)
            db.add(db_lead)
            db.commit()'''

new_loop = '''    if campaign.leads:
        new_leads = []
        for lead_in in campaign.leads:
            new_leads.append(database.CampaignLead(campaign_id=str(new_campaign.id), name=lead_in.name, email=lead_in.email, company=lead_in.company))
        if new_leads:
            db.add_all(new_leads)
            db.commit()'''

text = text.replace(orig_loop, new_loop)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated backend loop to bulk commit.")
