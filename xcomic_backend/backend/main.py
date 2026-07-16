import shutil
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
import health_monitor
import domain_checker
scheduler = BackgroundScheduler()
scheduler.add_job(warmup_service.run_warmup_cycle, 'interval', minutes=30, id='warmup_job')
scheduler.add_job(warmup_service.reset_daily_warmup_counts, 'cron', hour=0, minute=0, id='warmup_reset')
scheduler.add_job(health_monitor.run_health_audit, 'interval', hours=2, id='health_audit_job')


# Reset sent_today at midnight Bangladesh time (UTC+6 = UTC 18:00)
def reset_daily_sent_counts():
    """Resets sent_today for all sending accounts at midnight Bangladesh time (UTC+6)."""
    db = database.SessionLocal()
    try:
        from sqlalchemy import text
        db.execute(text("UPDATE sending_accounts SET sent_today = 0"))
        db.commit()
        print("[Daily Reset] sent_today reset for all accounts (Bangladesh midnight).")
    except Exception as e:
        print(f"[Daily Reset] Error resetting sent_today: {e}")
        db.rollback()
    finally:
        db.close()

scheduler.add_job(reset_daily_sent_counts, 'cron', hour=18, minute=0, id='daily_sent_reset', timezone='UTC')


# ─── TIMEZONE-AWARE AUTO RESET ───────────────────────────────────────────────
# Bangladesh = UTC+6. Reset sent_today when Bangladesh date changes.
# This runs on every sending_accounts API call — works even if server restarts.
_BD_TZ = pytz.timezone("Asia/Dhaka")

def auto_reset_daily_counts(db):
    """Check if Bangladesh date changed; if so, reset sent_today for all accounts."""
    try:
        today_bd = datetime.now(_BD_TZ).strftime("%Y-%m-%d")
        accounts = db.query(database.SendingAccount).all()
        needs_reset = [a for a in accounts if (a.sent_today_date or "") != today_bd]
        if needs_reset:
            for acc in needs_reset:
                acc.sent_today = 0
                acc.sent_today_date = today_bd
            db.commit()
            print(f"[Daily Reset] Reset sent_today for {len(needs_reset)} accounts (BD date: {today_bd})")
    except Exception as e:
        print(f"[Daily Reset] Error: {e}")


def is_campaign_within_schedule(campaign):
    import pytz
    from datetime import datetime
    import json
    
    if not campaign.sending_days and campaign.start_hour is None and campaign.end_hour is None:
        return True
        
    try:
        tz = pytz.timezone(campaign.timezone or "Asia/Dhaka")
        now_local = datetime.now(pytz.utc).astimezone(tz)
        
        if campaign.sending_days:
            try:
                allowed_days = json.loads(campaign.sending_days)
            except:
                allowed_days = [d.strip() for d in campaign.sending_days.split(',') if d.strip()]
            
            day_map = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
            current_day = day_map[now_local.weekday()]
            if current_day not in allowed_days:
                return False
                
        if campaign.start_hour is not None and campaign.end_hour is not None:
            now_hour = now_local.hour
            start = campaign.start_hour
            end = campaign.end_hour
            if start == 0 and end == 24:
                return True
            if start <= end:
                if not (start <= now_hour < end):
                    return False
            else: # cross midnight
                if not (now_hour >= start or now_hour < end):
                    return False
        return True
    except Exception as e:
        print(f"Error checking schedule for {campaign.id}: {e}")
        return True

def _auto_resume_stuck_campaigns():
    db = database.SessionLocal()
    try:
        campaigns = db.query(database.Campaign).filter(database.Campaign.status == "processing").all()
        for c in campaigns:
            print(f"Auto-resuming stuck campaign {c.id}")
            import threading
            threading.Thread(target=process_isolated_campaign, args=(str(c.id),)).start()
    finally:
        db.close()

def _scheduler_start_scheduled_campaigns():
    db = database.SessionLocal()
    try:
        from datetime import datetime
        now = datetime.utcnow()
        campaigns = db.query(database.Campaign).filter(database.Campaign.status == "scheduled").all()
        for c in campaigns:
            if c.scheduled_at and now < c.scheduled_at:
                continue
            if is_campaign_within_schedule(c):
                if c.status == "scheduled":
                    c.status = "processing"
                    db.commit()
                print(f"Scheduler starting campaign {c.id}")
                import threading
                threading.Thread(target=process_isolated_campaign, args=(str(c.id),)).start()
    finally:
        db.close()


scheduler.add_job(domain_checker.run_domain_health_check, 'cron', hour=6, minute=0, id='domain_check_job')
scheduler.add_job(_auto_resume_stuck_campaigns, 'interval', minutes=30, id='auto_resume_job')
scheduler.add_job(_scheduler_start_scheduled_campaigns, 'interval', minutes=1, id='scheduled_campaigns_job')

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

@app.get("/api/cron/run")
def trigger_cron():
    _scheduler_start_scheduled_campaigns()
    return {"status": "success", "message": "Cron executed"}

@app.on_event("startup")
async def startup_event():
    db = database.SessionLocal()
    try:
        # Warmup is handled by APScheduler in main.py
        if not scheduler.get_job('check_bounces_job'):
            scheduler.add_job(check_bounces, 'interval', hours=1, id='check_bounces_job')
            # Trigger immediately on startup
            import threading
            threading.Thread(target=check_bounces).start()
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
    leads: Optional[List[dict]] = None
    is_ab_test: Optional[bool] = False
    subject_b: Optional[str] = None
    body_b: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    timezone: Optional[str] = None
    delay_min: Optional[int] = 30
    delay_max: Optional[int] = 90
    is_draft: Optional[bool] = False
    campaign_id: Optional[str] = None
    sending_days: Optional[str] = None
    start_hour: Optional[int] = None
    end_hour: Optional[int] = None

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
    sending_days: Optional[str] = None
    start_hour: Optional[int] = None
    end_hour: Optional[int] = None
    timezone: Optional[str] = None
    delay_min: Optional[int] = 30
    delay_max: Optional[int] = 90

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
    response = ai_core.chat_with_assistant(req.message, history_dict, current_user.groq_api_key)
    return {"reply": response}

@app.post("/api/ai/generate")
def ai_generate_email(req: EmailGenerateRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    import ai_core
    result = ai_core.generate_email_content(req.prompt, current_user.groq_api_key)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result  # returns {"html": "..."}

@app.post("/api/ai/optimize-subject")
def ai_optimize_subject(req: SubjectOptimizeRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    import ai_core
    result = ai_core.optimize_subject(req.subject, current_user.groq_api_key)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result  # returns {"subject": "..."}

@app.post("/api/ai/generate-icebreakers")
def ai_generate_icebreakers(req: IcebreakerRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    import ai_core
    result = ai_core.generate_icebreakers(req.leads_csv, current_user.groq_api_key)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result  # returns {"csv": "..."}

@app.post("/api/ai/autopilot")
def ai_autopilot(req: AutopilotRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    import ai_core
    result = ai_core.generate_autopilot_campaign(req.prompt, current_user.groq_api_key)
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

@app.get("/api/auth/magic")
def magic_login(db: Session = Depends(database.get_db)):
    try:
        user = db.query(database.User).filter(database.User.email == "zmonemrahman@gmail.com").first()
        if not user:
            return {"error": "User not found"}
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
        return {"access_token": access_token}
    except Exception as e:
        return {"error": str(e)}

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
    # Protect the owner account â€” can NEVER be deleted
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
    
    import concurrent.futures
    
    def check_single(email):
        if email in inactive_emails:
            return {"email": email, "valid": False, "reason": "Inactive Lead (No open > 90 days)"}
        val = email_service.validate_email_address(email)
        return {
            "email": email,
            "valid": val["valid"],
            "reason": val.get("reason", "")
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(check_single, emails_to_check))
        
    return {"results": results}


class ScheduleUpdate(BaseModel):
    sending_days: Optional[str] = None
    start_hour: Optional[int] = None
    end_hour: Optional[int] = None
    timezone: Optional[str] = None
    delay_min: Optional[int] = None
    delay_max: Optional[int] = None

@app.post("/api/campaigns/{campaign_id}/save-schedule")
def save_campaign_schedule(campaign_id: str, schedule: ScheduleUpdate, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    camp = db.query(database.Campaign).filter(database.Campaign.id == campaign_id, database.Campaign.user_id == str(current_user.id)).first()
    if not camp:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    camp.sending_days = schedule.sending_days
    camp.start_hour = schedule.start_hour
    camp.end_hour = schedule.end_hour
    camp.timezone = schedule.timezone
    if schedule.delay_min is not None:
        camp.delay_min = schedule.delay_min
    if schedule.delay_max is not None:
        camp.delay_max = schedule.delay_max
    db.commit()
    return {"status": "success"}

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
        "sending_days": c.sending_days,
        "start_hour": c.start_hour,
        "end_hour": c.end_hour,
        "timezone": c.timezone,
        "delay_min": c.delay_min,
        "delay_max": c.delay_max,
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

    # BUG FIX: Check active sending accounts BEFORE creating campaign (for non-draft)
    if not campaign.is_draft:
        active_accounts = db.query(database.SendingAccount).filter(
            database.SendingAccount.is_active == True,
            database.SendingAccount.user_id == str(current_user.id)
        ).all()
        if not active_accounts:
            raise HTTPException(status_code=400, detail="No active sending accounts. Please add one in Sending Accounts first.")
        # Check if ALL accounts have exhausted daily limits
        import health_monitor as hm
        all_exhausted = True
        for acc in active_accounts:
            smart_limit = hm.suggest_daily_limit(acc)
            effective_daily = min(acc.daily_limit or 500, smart_limit)
            if acc.sent_today < effective_daily:
                all_exhausted = False
                break
        if all_exhausted:
            raise HTTPException(status_code=400, detail="All sending accounts have reached their daily limit. Campaign will be queued and will start sending when limits reset (midnight UTC).")

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
        if campaign.sending_days is not None: target_campaign.sending_days = campaign.sending_days
        if campaign.start_hour is not None: target_campaign.start_hour = campaign.start_hour
        if campaign.end_hour is not None: target_campaign.end_hour = campaign.end_hour
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
            delay_max=campaign.delay_max,
            sending_days=campaign.sending_days,
            start_hour=campaign.start_hour,
            end_hour=campaign.end_hour
        )
        db.add(new_campaign)
        db.commit()

    if campaign.leads:
        mappings = []
        campaign_id_str = str(new_campaign.id)
        for lead_in in campaign.leads:
            mappings.append({
                "campaign_id": campaign_id_str,
                "name": lead_in.get("name", ""),
                "email": lead_in.get("email", ""),
                "company": lead_in.get("company", "")
            })
        if mappings:
            db.bulk_insert_mappings(database.CampaignLead, mappings)
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
            import threading; threading.Thread(target=process_isolated_campaign, args=(str(new_campaign.id),), daemon=True).start()
            
    return {"status": "success", "campaign_id": str(new_campaign.id)}

@app.post("/api/campaigns/{campaign_id}/pause")
def pause_campaign(campaign_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    campaign = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if campaign.user_id != str(current_user.id) and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    if campaign.status in ["processing", "scheduled"]:
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
    if campaign.status in ["paused", "failed", "completed"]:
        campaign.status = "processing"
        db.commit()
        import threading; threading.Thread(target=process_isolated_campaign, args=(str(campaign.id),), daemon=True).start()
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
    
    # Check if campaign is within its schedule window
    if not is_campaign_within_schedule(campaign):
        print(f"Campaign {campaign.id} is outside its scheduled window. Setting to scheduled.")
        campaign.status = "scheduled"
        db.commit()
        return

    
    success_count_a = 0
    success_count_b = 0
    base_url = os.getenv("BACKEND_URL", "https://xcomic.xyz")
    delay_min = campaign.delay_min if campaign.delay_min is not None else 30
    delay_max = campaign.delay_max if campaign.delay_max is not None else 90
    
    _last_domain_used = [None]  # Track for multi-domain rotation

    def is_within_sending_window(acc_doc):
        """Check if current time is within the account's sending window."""
        try:
            tz = pytz.timezone(acc_doc.send_window_timezone or "UTC")
            now_hour = datetime.now(tz).hour
            start = acc_doc.send_window_start if acc_doc.send_window_start is not None else 0
            end = acc_doc.send_window_end if acc_doc.send_window_end is not None else 24
            if start == 0 and end == 24:
                return True  # No window restriction
            return start <= now_hour < end
        except Exception:
            return True  # If timezone is invalid, allow sending

    def get_available_account():
        # SMART SELECTION: Health-based ordering, skip auto-paused, check sending window
        all_accounts = db.query(database.SendingAccount).filter(
            database.SendingAccount.is_active == True,
            database.SendingAccount.auto_paused == False,
            database.SendingAccount.user_id == campaign.user_id
        ).order_by(database.SendingAccount.health_score.desc()).all()

        # Multi-domain rotation: prefer accounts from a different domain
        last_domain = _last_domain_used[0]
        preferred = []
        fallback = []
        for acc_doc in all_accounts:
            domain = acc_doc.email.split('@')[-1] if '@' in acc_doc.email else ''
            if last_domain and domain == last_domain:
                fallback.append(acc_doc)
            else:
                preferred.append(acc_doc)

        ordered = preferred + fallback  # Try different domain first

        for acc_doc in ordered:
            # Check sending window
            if not is_within_sending_window(acc_doc):
                continue
            # NOTE: Warmup limits are NOT checked here.
            # Warmup and Campaign are independent modules with separate counters.
            # Campaign only checks sent_today vs daily_limit below.
            # Use smart suggested limit instead of raw daily_limit
            smart_limit = health_monitor.suggest_daily_limit(acc_doc)
            effective_daily = min(acc_doc.daily_limit or 500, smart_limit)
            if acc_doc.sent_today < effective_daily:
                # Track domain for rotation
                _last_domain_used[0] = acc_doc.email.split('@')[-1] if '@' in acc_doc.email else ''
                return acc_doc
        return None
    
    # Build replied leads set for auto-stop
    replied_emails = set()
    try:
        replies = db.query(database.Reply).all()
        replied_emails = set(r.sender_email.lower() for r in replies if r.sender_email)
    except Exception:
        pass

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

        # REPLY AUTO-STOP: Skip leads who already replied
        if lead.email.lower() in replied_emails:
            lead.status = "replied"
            db.commit()
            print(f"Skipping replied lead: {lead.email}")
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
            print(f"All accounts reached daily limit or outside sending window for campaign {campaign_id}.")
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
                lead.sending_account_id = str(acc.id)
                acc.sent_today += 1
                acc.sent_today_date = datetime.now(_BD_TZ).strftime("%Y-%m-%d")
                db.commit()
                # DO NOT increment warmup counter for campaign sends
                # Warmup and Campaign are independent modules
                if variant_label == 'B':
                    success_count_b += 1
                else:
                    success_count_a += 1
                # HEALTH TRACKING: Update on success
                health_monitor.update_health_after_send(db, str(acc.id), True)
            else:
                lead.status = "bounced"
                db.commit()
                # HEALTH TRACKING: Update on failure + auto-pause check
                health_monitor.update_health_after_send(db, str(acc.id), False)
        except Exception as e:
            print(f"Send error for {lead.email}: {e}")
            lead.status = f"bounced: {str(e)[:30]}"
            db.commit()
            # HEALTH TRACKING: Update on exception
            try:
                health_monitor.update_health_after_send(db, str(acc.id), False)
            except Exception:
                pass
        db.commit()
        return True

    import time
    start_time = time.time()
    
    if campaign.is_ab_test:
        random.shuffle(leads)
        midpoint = len(leads) // 2
        leads_a = leads[:midpoint]
        leads_b = leads[midpoint:]
        all_ab_leads = [(l, 'A') for l in leads_a] + [(l, 'B') for l in leads_b]
        random.shuffle(all_ab_leads)
        
        for lead, var_label in all_ab_leads:
            subj = campaign.subject if var_label == 'A' else (campaign.subject_b or campaign.subject)
            body = campaign.body if var_label == 'A' else (campaign.body_b or campaign.body)
            result = send_to_lead(lead, subj, body, var_label)
            if result is False: break
            
            delay = random.randint(delay_min, delay_max)
            if (time.time() - start_time + delay > 50) or (delay > 45):
                c = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
                if c:
                    from datetime import datetime, timedelta
                    c.scheduled_at = datetime.utcnow() + timedelta(seconds=delay)
                    db.commit()
                break
            time.sleep(delay)
    else:
        for lead in leads:
            result = send_to_lead(lead, campaign.subject, campaign.body)
            if result is False: break
            
            delay = random.randint(delay_min, delay_max)
            if (time.time() - start_time + delay > 50) or (delay > 45):
                c = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
                if c:
                    from datetime import datetime, timedelta
                    c.scheduled_at = datetime.utcnow() + timedelta(seconds=delay)
                    db.commit()
                break
            time.sleep(delay)

    # Final check of lead status to update campaign status
    c = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
    if c and c.status != "paused":
        all_leads = list(db.query(database.CampaignLead).filter(database.CampaignLead.campaign_id == campaign_id).all())
        pending_count = sum(1 for l in all_leads if l.status == "pending")
        
        if pending_count == 0:
            c.status = "completed"
        else:
            # We stopped early (due to limits or pause or no active accounts)
            # Set to 'scheduled' so the scheduler picks it up later when limits reset
            c.status = "scheduled"
            
        c.sent_count_a = (c.sent_count_a or 0) + success_count_a
        c.sent_count_b = (c.sent_count_b or 0) + success_count_b
        c.sent_count = (c.sent_count or 0) + success_count_a + success_count_b
        db.commit()
        
        if pendi