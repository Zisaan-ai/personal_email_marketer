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

# For sqlite we need connect_args={"check_same_thread": False}
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
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

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(String, primary_key=True, default=generate_uuid)
    subject = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    type = Column(String, default="newsletter")
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    
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
    
    status = Column(String, default="sent")
    scheduled_at = Column(DateTime, nullable=True)
    timezone = Column(String, nullable=True)
    delay_min = Column(Integer, default=30)
    delay_max = Column(Integer, default=90)
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
    imap_server = Column(String, nullable=True)
    imap_port = Column(Integer, default=993)
    imap_password = Column(String, nullable=True)
    health_score = Column(Integer, default=100)
    warmup_enabled = Column(Boolean, default=False)
    warmup_daily_limit = Column(Integer, default=5)
    warmup_increment_per_day = Column(Integer, default=2)
    warmup_sent_today = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Reply(Base):
    __tablename__ = "replies"

    id = Column(String, primary_key=True, default=generate_uuid)
    account_id = Column(String, ForeignKey("sending_accounts.id"))
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

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class InactiveLeadList(Base):
    __tablename__ = "inactive_leads"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    tagged_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

