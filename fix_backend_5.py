import sys

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add fields to CampaignCreate
if "sending_days: Optional[str] = None" not in content:
    content = content.replace(
        "    timezone: Optional[str] = None",
        "    timezone: Optional[str] = None\n    sending_days: Optional[str] = None\n    start_hour: Optional[int] = None\n    end_hour: Optional[int] = None"
    )

# 2. Add fields to API endpoints (POST /api/campaigns)
if "new_campaign.sending_days = campaign.sending_days" not in content:
    old_create = """    new_campaign.is_draft = campaign.is_draft
    
    # Process leads if provided"""
    new_create = """    new_campaign.is_draft = campaign.is_draft
    new_campaign.sending_days = campaign.sending_days
    new_campaign.start_hour = campaign.start_hour
    new_campaign.end_hour = campaign.end_hour
    
    # Process leads if provided"""
    content = content.replace(old_create, new_create)

# 3. Add fields to API endpoints (PUT /api/campaigns/{campaign_id})
if "existing_campaign.sending_days = campaign.sending_days" not in content:
    old_update = """    existing_campaign.is_draft = campaign.is_draft
    
    # If leads provided, update them (Replace existing pending leads for simplicity)"""
    new_update = """    existing_campaign.is_draft = campaign.is_draft
    existing_campaign.sending_days = campaign.sending_days
    existing_campaign.start_hour = campaign.start_hour
    existing_campaign.end_hour = campaign.end_hour
    
    # If leads provided, update them (Replace existing pending leads for simplicity)"""
    content = content.replace(old_update, new_update)

# 4. Add fields to Newsletter endpoint (POST /api/newsletter/draft)
if "start_hour: Optional[int] = None" not in content:
    content = content.replace(
        "    timezone: Optional[str] = None\n    is_draft: Optional[bool] = False",
        "    timezone: Optional[str] = None\n    sending_days: Optional[str] = None\n    start_hour: Optional[int] = None\n    end_hour: Optional[int] = None\n    is_draft: Optional[bool] = False"
    )

if "db_camp.sending_days = draft.sending_days" not in content:
    content = content.replace(
        "    db_camp.is_draft = draft.is_draft\n    db_camp.timezone = draft.timezone\n    db.commit()",
        "    db_camp.is_draft = draft.is_draft\n    db_camp.timezone = draft.timezone\n    db_camp.sending_days = draft.sending_days\n    db_camp.start_hour = draft.start_hour\n    db_camp.end_hour = draft.end_hour\n    db.commit()"
    )

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Pass 5 (Campaign schemas) done")
