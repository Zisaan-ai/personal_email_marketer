import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, String, Boolean, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.pool import StaticPool

load_dotenv()

# Use absolute path for SQLite so it works on both local and cPanel
_DB_DIR = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_DB = f"sqlite:///{os.path.join(_DB_DIR, 'sql_app.db')}"
DATABASE_URL = os.getenv("DATABASE_URL", _DEFAULT_DB)

from sqlalchemy.pool import NullPool

# For sqlite we need connect_args={"check_same_thread": False}
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={
            "check_same_thread": False,
            "timeout": 15
        }, 
        poolclass=NullPool
    )
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            conn.execute(text("PRAGMA journal_mode=WAL;"))
            conn.execute(text("PRAGMA synchronous=NORMAL;"))
    except Exception as e:
        print(f"Failed to enable WAL: {e}")
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)
    is_email_verified = Column(Boolean, default=False)
    gemini_api_key = Column(String, nullable=True)
    groq_api_key = Column(String, nullable=True)
    openai_api_key = Column(String, nullable=True)
    anthropic_api_key = Column(String, nullable=True)
    deepseek_api_key = Column(String, nullable=True)

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(String, primary_key=True, default=generate_uuid)
    subject = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    type = Column(String, default="newsletter")
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    steps_json = Column(Text, nullable=True)
    
    max_emails_per_day = Column(Integer, default=50)
    daily_ramp_up = Column(Integer, default=0)
    current_daily_limit = Column(Integer, default=50)
    sent_today_campaign = Column(Integer, default=0)
    sent_today_date = Column(String, nullable=True)
    
    sent_count = Column(Integer, default=0)
    opens = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    
    is_ab_test = Column(Boolean, default=False)
    subject_b = Column(String, nullable=True)
    body_b = Column(Text, nullable=True)
    sent_count_a = Column(Integer, default=0)
    sent_count_b = Column(Integer, default=0)
    opens_a = Column(Integer, default=0)
    opens_b = Column(Integer, default=0)
    
    status = Column(String, default="draft")
    paused_reason = Column(String, nullable=True)
    scheduled_at = Column(DateTime, nullable=True)
    timezone = Column(String, nullable=True)
    delay_min = Column(Integer, default=30)
    delay_max = Column(Integer, default=90)
    # Sending schedule (per-campaign)
    sending_days = Column(String, nullable=True)  # JSON list e.g. ["Mon","Tue","Wed"]
    start_hour = Column(Integer, nullable=True)   # e.g. 9 (9 AM)
    end_hour = Column(Integer, nullable=True)      # e.g. 17 (5 PM)
    
    # --- Deliverability Options ---
    track_opens = Column(Boolean, default=True)
    track_clicks = Column(Boolean, default=True)
    use_unsubscribe = Column(Boolean, default=True)

    # --- Manual Sending Account Selection ---
    selected_sender_ids = Column(Text, nullable=True) # JSON list of account IDs, or null for all active

    created_at = Column(DateTime, default=datetime.utcnow)

class CampaignLead(Base):
    __tablename__ = "campaign_leads"

    id = Column(String, primary_key=True, default=generate_uuid)
    campaign_id = Column(String, ForeignKey("campaigns.id"), index=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=True)
    company = Column(String, nullable=True)
    status = Column(String, default="pending")
    variant = Column(String, nullable=True)
    sending_account_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    current_step = Column(Integer, default=0)
    next_send_at = Column(DateTime, nullable=True)
    replied = Column(Boolean, default=False)

class BounceRecord(Base):
    __tablename__ = "bounce_records"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String(36), index=True)
    email = Column(String(150), index=True)
    bounce_type = Column(String(50)) # 'hard' or 'soft'
    bounce_reason = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class Media(Base):
    __tablename__ = "media_gallery"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    filename = Column(String(255))
    original_name = Column(String(255))
    url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

class TrackingLog(Base):
    __tablename__ = "tracking_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    campaign_id = Column(String, index=True)
    contact_id = Column(String, index=True)
    event_type = Column(String, nullable=False)
    url = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SendingAccount(Base):
    __tablename__ = "sending_accounts"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    smtp_server = Column(String, nullable=False)
    smtp_port = Column(Integer, default=587)
    smtp_username = Column(String, nullable=False)
    smtp_password = Column(String, nullable=False)
    daily_limit = Column(Integer, default=500)
    sent_today = Column(Integer, default=0)
    sent_today_date = Column(String, nullable=True)  # "2026-07-13" (Bangladesh date)
    imap_server = Column(String, nullable=True)
    imap_port = Column(Integer, default=993)
    imap_password = Column(String, nullable=True)
    health_score = Column(Integer, default=100)
    warmup_enabled = Column(Boolean, default=False)
    warmup_daily_limit = Column(Integer, default=5)
    warmup_increment_per_day = Column(Integer, default=2)
    warmup_sent_today = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    smart_limit_enabled = Column(Boolean, default=False)
    smart_warmup_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # --- Health Tracking (Smart Deliverability) ---
    total_sent = Column(Integer, default=0)
    total_bounced = Column(Integer, default=0)
    total_opened = Column(Integer, default=0)
    total_replied = Column(Integer, default=0)
    bounce_streak = Column(Integer, default=0)
    last_health_check = Column(DateTime, nullable=True)
    auto_paused = Column(Boolean, default=False)
    auto_paused_reason = Column(String, nullable=True)

    # --- Sending Window (disabled by default - 0 to 24 = send 24/7) ---
    send_window_start = Column(Integer, default=0)    # 12 AM (no restriction)
    send_window_end = Column(Integer, default=24)      # 12 AM next day (no restriction)
    send_window_timezone = Column(String, default="UTC")

    # --- Custom Tracking ---
    custom_tracking_domain = Column(String, nullable=True)

class Reply(Base):
    __tablename__ = "replies"

    id = Column(String, primary_key=True, default=generate_uuid)
    account_id = Column(String, ForeignKey("sending_accounts.id"))
    message_id = Column(String, nullable=True, unique=True)
    sender_email = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    sentiment = Column(String, default="Unknown")
    received_at = Column(DateTime, default=datetime.utcnow)

class UnsubscribeList(Base):
    __tablename__ = "unsubscribes"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    unsubscribed_at = Column(DateTime, default=datetime.utcnow)

class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    url = Column(String, nullable=False)
    events = Column(String, default="all")

# --- Seed Test Results (Inbox Placement Testing) ---
class SeedTestResult(Base):
    __tablename__ = "seed_test_results"

    id = Column(String, primary_key=True, default=generate_uuid)
    account_id = Column(String, ForeignKey("sending_accounts.id"), index=True)
    seed_email = Column(String, nullable=False)
    provider = Column(String, nullable=True)       # gmail, outlook, yahoo
    landed_in = Column(String, default="pending")  # inbox, spam, not_found, pending
    tested_at = Column(DateTime, default=datetime.utcnow)

# --- Domain Health Cache (SPF/DKIM/DMARC/Blacklist) ---
class DomainHealthCache(Base):
    __tablename__ = "domain_health_cache"

    id = Column(String, primary_key=True, default=generate_uuid)
    domain = Column(String, unique=True, index=True, nullable=False)
    has_spf = Column(Boolean, default=False)
    has_dkim = Column(Boolean, default=False)
    has_dmarc = Column(Boolean, default=False)
    spf_record = Column(String, nullable=True)
    dmarc_record = Column(String, nullable=True)
    is_blacklisted = Column(Boolean, default=False)
    blacklist_details = Column(String, nullable=True)
    is_catch_all = Column(Boolean, default=False)
    last_checked = Column(DateTime, default=datetime.utcnow)

# --- Per-Account Daily Stats (Analytics) ---
class AccountDailyStats(Base):
    __tablename__ = "account_daily_stats"

    id = Column(String, primary_key=True, default=generate_uuid)
    account_id = Column(String, ForeignKey("sending_accounts.id"), index=True)
    date = Column(String, index=True)   # "2026-07-11"
    sent = Column(Integer, default=0)
    bounced = Column(Integer, default=0)
    opened = Column(Integer, default=0)
    clicked = Column(Integer, default=0)
    replied = Column(Integer, default=0)

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

class InactiveLeadList(Base):
    __tablename__ = "inactive_leads"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    tagged_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# --- Safe Migration for existing SQLite databases ---
def _safe_add_column(table_name: str, column_name: str, column_type: str, default=None):
    """Add a column to an existing table if it doesn't exist (SQLite safe)."""
    from sqlalchemy import text, inspect
    insp = inspect(engine)
    existing_cols = [c['name'] for c in insp.get_columns(table_name)]
    if column_name not in existing_cols:
        default_clause = ""
        if default is not None:
            if isinstance(default, str):
                default_clause = f" DEFAULT '{default}'"
            elif isinstance(default, bool):
                default_clause = f" DEFAULT {1 if default else 0}"
            else:
                default_clause = f" DEFAULT {default}"
        with engine.begin() as conn:
            conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}{default_clause}"))
        print(f"[Migration] Added column {table_name}.{column_name}")

def run_migrations():
    """Run safe migrations for new columns on existing tables."""
    try:
        _safe_add_column("users", "openai_api_key", "VARCHAR", None)
        _safe_add_column("users", "anthropic_api_key", "VARCHAR", None)
        _safe_add_column("users", "deepseek_api_key", "VARCHAR", None)
        
        _safe_add_column("sending_accounts", "total_sent", "INTEGER", 0)
        _safe_add_column("sending_accounts", "total_bounced", "INTEGER", 0)
        _safe_add_column("sending_accounts", "total_opened", "INTEGER", 0)
        _safe_add_column("sending_accounts", "total_replied", "INTEGER", 0)
        _safe_add_column("sending_accounts", "warmup_daily_limit", "INTEGER", 20)
        _safe_add_column("sending_accounts", "smart_limit_enabled", "BOOLEAN", False)
        _safe_add_column("sending_accounts", "smart_warmup_enabled", "BOOLEAN", False)
        _safe_add_column("sending_accounts", "bounce_streak", "INTEGER", 0)
        _safe_add_column("sending_accounts", "last_health_check", "DATETIME", None)
        _safe_add_column("sending_accounts", "auto_paused", "BOOLEAN", False)
        _safe_add_column("sending_accounts", "auto_paused_reason", "VARCHAR", None)
        _safe_add_column("sending_accounts", "send_window_start", "INTEGER", 0)
        _safe_add_column("sending_accounts", "send_window_end", "INTEGER", 24)
        _safe_add_column("sending_accounts", "send_window_timezone", "VARCHAR", "UTC")
        _safe_add_column("sending_accounts", "custom_tracking_domain", "VARCHAR", None)
        _safe_add_column("replies", "message_id", "VARCHAR", None)
        _safe_add_column("sending_accounts", "sent_today_date", "VARCHAR", None)
        _safe_add_column("campaign_leads", "sending_account_id", "VARCHAR", None)
        
        # --- Campaign Deliverability Options ---
        _safe_add_column("campaigns", "track_opens", "BOOLEAN", True)
        _safe_add_column("campaigns", "track_clicks", "BOOLEAN", True)
        _safe_add_column("campaigns", "use_unsubscribe", "BOOLEAN", True)
        _safe_add_column("campaigns", "steps_json", "TEXT", None)
        _safe_add_column("campaigns", "max_emails_per_day", "INTEGER", 50)
        _safe_add_column("campaigns", "daily_ramp_up", "INTEGER", 0)
        _safe_add_column("campaigns", "current_daily_limit", "INTEGER", 50)
        _safe_add_column("campaigns", "sent_today_campaign", "INTEGER", 0)
        _safe_add_column("campaigns", "sent_today_date", "VARCHAR(50)", None)
        _safe_add_column("campaigns", "paused_reason", "VARCHAR(255)", None)
        _safe_add_column("campaigns", "sending_days", "VARCHAR", "Mon,Tue,Wed,Thu,Fri,Sat,Sun")
        _safe_add_column("campaigns", "start_hour", "INTEGER", 0)
        _safe_add_column("campaigns", "end_hour", "INTEGER", 24)
        _safe_add_column("campaigns", "timezone", "VARCHAR", "UTC")
        _safe_add_column("campaigns", "delay_min", "INTEGER", 2)
        _safe_add_column("campaigns", "delay_max", "INTEGER", 5)
        
        _safe_add_column("campaign_leads", "current_step", "INTEGER", 0)
        _safe_add_column("campaign_leads", "next_send_at", "DATETIME", None)
        _safe_add_column("campaign_leads", "replied", "BOOLEAN", False)

        print("[Migration] All migrations completed successfully.")
    except Exception as e:
        print(f"[Migration] Error: {e}")

run_migrations()

