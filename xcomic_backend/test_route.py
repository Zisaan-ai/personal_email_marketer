from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import database
import json
from datetime import datetime

router = APIRouter()

@router.get('/api/test_followup')
def test_followup(db: Session = Depends(database.get_db)):
    try:
        account = db.query(database.SendingAccount).filter_by(is_active=True).first()
        if not account:
            return {'error': 'No active sending account'}
            
        campaign = database.Campaign(
            subject='Test Followup',
            body='Step 1 Body',
            type='cold_mail',
            user_id=account.user_id,
            steps_json=json.dumps([
                {'step': 1, 'subject': 'Step 1', 'body': 'Step 1', 'wait': 2, 'is_ab': False},
                {'step': 2, 'subject': 'Step 2', 'body': 'Step 2', 'wait': 3, 'is_ab': False}
            ]),
            status='processing',
            track_opens=False,
            track_clicks=False
        )
        db.add(campaign)
        db.commit()
        
        lead = database.CampaignLead(
            campaign_id=campaign.id,
            email='test_test_followup@example.com',
            name='Test Followup',
            status='pending',
            current_step=0
        )
        db.add(lead)
        db.commit()
        
        import main
        main._run_campaign(db, campaign.id)
        
        db.refresh(lead)
        step1_status = lead.status
        step1_next_send_at = str(lead.next_send_at)
        
        lead.next_send_at = datetime.utcnow()
        lead.status = 'sent'
        db.commit()
        
        main._run_campaign(db, campaign.id)
        
        db.refresh(lead)
        step2_status = lead.status
        step2_next_send_at = str(lead.next_send_at)
        
        db.delete(lead)
        db.delete(campaign)
        db.commit()
        
        return {
            'step1': {'status': step1_status, 'next_send_at': step1_next_send_at},
            'step2': {'status': step2_status, 'next_send_at': step2_next_send_at},
            'success': step1_status == 'sent' and step2_status == 'completed'
        }
    except Exception as e:
        return {'error': str(e)}
