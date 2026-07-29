import time
import random
import os
import json
import threading
from datetime import datetime
import pytz

active_bulk_campaign_threads = set()
bulk_campaign_thread_lock = threading.Lock()

def process_isolated_bulk_campaign(campaign_id: str):
    with bulk_campaign_thread_lock:
        if campaign_id in active_bulk_campaign_threads:
            print(f"Bulk Campaign {campaign_id} is already running in a thread. Skipping duplicate execution.")
            return
        active_bulk_campaign_threads.add(campaign_id)
        
    import database
    db = database.SessionLocal()
    try:
        _run_bulk_campaign(db, campaign_id)
    finally:
        db.close()
        with bulk_campaign_thread_lock:
            active_bulk_campaign_threads.discard(campaign_id)

def _run_bulk_campaign(db, campaign_id):
    import database
    import email_service
    from sqlalchemy import or_, and_
    
    campaign_id = str(campaign_id)
    campaign = db.query(database.BulkCampaign).filter(database.BulkCampaign.id == campaign_id).first()
    if not campaign:
        return

    now = datetime.utcnow()
    # If scheduled in future, wait
    if campaign.scheduled_at and campaign.scheduled_at > now:
        db.execute("UPDATE bulk_campaigns SET status='scheduled' WHERE id=:id", {"id": campaign_id})
        db.commit()
        return

    # Check active accounts
    if not campaign.sending_account_ids:
        campaign.status = "failed"
        db.commit()
        return
        
    try:
        account_ids = json.loads(campaign.sending_account_ids)
    except:
        account_ids = []
        
    if not account_ids:
        campaign.status = "failed"
        db.commit()
        return

    accounts = db.query(database.SendingAccount).filter(database.SendingAccount.id.in_(account_ids), database.SendingAccount.is_active == True).all()
    if not accounts:
        campaign.status = "failed"
        db.commit()
        return

    leads = db.query(database.BulkCampaignLead).filter(
        database.BulkCampaignLead.bulk_campaign_id == campaign_id,
        database.BulkCampaignLead.status == "pending"
    ).all()

    if not leads:
        campaign.status = "completed"
        db.commit()
        return

    campaign.status = "running"
    db.commit()

    import health_monitor as hm
    
    account_idx = 0
    for lead in leads:
        # Check if campaign was paused or deleted
        camp_check = db.query(database.BulkCampaign).filter(database.BulkCampaign.id == campaign_id).first()
        if not camp_check or camp_check.status != "running":
            return
            
        # Select account round-robin
        acc = accounts[account_idx % len(accounts)]
        account_idx += 1
        
        # Smart limit check
        if getattr(acc, "smart_limit_enabled", False):
            smart_limit = hm.suggest_daily_limit(acc)
            effective_daily = min(acc.daily_limit or 500, smart_limit)
        else:
            effective_daily = acc.daily_limit or 500
            
        if acc.sent_today >= effective_daily:
            # Skip if this account is exhausted
            continue

        # Format HTML content
        body = campaign.html_content or ""
        # Basic variable replacement (can add more if needed)
        body = body.replace("{{email}}", lead.email)

        # Send email
        subject = campaign.name
        
        try:
            sent = email_service.send_single_email(
                subject=subject,
                body_html=body,
                recipient=lead.email,
                account=acc
            )
            
            if sent:
                lead.status = "sent"
                lead.sent_at = datetime.utcnow()
                lead.sending_account_id = str(acc.id)
                acc.sent_today += 1
            else:
                lead.status = "failed"
                
            db.commit()
        except Exception as e:
            print(f"Error sending bulk email to {lead.email}: {e}")
            lead.status = "failed"
            db.commit()
            
        time.sleep(1) # Small delay between sends

    # Re-evaluate campaign status
    pending_leads = db.query(database.BulkCampaignLead).filter(
        database.BulkCampaignLead.bulk_campaign_id == campaign_id,
        database.BulkCampaignLead.status == "pending"
    ).count()
    
    if pending_leads == 0:
        campaign.status = "completed"
        db.commit()
