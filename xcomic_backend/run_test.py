
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import SessionLocal, Campaign, SendingAccount
from main import get_available_account, _last_domain_used
import main

db = SessionLocal()
campaign = db.query(Campaign).filter(Campaign.id == "2bf58216-2ab7-4bd3-bb2b-e4e7ba0d92a1").first()

output = []
output.append(f"Campaign user: {campaign.user_id}")
output.append(f"Campaign status: {campaign.status}")
output.append(f"Campaign sent_today_campaign: {campaign.sent_today_campaign}")
output.append(f"Campaign current_daily_limit: {campaign.current_daily_limit}")

all_accounts = db.query(SendingAccount).filter(
    SendingAccount.is_active == True,
    SendingAccount.auto_paused == False,
    SendingAccount.user_id == campaign.user_id
).all()

output.append(f"Active accounts count: {len(all_accounts)}")

main._last_domain_used = [""]
acc = get_available_account(db, campaign) if 'campaign' in get_available_account.__code__.co_varnames else get_available_account(db)
if acc:
    output.append(f"Available account: {acc.email}")
else:
    output.append("No available account")

db.close()

with open(os.path.join(os.path.dirname(__file__), "test_output.txt"), "w") as f:
    f.write(chr(10).join(output))
