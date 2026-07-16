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
import threading
import random
import string
from apscheduler.schedulers.background import BackgroundScheduler

active_campaign_threads = set()
campaign_thread_lock = threading.Lock()
import pytz

# Setup APScheduler
import warmup_service
import health_monitor
import domain_checker
scheduler = BackgroundScheduler()
from datetime import datetime
scheduler.add_job(warmup_service.run_warmup_cycle, 'interval', minutes=30, id='warmup_job', next_run_time=datetime.now())
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
        db.rollback()
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
import socket
try:
    _scheduler_lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _scheduler_lock_socket.bind(("127.0.0.1", 47200))
    scheduler.start()
    print("Scheduler started in this process.")
except socket.error:
    print("Scheduler already running in another process.")

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
            threading.Thread(target=warmup_service.run_warmup_cycle).start()
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
    name: Optional[str] = None
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
    track_opens: Optional[bool] = True
    track_clicks: Optional[bool] = True
    use_unsubscribe: Optional[bool] = True
    steps_json: Optional[str] = None
    max_emails_per_day: Optional[int] = 50
    daily_ramp_up: Optional[int] = 0

class CampaignResponse(BaseModel):
    id: str  # BUG-24 fix: MongoDB IDs are strings not ints
    name: Optional[str] = None
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
    track_opens: Optional[bool] = True
    track_clicks: Optional[bool] = True
    use_unsubscribe: Optional[bool] = True
    steps_json: Optional[str] = None
    max_emails_per_day: Optional[int] = 50
    daily_ramp_up: Optional[int] = 0
    current_daily_limit: Optional[int] = 50
    sent_today_campaign: Optional[int] = 0
    sent_today_date: Optional[str] = None
    
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
        if target_campaign and target_campaign.status == "processing":
            raise HTTPException(status_code=400, detail="Cannot edit a campaign that is currently processing. Pause it first.")
        
    if target_campaign:
        target_campaign.name = campaign.name
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
        target_campaign.sending_days = campaign.sending_days
        target_campaign.start_hour = campaign.start_hour
        target_campaign.end_hour = campaign.end_hour
        target_campaign.track_opens = campaign.track_opens
        target_campaign.track_clicks = campaign.track_clicks
        target_campaign.use_unsubscribe = campaign.use_unsubscribe
        target_campaign.steps_json = campaign.steps_json
        
        target_campaign.max_emails_per_day = campaign.max_emails_per_day
        target_campaign.daily_ramp_up = campaign.daily_ramp_up
        target_campaign.current_daily_limit = campaign.daily_ramp_up if (campaign.daily_ramp_up and campaign.daily_ramp_up > 0) else campaign.max_emails_per_day
        
        db.commit()
        db.query(database.CampaignLead).filter(database.CampaignLead.campaign_id == str(target_campaign.id)).delete()
        db.commit()
        new_campaign = target_campaign
    else:
        new_campaign = database.Campaign(
            name=campaign.name,
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
            end_hour=campaign.end_hour,
            track_opens=campaign.track_opens,
            track_clicks=campaign.track_clicks,
            use_unsubscribe=campaign.use_unsubscribe,
            steps_json=campaign.steps_json,
            max_emails_per_day=campaign.max_emails_per_day,
            daily_ramp_up=campaign.daily_ramp_up,
            current_daily_limit=campaign.daily_ramp_up if (campaign.daily_ramp_up and campaign.daily_ramp_up > 0) else campaign.max_emails_per_day
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
    
    with campaign_thread_lock:
        if campaign_id in active_campaign_threads:
            print(f"Campaign {campaign_id} is already running in a thread. Skipping duplicate execution.")
            return
        active_campaign_threads.add(campaign_id)
        
    db = database.SessionLocal()
    try:
        _run_campaign(db, campaign_id)
    finally:
        db.close()
        with campaign_thread_lock:
            active_campaign_threads.discard(campaign_id)

def _run_campaign(db, campaign_id):
    import time
    import random
    import os
    import email_service
    
    from sqlalchemy import or_, and_
    
    campaign_id = str(campaign_id)
    campaign = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
    if not campaign:
        return

    now = datetime.utcnow()
    today_str = datetime.now(_BD_TZ).strftime("%Y-%m-%d")
    
    # Check Campaign-level Date & Ramp Up
    if campaign.sent_today_date != today_str:
        campaign.sent_today_campaign = 0
        
        # If it's a new day, apply ramp up (but only if it's not the first time we ever send, i.e. sent_today_date is not None)
        if campaign.sent_today_date is not None:
            if getattr(campaign, 'daily_ramp_up', 0) > 0 and getattr(campaign, 'max_emails_per_day', 0) > 0:
                current_limit = getattr(campaign, 'current_daily_limit', 0)
                new_limit = current_limit + campaign.daily_ramp_up
                if new_limit > campaign.max_emails_per_day:
                    new_limit = campaign.max_emails_per_day
                campaign.current_daily_limit = new_limit
                
        campaign.sent_today_date = today_str
        db.commit()

    # Select leads that are pending, or sent and due for next step
    leads = list(db.query(database.CampaignLead).filter(
        database.CampaignLead.campaign_id == campaign_id,
        database.CampaignLead.replied == False,
        database.CampaignLead.status != 'unsubscribed',
        or_(
            database.CampaignLead.status == 'pending',
            and_(
                database.CampaignLead.status == 'sent', 
                database.CampaignLead.next_send_at != None, 
                database.CampaignLead.next_send_at <= now
            )
        )
    ).all())
    
    if not leads:
        # Check if all leads are done (no longer pending, and no future send date or already replied/unsubbed)
        all_leads = list(db.query(database.CampaignLead).filter(database.CampaignLead.campaign_id == campaign_id).all())
        is_finished = True
        for l in all_leads:
            if l.status == "pending" or (l.status == "sent" and l.next_send_at is not None and not l.replied):
                is_finished = False
                break
                
        if all_leads and is_finished:
            if campaign.status != "completed":
                campaign.status = "completed"
                db.commit()
        elif not all_leads:
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

    def get_available_account(db_session):
        # SMART SELECTION: Health-based ordering, skip auto-paused, check sending window
        all_accounts = db_session.query(database.SendingAccount).filter(
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

    def send_to_lead(db_session, lead, variant_label=None):
        nonlocal success_count_a, success_count_b
        
        c = db_session.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
        if not c or c.status == "paused":
            return False  # Signal to abort loop
            
        import json
        from datetime import timedelta
        steps = None
        if c.steps_json:
            try:
                steps = json.loads(c.steps_json)
            except Exception:
                pass
                
        current_step_idx = lead.current_step if lead.current_step is not None else 0
        
        # Default to campaign fields
        send_subject = c.subject
        send_body = c.body
        delay_days = -1
        
        if steps and len(steps) > current_step_idx:
            step_data = steps[current_step_idx]
            send_subject = step_data.get('subject', c.subject)
            if variant_label == 'B' and step_data.get('is_ab'):
                send_body = step_data.get('body_b') or step_data.get('body')
                send_subject = step_data.get('subject_b') or send_subject
            else:
                send_body = step_data.get('body', c.body)
                
            if len(steps) > current_step_idx + 1:
                next_step = steps[current_step_idx + 1]
                delay_days = int(next_step.get('wait', 0))
        elif steps and len(steps) <= current_step_idx:
            # Reached end of sequence
            lead.status = "completed"
            db_session.commit()
            return True
        else:
            # Fallback for old campaigns without steps
            if variant_label == 'B':
                send_subject = c.subject_b or c.subject
                send_body = c.body_b or c.body
            
        # Skip unsubscribed
        if lead.email.lower() in unsub_emails:
            lead.status = "unsubscribed"
            db_session.commit()
            return True

        # REPLY AUTO-STOP: Skip leads who already replied
        if lead.email.lower() in replied_emails:
            lead.status = "replied"
            db_session.commit()
            print(f"Skipping replied lead: {lead.email}")
            return True
            
        # Deliverability: Validate email format & MX record before sending
        validation = email_service.validate_email_address(lead.email)
        if not validation['valid']:
            lead.status = "invalid"
            db_session.commit()
            print(f"Skipping invalid email {lead.email}: {validation['reason']}")
            return True
            
        acc = get_available_account(db)
        if not acc:
            print(f"All accounts reached daily limit or outside sending window for campaign {campaign_id}.")
            return False  # signal to stop
        pixel_url = f"{base_url}/api/track/lead_open/{campaign_id}/{lead.id}"
        
        body_with_tracking = send_body
        if getattr(c, 'track_opens', True):
            body_with_tracking = email_service.inject_tracking_pixel(body_with_tracking, pixel_url)
            
        if getattr(c, 'track_clicks', True):
            click_track_url = f"{base_url}/api/track/click/{campaign_id}/{lead.id}"
            body_with_tracking = email_service.inject_click_tracking(body_with_tracking, click_track_url)
            
        if variant_label:
            lead.variant = variant_label
        try:
            use_unsub = getattr(c, 'use_unsubscribe', True)
            sent = email_service.send_single_email(send_subject, body_with_tracking, lead.email, account=acc, lead_name=lead.name or '', lead_company=lead.company or '', use_unsubscribe=use_unsub)
            if sent:
                lead.status = "sent"
                if delay_days > -1:
                    lead.next_send_at = datetime.utcnow() + timedelta(days=delay_days)
                else:
                    lead.next_send_at = None
                    lead.status = "completed"
                lead.current_step = current_step_idx + 1
                lead.sending_account_id = str(acc.id)
                db_session.query(database.SendingAccount).filter(database.SendingAccount.id == acc.id).update({
                    "sent_today": database.SendingAccount.sent_today + 1,
                    "sent_today_date": datetime.now(_BD_TZ).strftime("%Y-%m-%d")
                })
                
                db_session.query(database.Campaign).filter(database.Campaign.id == campaign_id).update({
                    "sent_today_campaign": database.Campaign.sent_today_campaign + 1
                })
                
                db_session.commit()
                # DO NOT increment warmup counter for campaign sends
                # Warmup and Campaign are independent modules
                if variant_label == 'B':
                    success_count_b += 1
                else:
                    success_count_a += 1
                # HEALTH TRACKING: Update on success
                health_monitor.update_health_after_send(db_session, str(acc.id), True)
            else:
                lead.status = "bounced"
                db_session.commit()
                # HEALTH TRACKING: Update on failure + auto-pause check
                health_monitor.update_health_after_send(db_session, str(acc.id), False)
        except Exception as e:
            print(f"Send error for {lead.email}: {e}")
            db_session.rollback()
            try:
                db_session.query(database.CampaignLead).filter(database.CampaignLead.id == lead.id).update({
                    "status": f"bounced: {str(e)[:30]}"
                })
                db_session.commit()
            except Exception:
                db_session.rollback()
            # HEALTH TRACKING: Update on exception
            try:
                health_monitor.update_health_after_send(db_session, str(acc.id), False)
            except Exception:
                pass
        db_session.commit()
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
            c_refresh = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
            if c_refresh and c_refresh.current_daily_limit and c_refresh.sent_today_campaign >= c_refresh.current_daily_limit:
                print(f"Campaign {campaign_id} reached its daily limit of {c_refresh.current_daily_limit}.")
                break
                
            result = send_to_lead(db, lead, var_label)
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
            c_refresh = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
            if c_refresh and c_refresh.current_daily_limit and c_refresh.sent_today_campaign >= c_refresh.current_daily_limit:
                print(f"Campaign {campaign_id} reached its daily limit of {c_refresh.current_daily_limit}.")
                break
                
            result = send_to_lead(db, lead)
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
        
        if pending_count == 0:
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
            
            # Track open stat on the sending account
            if getattr(lead, 'sending_account_id', None):
                try:
                    import health_monitor
                    health_monitor.update_health_after_open(db, lead.sending_account_id)
                except Exception as e:
                    print(f"Error updating health after open: {e}")
            
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
# Try to locate the frontend directory 'xcomic.xyz' dynamically.
# On local environment it might be 'frontend', on server it is 'xcomic.xyz'.
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_path = os.path.join(parent_dir, "xcomic.xyz")
if not os.path.exists(frontend_path):
    frontend_path = os.path.join(parent_dir, "frontend")

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
    is_active: Optional[bool] = None
    smart_limit_enabled: Optional[bool] = None
    warmup_enabled: Optional[bool] = None

# --- Sending Accounts API Endpoints ---
@app.get("/api/sending-accounts")
def get_sending_accounts(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    try:
        # Auto-reset sent_today based on Bangladesh timezone date
        auto_reset_daily_counts(db)
        accounts = db.query(database.SendingAccount).filter(database.SendingAccount.user_id == str(current_user.id)).all()
        # Mask passwords for safety
        result = []
        for acc in accounts:
            # Get domain health from cache
            domain = acc.email.split('@')[-1] if '@' in acc.email else ''
            domain_cache = db.query(database.DomainHealthCache).filter(database.DomainHealthCache.domain == domain).first() if domain else None

            # --- FIX: Recalculate health on the fly to ensure accuracy ---
            import health_monitor
            current_health = health_monitor.calculate_health_score(acc, db)
            if acc.health_score != current_health:
                acc.health_score = current_health
                db.commit()
            # -------------------------------------------------------------

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
                "warmup_total_sent": getattr(acc, "warmup_total_sent", 0) or 0,
                "smart_limit_enabled": getattr(acc, "smart_limit_enabled", False),
                "health_score": acc.health_score if acc.health_score is not None else 0,
                "created_at": str(acc.created_at),
                # --- New health fields ---
                "total_sent": acc.total_sent or 0,
                "total_bounced": acc.total_bounced or 0,
                "total_opened": acc.total_opened or 0,
                "total_replied": acc.total_replied or 0,
                "bounce_streak": acc.bounce_streak or 0,
                "auto_paused": acc.auto_paused or False,
                "auto_paused_reason": acc.auto_paused_reason,
                "suggested_daily_limit": health_monitor.suggest_daily_limit(acc),
                # --- Sending window ---
                "send_window_start": acc.send_window_start if acc.send_window_start is not None else 9,
                "send_window_end": acc.send_window_end if acc.send_window_end is not None else 17,
                "send_window_timezone": acc.send_window_timezone or "UTC",
                # --- Custom tracking ---
                "custom_tracking_domain": acc.custom_tracking_domain,
                # --- Domain health ---
                "domain_health": {
                    "has_spf": domain_cache.has_spf if domain_cache else None,
                    "has_dkim": domain_cache.has_dkim if domain_cache else None,
                    "has_dmarc": domain_cache.has_dmarc if domain_cache else None,
                    "is_blacklisted": domain_cache.is_blacklisted if domain_cache else None,
                    "is_catch_all": domain_cache.is_catch_all if domain_cache else None,
                    "last_checked": str(domain_cache.last_checked) if domain_cache and domain_cache.last_checked else None,
                } if domain_cache else None,
            })
        from fastapi.encoders import jsonable_encoder
        return jsonable_encoder(result)
    except Exception as e:
        import traceback
        return {"debug_error": str(e), "traceback": traceback.format_exc()}


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
    
    # If password is empty, keep existing. Otherwise verify new.
    final_smtp_pass = acc.smtp_password if acc.smtp_password and acc.smtp_password.strip() else existing_acc.smtp_password
    final_imap_pass = acc.imap_password if acc.imap_password and acc.imap_password.strip() else existing_acc.imap_password

    # Only verify if credentials changed or are provided
    if acc.smtp_password and acc.smtp_password.strip():
        smtp_check = email_service.verify_smtp_credentials(acc.smtp_server, acc.smtp_port, acc.smtp_username, final_smtp_pass)
        if smtp_check['status'] != 'success':
            raise HTTPException(status_code=400, detail=smtp_check['detail'])
        
    if acc.warmup_enabled and acc.imap_password and acc.imap_password.strip():
        if not acc.imap_server or not final_imap_pass:
            raise HTTPException(status_code=400, detail="IMAP server and password are required for Warmup.")
        imap_check = email_service.verify_imap_credentials(acc.imap_server, acc.imap_port, acc.smtp_username, final_imap_pass)
        if imap_check['status'] != 'success':
            raise HTTPException(status_code=400, detail=imap_check['detail'])

    try:
        existing_acc.name = acc.name
        existing_acc.email = acc.email
        existing_acc.smtp_server = acc.smtp_server
        existing_acc.smtp_port = acc.smtp_port
        existing_acc.smtp_username = acc.smtp_username
        existing_acc.smtp_password = final_smtp_pass
        existing_acc.daily_limit = acc.daily_limit
        existing_acc.imap_server = acc.imap_server
        existing_acc.imap_port = acc.imap_port
        existing_acc.imap_password = final_imap_pass
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
    if update_data.is_active is not None:
        acc.is_active = update_data.is_active
    if update_data.smart_limit_enabled is not None:
        acc.smart_limit_enabled = update_data.smart_limit_enabled
    if update_data.warmup_enabled is not None:
        acc.warmup_enabled = update_data.warmup_enabled
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

# ============================================================
# EMAIL HEALTH & DELIVERABILITY ENDPOINTS
# ============================================================

@app.get("/api/account-health/{acc_id}")
def get_account_health(acc_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Get detailed health report for a specific sending account."""
    acc = db.query(database.SendingAccount).filter(database.SendingAccount.id == acc_id, database.SendingAccount.user_id == str(current_user.id)).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return health_monitor.get_health_report(db, acc_id)

@app.get("/api/account-health-all")
def get_all_account_health(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Get health reports and suggested limits for all accounts."""
    accounts = db.query(database.SendingAccount).filter(database.SendingAccount.user_id == str(current_user.id)).all()
    return [health_monitor.get_health_report(db, str(acc.id)) for acc in accounts]

@app.post("/api/sending-accounts/{acc_id}/reactivate")
def reactivate_account(acc_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Manually reactivate an auto-paused account."""
    acc = db.query(database.SendingAccount).filter(database.SendingAccount.id == acc_id, database.SendingAccount.user_id == str(current_user.id)).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    result = health_monitor.reactivate_account(db, acc_id)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["detail"])
    return result

@app.get("/api/account-stats/{acc_id}")
def get_account_stats(acc_id: str, days: int = 30, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Get per-account daily stats for analytics charts."""
    acc = db.query(database.SendingAccount).filter(database.SendingAccount.id == acc_id, database.SendingAccount.user_id == str(current_user.id)).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    stats = health_monitor.get_account_stats(db, acc_id, days)
    return {"account_id": acc_id, "email": acc.email, "days": days, "stats": stats}

# --- Domain Health Endpoints ---
@app.get("/api/domain-health/{domain}")
def get_domain_health(domain: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Run a full domain health audit (SPF/DKIM/DMARC/Blacklist/Catch-all)."""
    result = domain_checker.full_domain_audit(domain)
    # Cache the result
    domain_checker.cache_domain_health(db, domain, result)
    return result

@app.get("/api/domain-health-all")
def get_all_domains_health(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Get cached domain health for all sending account domains."""
    accounts = db.query(database.SendingAccount).filter(database.SendingAccount.user_id == str(current_user.id)).all()
    domains = set()
    for acc in accounts:
        if '@' in acc.email:
            domains.add(acc.email.split('@')[1])

    results = []
    for domain in domains:
        cache = db.query(database.DomainHealthCache).filter(database.DomainHealthCache.domain == domain).first()
        if cache:
            results.append({
                "domain": domain,
                "has_spf": cache.has_spf,
                "has_dkim": cache.has_dkim,
                "has_dmarc": cache.has_dmarc,
                "is_blacklisted": cache.is_blacklisted,
                "blacklist_details": cache.blacklist_details,
                "is_catch_all": cache.is_catch_all,
                "last_checked": str(cache.last_checked) if cache.last_checked else None,
            })
        else:
            results.append({"domain": domain, "status": "not_checked"})
    return results

# --- Inbox Placement Test (Seed Testing) ---
class InboxTestRequest(BaseModel):
    seed_email: str
    seed_imap_server: Optional[str] = None
    seed_imap_port: int = 993
    seed_imap_password: Optional[str] = None

@app.post("/api/inbox-test/{acc_id}")
def run_inbox_test(acc_id: str, req: InboxTestRequest, background_tasks: BackgroundTasks, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Send a test email and check if it lands in inbox or spam."""
    acc = db.query(database.SendingAccount).filter(database.SendingAccount.id == acc_id, database.SendingAccount.user_id == str(current_user.id)).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    # Create seed test record
    test = database.SeedTestResult(
        account_id=acc_id,
        seed_email=req.seed_email,
        provider=req.seed_email.split('@')[-1] if '@' in req.seed_email else 'unknown',
        landed_in="pending"
    )
    db.add(test)
    db.commit()
    test_id = str(test.id)

    # Send test email in background
    def _run_seed_test():
        import time
        test_db = database.SessionLocal()
        try:
            # Send a test email
            subject = f"Inbox Test {datetime.utcnow().strftime('%H:%M')}"
            body = "<p>This is an automated inbox placement test. If you can read this, your email is landing in the inbox!</p>"
            sent = email_service.send_single_email(subject, body, req.seed_email, account=acc)

            if not sent:
                t = test_db.query(database.SeedTestResult).filter(database.SeedTestResult.id == test_id).first()
                if t:
                    t.landed_in = "send_failed"
                    test_db.commit()
                return

            # Wait for email to arrive
            time.sleep(120)  # 2 minutes

            # Check via IMAP if provided
            if req.seed_imap_server and req.seed_imap_password:
                import imaplib
                import email as email_module
                try:
                    imap = imaplib.IMAP4_SSL(req.seed_imap_server, req.seed_imap_port, timeout=15)
                    imap.login(req.seed_email, req.seed_imap_password)

                    # Check inbox first
                    imap.select('INBOX')
                    typ, data = imap.search(None, f'SUBJECT "{subject}"')
                    if typ == 'OK' and data[0]:
                        landed = "inbox"
                    else:
                        # Check spam
                        spam_folders = ['[Gmail]/Spam', 'Spam', 'Junk', 'Junk Email']
                        landed = "not_found"
                        for folder in spam_folders:
                            try:
                                imap.select(folder)
                                typ, data = imap.search(None, f'SUBJECT "{subject}"')
                                if typ == 'OK' and data[0]:
                                    landed = "spam"
                                    break
                            except Exception:
                                continue

                    imap.logout()

                    t = test_db.query(database.SeedTestResult).filter(database.SeedTestResult.id == test_id).first()
                    if t:
                        t.landed_in = landed
                        test_db.commit()
                except Exception as e:
                    print(f"[Inbox Test] IMAP check failed: {e}")
                    t = test_db.query(database.SeedTestResult).filter(database.SeedTestResult.id == test_id).first()
                    if t:
                        t.landed_in = "check_failed"
                        test_db.commit()
            else:
                # No IMAP credentials — mark as sent (user checks manually)
                t = test_db.query(database.SeedTestResult).filter(database.SeedTestResult.id == test_id).first()
                if t:
                    t.landed_in = "sent_check_manually"
                    test_db.commit()
        except Exception as e:
            print(f"[Inbox Test] Error: {e}")
        finally:
            test_db.close()

    import threading; threading.Thread(target=_run_seed_test, daemon=True).start()
    return {"status": "test_started", "test_id": test_id, "message": "Test email sent. Results will be available in ~2 minutes."}

@app.get("/api/inbox-test/{acc_id}/results")
def get_inbox_test_results(acc_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Get inbox placement test results for an account."""
    tests = db.query(database.SeedTestResult).filter(
        database.SeedTestResult.account_id == acc_id
    ).order_by(database.SeedTestResult.tested_at.desc()).limit(20).all()
    return [{
        "id": str(t.id),
        "seed_email": t.seed_email,
        "provider": t.provider,
        "landed_in": t.landed_in,
        "tested_at": str(t.tested_at) if t.tested_at else None
    } for t in tests]

# --- Sending Window Configuration ---
class SendWindowRequest(BaseModel):
    send_window_start: int = 9
    send_window_end: int = 17
    send_window_timezone: str = "UTC"

@app.post("/api/sending-accounts/{acc_id}/send-window")
def update_send_window(acc_id: str, req: SendWindowRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Update sending window for an account."""
    acc = db.query(database.SendingAccount).filter(database.SendingAccount.id == acc_id, database.SendingAccount.user_id == str(current_user.id)).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    acc.send_window_start = req.send_window_start
    acc.send_window_end = req.send_window_end
    acc.send_window_timezone = req.send_window_timezone
    db.commit()
    return {"status": "success"}

# --- Custom Tracking Domain ---
class TrackingDomainRequest(BaseModel):
    custom_tracking_domain: Optional[str] = None

@app.post("/api/sending-accounts/{acc_id}/tracking-domain")
def update_tracking_domain(acc_id: str, req: TrackingDomainRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Update custom tracking domain for an account."""
    acc = db.query(database.SendingAccount).filter(database.SendingAccount.id == acc_id, database.SendingAccount.user_id == str(current_user.id)).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    acc.custom_tracking_domain = req.custom_tracking_domain
    db.commit()
    return {"status": "success"}

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
@app.get('/api/run-campaign-debug/{campaign_id}')
def debug_campaign(campaign_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    try:
        _run_campaign(db, campaign_id)
        leads = db.query(database.CampaignLead).filter_by(campaign_id=campaign_id).all()
        return {"status": "done", "leads": [{"email": l.email, "status": l.status} for l in leads]}
    except Exception as e:
        import traceback
        return {"error": str(e), "trace": traceback.format_exc()}

@app.get('/api/reset-lead/{campaign_id}')
def reset_lead(campaign_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    leads = db.query(database.CampaignLead).filter_by(campaign_id=campaign_id).all()
    for l in leads: l.status = 'pending'
    db.commit()
    return {"status": "reset"}

class ReplySendRequest(BaseModel):
    content: str

@app.post("/api/replies/{reply_id}/draft")
def draft_reply(reply_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    reply = db.query(database.Reply).join(database.SendingAccount).filter(
        database.Reply.id == reply_id, 
        database.SendingAccount.user_id == current_user.id
    ).first()
    
    if not reply:
        raise HTTPException(status_code=404, detail="Reply not found or unauthorized")
        
    import ai_core
    draft = ai_core.draft_reply_to_email(reply.body or "", current_user.groq_api_key)
    return {"draft": draft}

@app.post("/api/replies/{reply_id}/send")
def send_ai_reply(reply_id: str, req: ReplySendRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    reply = db.query(database.Reply).join(database.SendingAccount).filter(
        database.Reply.id == reply_id, 
        database.SendingAccount.user_id == current_user.id
    ).first()
    
    if not reply:
        raise HTTPException(status_code=404, detail="Reply not found or unauthorized")
        
    account = db.query(database.SendingAccount).filter(database.SendingAccount.id == reply.account_id).first()
    
    import email_service
    success = email_service.send_single_email(
        subject="Re: " + (reply.subject or "Your Message"),
        body_html=f"<p>{req.content.replace(chr(10), '<br>')}</p>",
        recipient=reply.sender_email,
        account=account
    )
    
    if success:
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email. Check account settings.")

@app.get('/api/replies')
def get_replies(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    replies = db.query(database.Reply).join(database.SendingAccount).filter(
        database.SendingAccount.user_id == current_user.id
    ).order_by(database.Reply.received_at.desc()).all()
    
    return [{
        "id": str(r.id),
        "account_id": r.account_id,
        "sender_email": r.sender_email,
        "subject": r.subject,
        "body": r.body,
        "sentiment": r.sentiment,
        "received_at": str(r.received_at)
    } for r in replies]

@app.delete('/api/replies/{reply_id}')
def delete_reply(reply_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    reply = db.query(database.Reply).join(database.SendingAccount).filter(
        database.Reply.id == reply_id, 
        database.SendingAccount.user_id == current_user.id
    ).first()
    
    if not reply:
        raise HTTPException(status_code=404, detail="Reply not found or unauthorized")
        
    db.delete(reply)
    db.commit()
    return {"status": "ok", "message": "Reply deleted successfully"}


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

# ============================================================
# MEDIA GALLERY ENDPOINTS
# ============================================================
import uuid
from fastapi import UploadFile, File

@app.post("/api/gallery/upload")
async def upload_image(file: UploadFile = File(...), current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    ext = file.filename.split('.')[-1] if '.' in file.filename else 'png'
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", new_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    url = f"/uploads/{new_filename}"
    
    media = database.Media(
        user_id=str(current_user.id),
        filename=new_filename,
        original_name=file.filename,
        url=url
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    
    return {"status": "success", "media": {"id": media.id, "url": media.url, "name": media.original_name}}

@app.get("/api/gallery")
def get_gallery(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    media_files = db.query(database.Media).filter(database.Media.user_id == str(current_user.id)).order_by(database.Media.created_at.desc()).all()
    return [{"id": m.id, "url": m.url, "name": m.original_name, "created_at": m.created_at} for m in media_files]

@app.delete("/api/gallery/{media_id}")
def delete_media(media_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    media = db.query(database.Media).filter(database.Media.id == media_id, database.Media.user_id == str(current_user.id)).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
        
    file_path = os.path.join("uploads", media.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.delete(media)
    db.commit()
    return {"status": "success"}

@app.get("/api/dump-replies")
def dump_replies(db: Session = Depends(database.get_db)):
    try:
        with open("error.log", "r") as f:
            log = f.read()[-5000:]
    except:
        log = "no log"
    return {"log": log}

@app.get("/api/recalculate-stats")
def recalculate_stats(db: Session = Depends(database.get_db)):
    campaigns = db.query(database.Campaign).all()
    for c in campaigns:
        leads = db.query(database.CampaignLead).filter(database.CampaignLead.campaign_id == str(c.id)).all()
        sent = 0
        opens = 0
        clicks = 0
        for l in leads:
            if l.status in ['sent', 'opened', 'clicked', 'replied']:
                sent += 1
            if l.status in ['opened', 'clicked', 'replied']:
                opens += 1
            if l.status == 'clicked':
                clicks += 1
        c.sent_count = sent
        c.opens = opens
        c.clicks = clicks
    db.commit()
    return {"status": "ok"}

@app.get("/api/debug-imap")
def debug_imap(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    import sys, io
    import bounce_processor
    
    out = io.StringIO()
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = out
    sys.stderr = out
    
    try:
        bounce_processor.check_bounces()
    except Exception as e:
        print(f"CRASH: {str(e)}")
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        
    return {"debug_logs": out.getvalue().split('\n')}


# ============================================================
# CATCH-ALL: Serve Frontend (MUST be LAST route)
# ============================================================
@app.get("/{full_path:path}")
def serve_frontend(full_path: str, db: Session = Depends(database.get_db)):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API route not found")
    # Read file fresh every time - bypasses any server-side caching
    index_path = os.path.join(frontend_path, "index.html")
    try:
        if not os.path.exists(index_path):
            raise FileNotFoundError()
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
    except (FileNotFoundError, OSError):
        return Response(
            content="<html><body><h2>Frontend Not Found</h2><p>Please check the static files directory.</p></body></html>",
            media_type="text/html",
            status_code=404
        )
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


