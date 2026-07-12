import sys
import re

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add import threading if not exists
if 'import threading' not in content:
    content = content.replace('import os', 'import os\nimport threading')

# Replace background tasks with threading.Thread
old_1 = "background_tasks.add_task(process_isolated_campaign, str(new_campaign.id))"
new_1 = "threading.Thread(target=process_isolated_campaign, args=(str(new_campaign.id),)).start()"
content = content.replace(old_1, new_1)

old_2 = "background_tasks.add_task(process_isolated_campaign, str(campaign.id))"
new_2 = "threading.Thread(target=process_isolated_campaign, args=(str(campaign.id),)).start()"
content = content.replace(old_2, new_2)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed background tasks to use threading")
