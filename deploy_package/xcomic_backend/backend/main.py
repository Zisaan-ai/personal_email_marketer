import base64
import asyncio
from fastapi import FastAPI, Depends, HTTPException, status, Request, BackgroundTasks, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import os
import re
import database
from sqlalchemy.orm import Session
import email_service
import auth
import random
import string
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

# Setup APScheduler
import warmup_service
scheduler = BackgroundScheduler()
scheduler.add_job(warmup_service.run_warmup_cycle, 'interval', minutes=30, id='warmup_job')
scheduler.add_job(warmup_service.reset_daily_warmup_counts, 'cron', hour=0, minute=0, id='warmup_reset')
scheduler.start()


app = FastAPI(title="MailChimp Clone API")

# Allow CORS for local React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

from bounce_processor import check_bounces

@app.on_event("startup")
async def startup_event():
    db = database.SessionLocal()
    try:
        # Warmup is handled by APScheduler in main.py
        if not scheduler.get_job('check_bounces_job'):
            scheduler.add_job(check_bounces, 'interval', hours=1, id='check_bounces_job')

        # Resume processing campaigns
        processing_campaigns = db.query(database.Campaign).filter(database.Campaign.status == "processing").all()

        
        # We can't inject background_tasks into startup event, so we'll start them in a thread/asyncio loop
        def resume_task(cid):
            process_isolated_campaign(cid)
        
        for c in processing_campaigns:
            print(f"Resuming campaign {c.id}")
            asyncio.get_running_loop().run_in_executor(None, resume_task, str(c.id))

        # Load API keys from DB into env (survives server restarts)
        # Priority: HF Space secrets (already in os.environ) > DB saved keys
        admin = db.query(database.User).filter(database.User.is_admin == True).first()
        if admin:
            if not os.getenv("GROQ_API_KEY") and admin.groq_api_key:
                os.environ["GROQ_API_KEY"] = admin.groq_api_key
                print("[Startup] Loaded GROQ_API_KEY from DB")
            if not os.getenv("GEMINI_API_KEY") and admin.gemini_api_key:
                os.environ["GEMINI_API_KEY"] = admin.gemini_api_key
                print("[Startup] Loaded GEMINI_API_KEY from DB")
            if os.getenv("GROQ_API_KEY"):
                print("[Startup] GROQ_API_KEY is available")
            else:
                print("[Startup] WARNING: GROQ_API_KEY not found. Set it in Settings or HF Secrets.")
    except Exception as e:
        print(f"[Startup] Error in startup_event: {e}")
    finally:
        db.close()


@app.get("/api/ping")
def ping(db: Session = Depends(database.get_db)):
    return {"status": "ok", "msg": "Server is alive"}



# Debug endpoints removed for security - BUG-02 fix

# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str
    is_admin: bool = False

class UserCreate(BaseModel):
    email: str
    password: str

class VerifyEmail(BaseModel):
    email: str
    code: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    code: str
    new_password: str

class CampaignLeadBase(BaseModel):
    name: Optional[str] = ""
    email: str
    company: Optional[str] = ""

class CampaignCreate(BaseModel):
    subject: str
    body: str
    type: str = "newsletter"
    leads: Optional[List[CampaignLeadBase]] = None
    is_ab_test: Optional[bool] = False
    subject_b: Optional[str] = None
    body_b: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    timezone: Optional[str] = None
    delay_min: Optional[int] = 30
    delay_max: Optional[int] = 90
    is_draft: Optional[bool] = False
    campaign_id: Optional[str] = None

class CampaignResponse(BaseModel):
    id: str  # BUG-24 fix: MongoDB IDs are strings not ints
    subject: str
    body: str
    type: str
    sent_count: int
    opens: int
    clicks: int
    status: str
    is_ab_test: Optional[bool] = False
    created_at: Optional[datetime] = None
    sent_count_a: Optional[int] = 0
    sent_count_b: Optional[int] = 0
    opens_a: Optional[int] = 0
    opens_b: Optional[int] = 0

    class Config:
        from_attributes = True

# --- AI ENDPOINTS ---
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = None

class EmailGenerateRequest(BaseModel):
    prompt: str

class SubjectOptimizeRequest(BaseModel):
    subject: str

class IcebreakerRequest(BaseModel):
    leads_csv: str

class AutopilotRequest(BaseModel):
    prompt: str

@app.post("/api/ai/chat")
def ai_chat(req: ChatRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    import ai_core
    history_dict = [msg.dict() for msg in req.history] if req.history else []
    response = ai_core.chat_with_assistant(req.message, history_dict)
    return {"reply": response}

@app.post("/api/ai/generate")
def ai_generate_email(req: EmailGenerateRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    import ai_core
    result = ai_core.generate_email_content(req.prompt)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result  # returns {"html": "..."}

@app.post("/api/ai/optimize-subject")
def ai_optimize_subject(req: SubjectOptimizeRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    import ai_core
    result = ai_core.optimize_subject(req.subject)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result  # returns {"subject": "..."}

@app.post("/api/ai/generate-icebreakers")
def ai_generate_icebreakers(req: IcebreakerRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    import ai_core
    result = ai_core.generate_icebreakers(req.leads_csv)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result  # returns {"csv": "..."}

@app.post("/api/ai/autopilot")
def ai_autopilot(req: AutopilotRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    import ai_core
    result = ai_core.generate_autopilot_campaign(req.prompt)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result  # returns {"subject_a", "body_a", "subject_b", "body_b"}


# --- AUTH ENDPOINTS ---
@app.post("/api/auth/register")
def register(user: UserCreate, db: Session = Depends(database.get_db)):
    email_lower = user.email.strip().lower()
    db_user = db.query(database.User).filter(database.User.email.ilike(email_lower)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_count = db.query(database.User).count()
    is_admin = (user_count == 0) or (email_lower == "zmonemrahman@gmail.com")
    is_approved = is_admin
    
    verification_code = ''.join(random.choices(string.digits, k=6))
    
    # Try sending email first before saving to DB
    try:
        email_sent = email_service.send_verification_email(user.email, verification_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SMTP Error: {str(e)}")
        
    if not email_sent:
        raise HTTPException(status_code=500, detail="Failed to send verification email.")

    hashed_password = auth.get_password_hash(user.password)
    new_user = database.User(
        email=email_lower,
        hashed_password=hashed_password,
        is_admin=is_admin,
        is_approved=is_admin,  # Require admin approval for non-admins
        verification_code=verification_code,
        is_email_verified=False  # Must verify email
    )
    db.add(new_user)
    db.commit()
    
    if is_admin:
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(data={"sub": new_user.email}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer", "is_admin": True}
    
    return {"status": "needs_approval", "message": "Account created! Please wait for admin approval to log in."}

@app.post("/api/auth/forgot-password")
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(database.get_db)):
    user = db.query(database.User).filter(database.User.email == req.email).first()
    if not user:
        # Don't reveal if user exists or not
        return {"message": "If your email is registered, you will receive a reset code."}
        
    verification_code = ''.join(random.choices(string.digits, k=6))
    user.verification_code = verification_code
    db.commit()  # BUG-28 FIX: was missing, reset code was never saved to DB
    
    try:
        email_service.send_password_reset_email(user.email, verification_code)
    except Exception as e:
        # Still return success to not break the flow or reveal info
        print(f"Failed to send reset email: {e}")
        
    return {"message": "If your email is registered, you will receive a reset code."}

@app.post("/api/auth/reset-password")
def reset_password(req: ResetPasswordRequest, db: Session = Depends(database.get_db)):
    user = db.query(database.User).filter(database.User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user.verification_code != req.code:
        raise HTTPException(status_code=400, detail="Invalid reset code")
        
    user.hashed_password = auth.get_password_hash(req.new_password)
    user.verification_code = None
    db.commit()  # BUG-29 FIX: was missing, new password was never persisted
    
    return {"message": "Password reset successfully"}

@app.post("/api/auth/verify", response_model=Token)
def verify_email(payload: VerifyEmail, db: Session = Depends(database.get_db)):
    user = db.query(database.User).filter(database.User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_email_verified:
        raise HTTPException(status_code=400, detail="Email already verified")
        
    if user.verification_code != payload.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
        
    user.is_email_verified = True
    user.verification_code = None
    db.commit()  # BUG-30 FIX: was missing for non-admin users
    
    if user.email == "zmonemrahman@gmail.com":
        user.is_admin = True
        user.is_approved = True
        db.commit()
        
    if not user.is_approved:
        raise HTTPException(status_code=403, detail="Wait for admin approve")
        
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "is_admin": user.is_admin}

@app.post("/api/auth/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    email_lower = form_data.username.strip().lower()
    user = db.query(database.User).filter(database.User.email.ilike(email_lower)).first()
    if not user or not auth.verify_password(form_data.password.strip(), user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    
    if user.email == "zmonemrahman@gmail.com":
        user.is_admin = True
        user.is_approved = True
        user.is_email_verified = True
        db.commit()
        

        
    if not user.is_approved:
        raise HTTPException(status_code=403, detail="Wait for admin approve")
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "is_admin": user.is_admin}

# --- ADMIN ENDPOINTS ---
@app.get("/api/test-db")
def test_db(db: Session = Depends(database.get_db)):
    users = db.query(database.User).count()
    return {"count": users, "url": database.DATABASE_URL}

@app.get("/api/admin/users")
def get_all_users(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    users = db.query(database.User).all()
    return [{"id": str(u.id), "email": u.email, "is_admin": u.is_admin, "is_approved": u.is_approved} for u in users]

@app.post("/api/admin/users/{user_id}/approve")
def approve_user(user_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    target_user = db.query(database.User).filter(database.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    target_user.is_approved = True
    db.commit()
    return {"message": "User approved successfully"}

@app.delete("/api/admin/users/{user_id}")
def delete_user(user_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    target_user = db.query(database.User).filter(database.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    # Protect the owner account — can NEVER be deleted
    if target_user.email == "zmonemrahman@gmail.com":
        raise HTTPException(status_code=403, detail="Owner account cannot be deleted")
    db.delete(target_user)
    db.commit()
    return {"message": "User deleted"}


# --- SECURE ENDPOINTS ---
# Contacts endpoints removed

@app.post("/api/clean-inactive-leads")
def clean_inactive_leads(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    cutoff_date = datetime.utcnow() - timedelta(days=90)
    
    try:
        # Get all campaigns for the current user
        campaigns = db.query(database.Campaign.id).filter(database.Campaign.user_id == str(current_user.id)).all()
        campaign_ids = [c.id for c in campaigns]
        
        if not campaign_ids:
            return {"status": "success", "tagged_count": 0}
            
        # Get all leads across these campaigns
        leads = db.query(database.CampaignLead).filter(database.CampaignLead.campaign_id.in_(campaign_ids)).all()
        
        email_map = {}
        for lead in leads:
            email = lead.email.lower()
            if email not in email_map:
                email_map[email] = lead.created_at or datetime.utcnow()
            else:
                if lead.created_at and lead.created_at < email_map[email]:
                    email_map[email] = lead.created_at
                    
        tagged_count = 0
        for email, first_seen in email_map.items():
            # Skip if already in the inactive list
            existing = db.query(database.InactiveLeadList).filter(database.InactiveLeadList.email == email).first()
            if existing:
                continue
                
            lead_ids = [str(l.id) for l in leads if l.email.lower() == email]
            
            # Check last open
            last_open = db.query(database.TrackingLog).filter(
                database.TrackingLog.contact_id.in_(lead_ids),
                database.TrackingLog.event_type == 'lead_open'
            ).order_by(database.TrackingLog.timestamp.desc()).first()
            
            is_inactive = False
            if last_open:
                if last_open.timestamp < cutoff_date:
                    is_inactive = True
            else:
                if first_seen < cutoff_date:
                    is_inactive = True
                    
            if is_inactive:
                db.add(database.InactiveLeadList(email=email))
                tagged_count += 1
                
        db.commit()
        return {"status": "success", "tagged_count": tagged_count}
        
    except Exception as e:
        db.rollback()
        print(f"Error cleaning inactive leads: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during scan")

class LeadsValidateRequest(BaseModel):
    emails: List[str]

@app.post("/api/validate-leads")
def validate_leads(req: LeadsValidateRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    results = []
    # To prevent huge payloads from timing out the request, we limit to 500 max
    emails_to_check = req.emails[:500]
    
    # Pre-fetch inactive leads to check them
    inactive = db.query(database.InactiveLeadList.email).filter(database.InactiveLeadList.email.in_(emails_to_check)).all()
    inactive_emails = set(e[0] for e in inactive)
    
    for email in emails_to_check:
        if email in inactive_emails:
            results.append({"email": email, "valid": False, "reason": "Inactive Lead (No open > 90 days)"})
            continue
            
        val = email_service.validate_email_address(email)
        results.append({
            "email": email,
            "valid": val["valid"],
            "reason": val.get("reason", "")
        })
    return {"results": results}

@app.get("/api/campaigns")
def get_campaigns(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    # BUG-31 FIX: filter by user_id so users only see their own campaigns
    campaigns = db.query(database.Campaign).filter(database.Campaign.user_id == str(current_user.id)).order_by(database.Campaign.created_at.desc()).all()
    return [{
        "id": str(c.id),
        "subject": c.subject or "",
        "body": c.body or "",
        "type": c.type or "newsletter",
        "sent_count": c.sent_count or 0,
        "opens": c.opens or 0,
        "clicks": c.clicks or 0,
        "status": c.status or "draft",
        "is_ab_test": c.is_ab_test or False,
        "sent_count_a": c.sent_count_a or 0,
        "sent_count_b": c.sent_count_b or 0,
        "opens_a": c.opens_a or 0,
        "opens_b": c.opens_b or 0,
        "created_at": str(c.created_at) if c.created_at else None,
        "scheduled_at": str(c.scheduled_at) if c.scheduled_at else None,
    } for c in campaigns]

class PreflightRequest(BaseModel):
    subject: str
    body: str

@app.post("/api/preflight")
def run_preflight(req: PreflightRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Runs deliverability checks (spam score, Base64 checks) before sending."""
    result = email_service.check_spam_score(req.subject or "", req.body or "")
    
    # Check if accounts are active
    active_accounts = db.query(database.SendingAccount).filter(database.SendingAccount.is_active == True, database.SendingAccount.user_id == str(current_user.id)).count()
    if active_accounts == 0:
        result['warnings'].append("No active sending accounts found. Please configure an SMTP account.")
        result['score'] = max(0, result['score'] - 2)

    return result

@app.post("/api/campaigns/send")
def send_campaign(campaign: CampaignCreate, background_tasks: BackgroundTasks, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    # BUG FIX: Check leads BEFORE saving to DB to avoid orphan campaigns, unless it's a draft
    if not campaign.is_draft and (not campaign.leads or len(campaign.leads) == 0):
        raise HTTPException(status_code=400, detail="No leads provided for campaign")

    if campaign.is_draft:
        campaign_status = "draft"
    else:
        campaign_status = "scheduled" if campaign.scheduled_at else "processing"
    
    target_campaign = None
    if campaign.campaign_id:
        target_campaign = db.query(database.Campaign).filter(database.Campaign.id == campaign.campaign_id, database.Campaign.user_id == str(current_user.id)).first()
        
    if target_campaign:
        target_campaign.subject = campaign.subject
        target_campaign.body = campaign.body
        target_campaign.type = campaign.type
        target_campaign.status = campaign_status
        target_campaign.is_ab_test = campaign.is_ab_test
        target_campaign.subject_b = campaign.subject_b
        target_campaign.body_b = campaign.body_b
        target_campaign.scheduled_at = campaign.scheduled_at
        target_campaign.timezone = campaign.timezone
        target_campaign.delay_min = campaign.delay_min
        target_campaign.delay_max = campaign.delay_max
        db.commit()
        db.query(database.CampaignLead).filter(database.CampaignLead.campaign_id == str(target_campaign.id)).delete()
        db.commit()
        new_campaign = target_campaign
    else:
        new_campaign = database.Campaign(
            subject=campaign.subject,
            body=campaign.body,
            type=campaign.type,
            status=campaign_status,
            user_id=str(current_user.id),
            is_ab_test=campaign.is_ab_test,
            subject_b=campaign.subject_b,
            body_b=campaign.body_b,
            scheduled_at=campaign.scheduled_at,
            timezone=campaign.timezone,
            delay_min=campaign.delay_min,
            delay_max=campaign.delay_max
        )
        db.add(new_campaign)
        db.commit()

    if campaign.leads:
        for lead_in in campaign.leads:
            db_lead = database.CampaignLead(campaign_id=str(new_campaign.id), name=lead_in.name, email=lead_in.email, company=lead_in.company)
            db.add(db_lead)
            db.commit()
    
    if not campaign.is_draft:
        if campaign.scheduled_at:
            try:
                tz = pytz.timezone(campaign.timezone or "UTC")
                run_date = campaign.scheduled_at
                if run_date.tzinfo is None:
                    run_date = tz.localize(run_date)
                scheduler.add_job(
                    process_isolated_campaign, 
                    'date', 
                    run_date=run_date, 
                    args=[new_campaign.id], 
                    id=f"camp_{new_campaign.id}"
                )
            except Exception as e:
                new_campaign.status = "failed"
                db.add(new_campaign)
                db.commit()
                raise HTTPException(status_code=400, detail=f"Failed to schedule: {str(e)}")
        else:
            background_tasks.add_task(process_isolated_campaign, str(new_campaign.id))
            
    return {"status": "success", "campaign_id": str(new_campaign.id)}

@app.post("/api/campaigns/{campaign_id}/pause")
def pause_campaign(campaign_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    campaign = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if campaign.user_id != str(current_user.id) and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    if campaign.status == "processing":
        campaign.status = "paused"
        db.commit()
    return {"status": "success"}

@app.post("/api/campaigns/{campaign_id}/resume")
def resume_campaign(campaign_id: str, background_tasks: BackgroundTasks, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    campaign = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if campaign.user_id != str(current_user.id) and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    if campaign.status == "paused":
        campaign.status = "processing"
        db.commit()
        background_tasks.add_task(process_isolated_campaign, str(campaign.id))
    return {"status": "success"}

@app.delete("/api/campaigns/{campaign_id}")
def delete_campaign(campaign_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    campaign = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if campaign.user_id != str(current_user.id) and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this campaign")
    
    # Delete associated leads
    db.query(database.CampaignLead).filter(database.CampaignLead.campaign_id == str(campaign.id)).delete()
    db.commit()
    db.delete(campaign)
    db.commit()
    return {"status": "success"}

@app.get("/api/campaigns/{campaign_id}/leads")
def get_campaign_leads(campaign_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    campaign = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if campaign.user_id != str(current_user.id) and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to view this campaign's leads")
    
    leads = db.query(database.CampaignLead).filter(database.CampaignLead.campaign_id == str(campaign.id)).all()
    return [{
        "id": str(lead.id),
        "email": lead.email,
        "name": lead.name,
        "company": lead.company,
        "status": lead.status,
        "variant": getattr(lead, "variant", "")
    } for lead in leads]


def process_isolated_campaign(campaign_id: str):
    """Background task: send all leads for a campaign with unsubscribe check & proper DB persistence."""
    db = database.SessionLocal()
    try:
        _run_campaign(db, campaign_id)
    finally:
        db.close()

def _run_campaign(db, campaign_id):
    import time
    import random
    import os
    import email_service
    
    campaign_id = str(campaign_id)
    campaign = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
    if not campaign:
        return

    leads = list(db.query(database.CampaignLead).filter(database.CampaignLead.campaign_id == campaign_id, database.CampaignLead.status == 'pending').all())
    if not leads:
        # Check if all leads are done
        all_leads = list(db.query(database.CampaignLead).filter(database.CampaignLead.campaign_id == campaign_id).all())
        if all_leads and all(l.status != "pending" for l in all_leads):
            if campaign.status != "completed":
                campaign.status = "completed"
                db.commit()
        else:
            campaign.status = "failed"
            db.commit()
        return
    
    # BUG FIX: Re-fetch accounts from DB each time (not stale in-memory list)
    accounts = list(db.query(database.SendingAccount).filter(database.SendingAccount.is_active == True, database.SendingAccount.user_id == campaign.user_id).all())
    if not accounts:
        campaign.status = "failed"
        db.commit()
        print(f"Campaign {campaign_id} failed: No active sending accounts.")
        return
    
    # BUG FIX: Build unsubscribe set for fast lookup
    unsub_emails = set(u.email.lower() for u in db.query(database.UnsubscribeList).all())
    
    success_count_a = 0
    success_count_b = 0
    base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    delay_min = campaign.delay_min if campaign.delay_min else 45
    delay_max = campaign.delay_max if campaign.delay_max else 120
    
    def get_available_account():
        # BUG FIX: Re-fetch from DB to get accurate sent_today count
        for acc_doc in db.query(database.SendingAccount).filter(database.SendingAccount.is_active == True, database.SendingAccount.user_id == campaign.user_id).all():
            # DELIVERABILITY: Enforce warmup limits
            if acc_doc.warmup_enabled:
                effective_limit = acc_doc.warmup_daily_limit or 5
                if acc_doc.warmup_sent_today >= effective_limit:
                    continue
            if acc_doc.sent_today < (acc_doc.daily_limit or 500):
                return acc_doc
        return None
    
    def send_to_lead(lead, subject, body, variant_label=None):
        nonlocal success_count_a, success_count_b
        
        c = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
        if c and c.status == "paused":
            return False  # Signal to abort loop
            
        # Skip unsubscribed
        if lead.email.lower() in unsub_emails:
            lead.status = "unsubscribed"
            db.commit()
            return True
            
        # Deliverability: Validate email format & MX record before sending
        validation = email_service.validate_email_address(lead.email)
        if not validation['valid']:
            lead.status = "invalid"
            db.commit()
            print(f"Skipping invalid email {lead.email}: {validation['reason']}")
            return True
            
        acc = get_available_account()
        if not acc:
            print("All accounts reached daily limit.")
            return False  # signal to stop
        pixel_url = f"{base_url}/api/track/lead_open/{campaign_id}/{lead.id}"
        body_with_pixel = email_service.inject_tracking_pixel(body, pixel_url)
        click_track_url = f"{base_url}/api/track/click/{campaign_id}/{lead.id}"
        body_with_tracking = email_service.inject_click_tracking(body_with_pixel, click_track_url)
        if variant_label:
            lead.variant = variant_label
        try:
            sent = email_service.send_single_email(subject, body_with_tracking, lead.email, account=acc, lead_name=lead.name or '', lead_company=lead.company or '')
            if sent:
                lead.status = "sent"
                # BUG FIX: Persist sent_today to DB immediately
                acc.sent_today += 1
                db.commit()
                if acc.warmup_enabled:
                    acc.warmup_sent_today += 1
                    db.commit()
                if variant_label == 'B':
                    success_count_b += 1
                else:
                    success_count_a += 1
            else:
                lead.status = "bounced"
        except Exception as e:
            print(f"Send error for {lead.email}: {e}")
            lead.status = "bounced"
        db.commit()
        return True

    if campaign.is_ab_test:
        random.shuffle(leads)
        midpoint = len(leads) // 2
        leads_a = leads[:midpoint]
        leads_b = leads[midpoint:]
        for lead in leads_a:
            result = send_to_lead(lead, campaign.subject, campaign.body, 'A')
            if result is False: break
            time.sleep(random.randint(delay_min, delay_max))
        for lead in leads_b:
            subj_b = campaign.subject_b or campaign.subject
            body_b = campaign.body_b or campaign.body
            result = send_to_lead(lead, subj_b, body_b, 'B')
            if result is False: break
            time.sleep(random.randint(delay_min, delay_max))
        campaign.sent_count_a += success_count_a
        campaign.sent_count_b += success_count_b
        campaign.sent_count = campaign.sent_count_a + campaign.sent_count_b
    else:
        for lead in leads:
            result = send_to_lead(lead, campaign.subject, campaign.body)
            if result is False: break
            time.sleep(random.randint(delay_min, delay_max))
        campaign.sent_count += success_count_a

    # Only mark completed if not paused
    c = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
    if c and c.status != "paused":
        c.status = "completed"
        c.sent_count_a = (c.sent_count_a or 0) + success_count_a
        c.sent_count_b = (c.sent_count_b or 0) + success_count_b
        c.sent_count = (c.sent_count or 0) + success_count_a + success_count_b
        db.commit()
        trigger_webhook(c.user_id or "", "campaign_completed", {"campaign_id": str(c.id), "status": "completed"})

@app.get("/api/track/lead_open/{campaign_id}/{lead_id}")
def track_lead_open(campaign_id: str, lead_id: str, db: Session = Depends(database.get_db)):
    existing = db.query(database.TrackingLog).filter(database.TrackingLog.campaign_id == campaign_id, database.TrackingLog.contact_id == lead_id, database.TrackingLog.event_type == 'lead_open').first()
    if not existing:
        log = database.TrackingLog(campaign_id=campaign_id, contact_id=lead_id, event_type="lead_open")
        db.add(log)
        db.commit()
        campaign = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
        lead = db.query(database.CampaignLead).filter(database.CampaignLead.id == lead_id).first()
        if campaign and lead:
            if lead.status == 'sent':
                lead.status = 'opened'
            
            if campaign.is_ab_test:
                if lead.variant == 'A':
                    campaign.opens_a = (campaign.opens_a or 0) + 1
                elif lead.variant == 'B':
                    campaign.opens_b = (campaign.opens_b or 0) + 1
                campaign.opens = (campaign.opens_a or 0) + (campaign.opens_b or 0)
            else:
                campaign.opens = (campaign.opens or 0) + 1
            db.commit()
    return FileResponse(os.path.join(os.path.dirname(__file__), "pixel.gif"), media_type="image/gif")


@app.get("/api/track/click/{campaign_id}/{contact_id}")
def track_click(campaign_id: str, contact_id: str, url: str, db: Session = Depends(database.get_db)):
    existing = db.query(database.TrackingLog).filter(database.TrackingLog.campaign_id == campaign_id, database.TrackingLog.contact_id == contact_id, database.TrackingLog.event_type == 'click', database.TrackingLog.url == url).first()
    if not existing:
        log = database.TrackingLog(campaign_id=campaign_id, contact_id=contact_id, event_type="click", url=url)
        db.add(log)
        db.commit()
        campaign = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
        lead = db.query(database.CampaignLead).filter(database.CampaignLead.id == contact_id).first()
        
        if lead and lead.status in ['sent', 'opened']:
            lead.status = 'clicked'
            
        if campaign:
            campaign.clicks = (campaign.clicks or 0) + 1
        db.commit()
    return RedirectResponse(url=url)


# --- SERVE FRONTEND ---
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")
    

# --- Sending Accounts Schema ---
class SendingAccountCreate(BaseModel):
    name: Optional[str] = None
    email: str
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    daily_limit: int = 500
    imap_server: Optional[str] = None
    imap_port: int = 993
    imap_password: Optional[str] = None
    warmup_enabled: bool = False
    warmup_daily_limit: int = 5
    warmup_increment_per_day: int = 2

class SendingAccountUpdate(BaseModel):
    is_active: bool

# --- Sending Accounts API Endpoints ---
@app.get("/api/sending-accounts")
def get_sending_accounts(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    accounts = db.query(database.SendingAccount).filter(database.SendingAccount.user_id == str(current_user.id)).all()
    # Mask passwords for safety
    result = []
    for acc in accounts:
        result.append({
            "id": str(acc.id),
            "name": acc.name,
            "email": acc.email,
            "smtp_server": acc.smtp_server,
            "smtp_port": acc.smtp_port,
            "smtp_username": acc.smtp_username,
            "daily_limit": acc.daily_limit,
            "sent_today": acc.sent_today,
            "is_active": acc.is_active,
            "imap_server": acc.imap_server,
            "imap_port": acc.imap_port,
            "warmup_enabled": acc.warmup_enabled,
            "warmup_daily_limit": acc.warmup_daily_limit,
            "warmup_increment_per_day": acc.warmup_increment_per_day,
            "warmup_sent_today": acc.warmup_sent_today,
            "health_score": acc.health_score,
            "created_at": acc.created_at
        })
    return result

@app.post("/api/sending-accounts")
def create_sending_account(acc: SendingAccountCreate, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    # Check if email already exists for this user
    existing = db.query(database.SendingAccount).filter(database.SendingAccount.email == acc.email).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"A sending account with email '{acc.email}' already exists.")
    
    # 1. Verify SMTP Connection
    import email_service
    smtp_check = email_service.verify_smtp_credentials(acc.smtp_server, acc.smtp_port, acc.smtp_username, acc.smtp_password)
    if smtp_check['status'] != 'success':
        raise HTTPException(status_code=400, detail=smtp_check['detail'])
        
    # 2. Verify IMAP Connection if warmup enabled
    if acc.warmup_enabled:
        if not acc.imap_server or not acc.imap_password:
            raise HTTPException(status_code=400, detail="IMAP server and password are required for Warmup.")
        imap_check = email_service.verify_imap_credentials(acc.imap_server, acc.imap_port, acc.smtp_username, acc.imap_password)
        if imap_check['status'] != 'success':
            raise HTTPException(status_code=400, detail=imap_check['detail'])

    try:
        new_acc = database.SendingAccount(
            user_id=str(current_user.id),
            name=acc.name,
            email=acc.email,
            smtp_server=acc.smtp_server,
            smtp_port=acc.smtp_port,
            smtp_username=acc.smtp_username,
            smtp_password=acc.smtp_password,
            daily_limit=acc.daily_limit,
            is_active=True,
            imap_server=acc.imap_server,
            imap_port=acc.imap_port,
            imap_password=acc.imap_password,
            warmup_enabled=acc.warmup_enabled,
            warmup_daily_limit=acc.warmup_daily_limit,
            warmup_increment_per_day=acc.warmup_increment_per_day
        )
        db.add(new_acc)
        db.commit()
        return {"status": "success", "id": str(new_acc.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save account: {str(e)}")

@app.put("/api/sending-accounts/{acc_id}")
def edit_sending_account(acc_id: str, acc: SendingAccountCreate, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    existing_acc = db.query(database.SendingAccount).filter(database.SendingAccount.id == acc_id, database.SendingAccount.user_id == str(current_user.id)).first()
    if not existing_acc:
        raise HTTPException(status_code=404, detail="Account not found.")
        
    email_check = db.query(database.SendingAccount).filter(database.SendingAccount.email == acc.email, database.SendingAccount.id != acc_id).first()
    if email_check:
        raise HTTPException(status_code=400, detail=f"A sending account with email '{acc.email}' already exists.")

    import email_service
    smtp_check = email_service.verify_smtp_credentials(acc.smtp_server, acc.smtp_port, acc.smtp_username, acc.smtp_password)
    if smtp_check['status'] != 'success':
        raise HTTPException(status_code=400, detail=smtp_check['detail'])
        
    if acc.warmup_enabled:
        if not acc.imap_server or not acc.imap_password:
            raise HTTPException(status_code=400, detail="IMAP server and password are required for Warmup.")
        imap_check = email_service.verify_imap_credentials(acc.imap_server, acc.imap_port, acc.smtp_username, acc.imap_password)
        if imap_check['status'] != 'success':
            raise HTTPException(status_code=400, detail=imap_check['detail'])

    try:
        existing_acc.name = acc.name
        existing_acc.email = acc.email
        existing_acc.smtp_server = acc.smtp_server
        existing_acc.smtp_port = acc.smtp_port
        existing_acc.smtp_username = acc.smtp_username
        existing_acc.smtp_password = acc.smtp_password
        existing_acc.daily_limit = acc.daily_limit
        existing_acc.imap_server = acc.imap_server
        existing_acc.imap_port = acc.imap_port
        existing_acc.imap_password = acc.imap_password
        existing_acc.warmup_enabled = acc.warmup_enabled
        existing_acc.warmup_daily_limit = acc.warmup_daily_limit
        existing_acc.warmup_increment_per_day = acc.warmup_increment_per_day
        db.commit()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not update account: {str(e)}")

@app.delete("/api/sending-accounts/{acc_id}")
def delete_sending_account(acc_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    acc = db.query(database.SendingAccount).filter(database.SendingAccount.id == acc_id, database.SendingAccount.user_id == str(current_user.id)).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(acc)
    db.commit()
    return {"status": "success"}

@app.patch("/api/sending-accounts/{acc_id}")
def update_sending_account_status(acc_id: str, update_data: SendingAccountUpdate, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    acc = db.query(database.SendingAccount).filter(database.SendingAccount.id == acc_id, database.SendingAccount.user_id == str(current_user.id)).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    acc.is_active = update_data.is_active
    db.commit()
    return {"status": "success"}

class SpamCheckRequest(BaseModel):
    content: str
    subject: Optional[str] = ""

@app.post("/api/spam-check")
def check_spam_score_endpoint(req: SpamCheckRequest, db: Session = Depends(database.get_db)):
    # Use enhanced spam checker from email_service
    result = email_service.check_spam_score(req.subject or '', req.content or '')
    return result

# NOTE: BUG-45 FIX - Duplicate unprotected AI endpoints removed.
# The authenticated versions are defined above at /api/ai/chat, /api/ai/generate,
# /api/ai/optimize-subject, /api/ai/generate-icebreakers, /api/ai/autopilot

# --- SETTINGS ENDPOINTS ---
class GeminiKeyRequest(BaseModel):
    gemini_api_key: str

class GroqKeyRequest(BaseModel):
    groq_api_key: str

@app.get("/api/settings")
def get_settings(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    return {
        "gemini_api_key": current_user.gemini_api_key or "",
        "groq_api_key": current_user.groq_api_key or "",
    }

@app.post("/api/settings/gemini")
def save_gemini_key(req: GeminiKeyRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    current_user.gemini_api_key = req.gemini_api_key
    db.commit()
    os.environ["GEMINI_API_KEY"] = req.gemini_api_key
    return {"ok": True, "message": "Gemini API key saved"}

@app.post("/api/settings/groq")
def save_groq_key(req: GroqKeyRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    current_user.groq_api_key = req.groq_api_key
    db.commit()
    os.environ["GROQ_API_KEY"] = req.groq_api_key
    return {"ok": True, "message": "Groq API key saved"}


# --- UNSUBSCRIBE ENDPOINTS ---
@app.get('/unsubscribe/{token}')
def unsubscribe(token: str, db: Session = Depends(database.get_db)):
    try:
        email = base64.b64decode(token).decode('utf-8')
        existing = db.query(database.UnsubscribeList).filter(database.UnsubscribeList.email == email).first()
        if not existing:
            new_unsub = database.UnsubscribeList(email=email)
            db.add(new_unsub)
            db.commit()
            # db.commit()
        return Response(content="<html><body style='font-family:sans-serif;text-align:center;padding:50px;'><h2>Unsubscribed Successfully</h2><p>You will no longer receive emails from us.</p></body></html>", media_type='text/html')
    except:
        raise HTTPException(status_code=400, detail='Invalid token')

@app.get('/api/unsubscribes')
def get_unsubscribes(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    # BUG FIX: return serializable dicts, accessible to all users
    unsubs = db.query(database.UnsubscribeList).all()
    return [{"email": u.email, "unsubscribed_at": str(u.unsubscribed_at)} for u in unsubs]


# --- BOUNCES ENDPOINT ---
@app.get('/api/bounces')
def get_bounces(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    # BUG FIX: return serializable dicts
    bounces = db.query(database.CampaignLead).filter(database.CampaignLead.status == 'bounced').all()
    return [{"email": l.email, "campaign_id": l.campaign_id, "name": l.name} for l in bounces]


# --- REPLIES ENDPOINT ---
@app.get('/api/replies')
def get_replies(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    # BUG FIX: return serializable dicts
    replies = db.query(database.Reply).order_by(database.Reply.received_at.desc()).all()
    return [{
        "id": str(r.id),
        "account_id": r.account_id,
        "sender_email": r.sender_email,
        "subject": r.subject,
        "body": r.body,
        "sentiment": r.sentiment,
        "received_at": str(r.received_at)
    } for r in replies]


# --- WEBHOOK ENDPOINTS ---
import requests
import threading

def trigger_webhook(user_id: str, event_type: str, payload: dict):
    db = database.SessionLocal()
    """BUG FIX: was calling requests.post twice (once direct, once in thread). Now only in thread."""
    if not user_id:
        return
    webhook = db.query(database.Webhook).filter(database.Webhook.user_id == user_id).first()
    if not webhook or not webhook.url:
        db.close()
        return
        
    webhook_url = webhook.url
    db.close()
    
    def _send():
        try:
            import requests
            requests.post(webhook_url, json={"event": event_type, "data": payload}, timeout=5)
        except Exception as e:
            print(f"Webhook error: {e}")
    threading.Thread(target=_send, daemon=True).start()

class WebhookRequest(BaseModel):
    url: str

@app.get('/api/webhook')
def get_webhook(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    webhook = db.query(database.Webhook).filter(database.Webhook.user_id == str(current_user.id)).first()
    return {"url": webhook.url if webhook else ""}

@app.post('/api/webhook')
def save_webhook(req: WebhookRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    webhook = db.query(database.Webhook).filter(database.Webhook.user_id == str(current_user.id)).first()
    if not webhook:
        webhook = database.Webhook(user_id=str(current_user.id), url=req.url)
        db.add(webhook)
    else:
        webhook.url = req.url
    db.commit()
    return {"ok": True}

@app.get("/{full_path:path}")
def serve_frontend(full_path: str, db: Session = Depends(database.get_db)):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API route not found")
    # Read file fresh every time - bypasses any server-side caching
    index_path = os.path.join(frontend_path, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    return Response(
        content=content,
        media_type="text/html",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0",
            "Surrogate-Control": "no-store",
        }
    )
