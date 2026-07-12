with open('backend/main.py', encoding='utf-8') as f:
    text = f.read()

orig = '''    if campaign.leads:
        new_leads = []
        for lead_in in campaign.leads:
            new_leads.append(database.CampaignLead(campaign_id=str(new_campaign.id), name=lead_in.name, email=lead_in.email, company=lead_in.company))
        if new_leads:
            db.add_all(new_leads)
            db.commit()'''

new_val = '''    if campaign.leads:
        mappings = []
        campaign_id_str = str(new_campaign.id)
        for lead_in in campaign.leads:
            mappings.append({
                "campaign_id": campaign_id_str,
                "name": lead_in.name,
                "email": lead_in.email,
                "company": lead_in.company
            })
        if mappings:
            db.bulk_insert_mappings(database.CampaignLead, mappings)
            db.commit()'''

text = text.replace(orig, new_val)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated backend to use bulk_insert_mappings.")
