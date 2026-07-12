import sys

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. DB Migrations
if "ALTER TABLE campaigns ADD COLUMN paused_reason VARCHAR" not in content:
    old_mig = """        try:
            from sqlalchemy import text
            migrations = [
                "ALTER TABLE campaigns ADD COLUMN sending_days TEXT",
                "ALTER TABLE campaigns ADD COLUMN start_hour INTEGER",
                "ALTER TABLE campaigns ADD COLUMN end_hour INTEGER",
            ]"""
    new_mig = """        try:
            from sqlalchemy import text
            migrations = [
                "ALTER TABLE sending_accounts ADD COLUMN smart_limit_enabled BOOLEAN DEFAULT 0",
                "ALTER TABLE campaigns ADD COLUMN paused_reason VARCHAR",
                "ALTER TABLE campaigns ADD COLUMN sending_days TEXT",
                "ALTER TABLE campaigns ADD COLUMN start_hour INTEGER",
                "ALTER TABLE campaigns ADD COLUMN end_hour INTEGER",
            ]"""
    content = content.replace(old_mig, new_mig)

# 2. CampaignResponse
if "paused_reason: Optional[str] = None" not in content:
    content = content.replace(
        "status: str\n    is_ab_test: Optional[bool] = False",
        "status: str\n    paused_reason: Optional[str] = None\n    is_ab_test: Optional[bool] = False"
    )

# 3. get_campaigns
if '"paused_reason": c.paused_reason,' not in content:
    content = content.replace(
        '"status": c.status or "draft",\n        "is_ab_test": c.is_ab_test or False,',
        '"status": c.status or "draft",\n        "paused_reason": c.paused_reason,\n        "is_ab_test": c.is_ab_test or False,'
    )

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Pass 1 done")
