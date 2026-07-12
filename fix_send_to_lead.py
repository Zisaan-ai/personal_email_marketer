import sys
with open('backend/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

fix_code = '''
    # BUG FIX: Check leads BEFORE saving to DB to avoid orphan campaigns, unless it's a draft
    if not campaign.is_draft and (not campaign.leads or len(campaign.leads) == 0):
        raise HTTPException(status_code=400, detail="No leads provided for campaign")

    if campaign.is_draft:'''

text = text.replace('    if campaign.is_draft:', fix_code, 1)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done!')
