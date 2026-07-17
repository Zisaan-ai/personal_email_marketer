from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, JSON, Enum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    mailboxes = relationship("Mailbox", back_populates="user")
    workflows = relationship("VisualWorkflow", back_populates="user")

class Domain(Base):
    __tablename__ = 'domains'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Mailbox(Base):
    __tablename__ = 'mailboxes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    domain_id = Column(UUID(as_uuid=True), ForeignKey('domains.id'))
    email_address = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    overall_health = Column(Float, default=100.0)
    consistency_score = Column(Float, default=100.0)
    trust_score = Column(Float, default=50.0)
    risk_score = Column(Float, default=0.0)
    
    user = relationship("User", back_populates="mailboxes")
    reputations = relationship("ProviderReputation", back_populates="mailbox")

class ProviderReputation(Base):
    __tablename__ = 'provider_reputations'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mailbox_id = Column(UUID(as_uuid=True), ForeignKey('mailboxes.id'), index=True)
    provider_name = Column(String) # e.g., 'Gmail', 'Outlook', 'Yahoo'
    
    reputation_score = Column(Float, default=100.0)
    daily_limit = Column(Integer, default=50)
    warmup_percent = Column(Float, default=100.0)
    campaign_percent = Column(Float, default=0.0)
    
    mailbox = relationship("Mailbox", back_populates="reputations")

class VisualWorkflow(Base):
    __tablename__ = 'visual_workflows'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    name = Column(String)
    status = Column(String, default="draft")
    dag_json = Column(JSON) # Directed Acyclic Graph storing nodes and edges
    
    user = relationship("User", back_populates="workflows")

class VisualTemplate(Base):
    __tablename__ = 'visual_templates'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    name = Column(String)
    structure_json = Column(JSON) # JSON block structure (MJML/GrapesJS)
    compiled_html = Column(String) # The finalized HTML
