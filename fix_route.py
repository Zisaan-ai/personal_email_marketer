import os

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
content = content.replace('@app.post("/api/campaigns/{campaign_id}/schedule")', '@app.post("/api/campaigns/{campaign_id}/save-schedule")')

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed route name!')
