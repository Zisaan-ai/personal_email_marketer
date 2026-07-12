import sys

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_get = """        "opens_a": c.opens_a or 0,
        "opens_b": c.opens_b or 0,
        "created_at": str(c.created_at) if c.created_at else None,
        "scheduled_at": str(c.scheduled_at) if c.scheduled_at else None,
    } for c in campaigns]"""

new_get = """        "opens_a": c.opens_a or 0,
        "opens_b": c.opens_b or 0,
        "created_at": str(c.created_at) if c.created_at else None,
        "scheduled_at": str(c.scheduled_at) if c.scheduled_at else None,
        "sending_days": c.sending_days,
        "start_hour": c.start_hour,
        "end_hour": c.end_hour,
        "timezone": c.timezone,
    } for c in campaigns]"""

if old_get in content:
    content = content.replace(old_get, new_get)
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added schedule fields to get_campaigns")
else:
    print("Could not find old_get block")
