import os
import sys
import json
from datetime import datetime
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import database
from database import SessionLocal
import main

db = SessionLocal()

try:
    print("--- Starting Smart Follow-up Test ---")
    account = db.query(database.SendingAccount).filter_by(is_active=True).first()
    if not account:
        print("No active sending account found. Cannot test.")
        sys.exit(1)
        
    user_id = account.user_id
    
    steps = [
        {"step": 1, "subject": "Test Step 1", "body": "Hello, this is step 1", "wait": 2, "is_ab": False},
        {"step": 2, "subject": "Test Step 2", "body": "Hello, this is step 2", "wait": 3, "is_ab": False}
    ]
    
    campaign = database.Campaign(
        subject="Test Step 1",
        body="Hello, this is step 1",
        type="cold_mail",
        user_id=user_id,
        steps_json=json.dumps(steps),
        status="processing",
        track_opens=False,
        track_clicks=False
    )
    db.add(campaign)
    db.commit()
    print(f"Created Campaign ID: {campaign.id}")
    
    lead = database.CampaignLead(
        campaign_id=campaign.id,
        email="test_followup@example.com",
        name="Test Followup",
        status="pending",
        current_step=0
    )
    db.add(lead)
    db.commit()
    print(f"Created Lead: {lead.email}")
    
    print("Running campaign for Step 1...")
    main._run_campaign(db, campaign.id)
    
    db.refresh(lead)
    print(f"After Step 1 -> Status: {lead.status}, Current Step: {lead.current_step}, Next Send At: {lead.next_send_at}")
    
    if lead.status == "sent" and lead.current_step == 1 and lead.next_send_at is not None:
        print("SUCCESS: Step 1 executed successfully and scheduled next step.")
    else:
        print("FAIL: Step 1 did not execute or schedule correctly.")
        
    print("Fast-forwarding time to simulate 2 days passing...")
    lead.next_send_at = datetime.utcnow()
    lead.status = "sent"
    db.commit()
    
    print("Running campaign for Step 2...")
    main._run_campaign(db, campaign.id)
    
    db.refresh(lead)
    print(f"After Step 2 -> Status: {lead.status}, Current Step: {lead.current_step}, Next Send At: {lead.next_send_at}")
    
    if lead.status == "completed" and lead.current_step == 2 and lead.next_send_at is None:
        print("SUCCESS: Step 2 executed successfully and marked as completed.")
    else:
        print("FAIL: Step 2 did not execute or mark completed correctly.")
        
    db.delete(lead)
    db.delete(campaign)
    db.commit()
    print("Test data cleaned up.")
    print("--- Test Complete ---")
    
except Exception as e:
    print(f"Error during test: {e}")
finally:
    db.close()
