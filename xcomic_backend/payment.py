import os
import hmac
import hashlib
import json
from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database
import auth

router = APIRouter(prefix="/api/payment", tags=["Payment"])

# Paddle Webhook Secret (from environment)
PADDLE_WEBHOOK_SECRET = os.getenv("PADDLE_WEBHOOK_SECRET", "")

def verify_paddle_signature(request: Request, body: bytes):
    signature_header = request.headers.get("Paddle-Signature")
    if not signature_header or not PADDLE_WEBHOOK_SECRET:
        return True # For local testing or if secret is not set
    
    try:
        parts = dict(part.split('=') for part in signature_header.split(';'))
        ts = parts.get('ts')
        h1 = parts.get('h1')
        
        if not ts or not h1:
            return False
            
        payload = f"{ts}:{body.decode('utf-8')}"
        computed_hash = hmac.new(
            PADDLE_WEBHOOK_SECRET.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(computed_hash, h1)
    except Exception as e:
        return False


@router.post("/webhook")
async def paddle_webhook(request: Request, db: Session = Depends(database.get_db)):
    body = await request.body()
    
    if PADDLE_WEBHOOK_SECRET:
        is_valid = verify_paddle_signature(request, body)
        if not is_valid:
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
            
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    event_type = payload.get("event_type")
    data = payload.get("data", {})
    
    print(f"[Paddle Webhook] Received event: {event_type}")

    # Process subscription & transaction events
    if event_type in ["subscription.created", "subscription.updated", "subscription.activated", "transaction.completed", "checkout.completed"]:
        custom_data = data.get("custom_data", {})
        user_id = custom_data.get("user_id")
        plan_from_custom = custom_data.get("plan", "").lower()
        
        if user_id:
            user = db.query(database.User).filter(database.User.id == user_id).first()
            if user:
                user.subscription_status = data.get("status", "active")
                if data.get("id"):
                    user.paddle_subscription_id = data.get("id")
                if data.get("customer_id"):
                    user.paddle_customer_id = data.get("customer_id")
                
                # Determine plan name from custom_data or items price_id
                target_plan = plan_from_custom
                if not target_plan:
                    items = data.get("items", [])
                    if items and len(items) > 0:
                        price_id = items[0].get("price", {}).get("id") or items[0].get("price_id", "")
                        # Map default price IDs if match
                        if "fz3n7mq" in price_id or "enterprise" in price_id.lower():
                            target_plan = "enterprise"
                        elif "fxmmpdp" in price_id or "pro" in price_id.lower():
                            target_plan = "professional"
                        elif "fwdrmsw" in price_id or "starter" in price_id.lower():
                            target_plan = "starter"
                        else:
                            target_plan = price_id
                
                if target_plan:
                    user.subscription_plan = target_plan
                    user.original_subscription_plan = target_plan
                
                from datetime import datetime, timedelta
                if not getattr(user, 'subscription_started_at', None):
                    user.subscription_started_at = datetime.utcnow()
                user.subscription_expires_at = datetime.utcnow() + timedelta(days=30)
                
                db.commit()
                print(f"[Paddle Webhook] Updated subscription for user {user_id} -> {user.subscription_plan}")
                
    elif event_type in ["subscription.canceled", "subscription.past_due"]:
        custom_data = data.get("custom_data", {})
        user_id = custom_data.get("user_id")
        
        if user_id:
            user = db.query(database.User).filter(database.User.id == user_id).first()
            if user:
                user.subscription_status = data.get("status", "canceled")
                user.subscription_plan = "free"
                db.commit()
                print(f"[Paddle Webhook] Canceled subscription for user {user_id}")

    return {"status": "success"}

@router.get("/status")
def payment_status(user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Get the current user's subscription status, expiration, and custom overrides."""
    started_at = getattr(user, 'subscription_started_at', None)
    expires_at = getattr(user, 'subscription_expires_at', None)
    plan_clean = (getattr(user, 'subscription_plan', 'free') or "free").lower()
    
    from datetime import datetime, timedelta
    if plan_clean != "free" and not expires_at:
        started_at = started_at or datetime.utcnow()
        expires_at = datetime.utcnow() + timedelta(days=30)
        try:
            user.subscription_started_at = started_at
            user.subscription_expires_at = expires_at
            db.commit()
        except Exception:
            db.rollback()

    days_remaining = None
    if expires_at:
        try:
            diff = (expires_at - datetime.utcnow()).days
            days_remaining = max(0, diff) if diff >= 0 else 0
        except Exception:
            pass

    orig_plan = getattr(user, 'original_subscription_plan', None) or 'free'

    return {
        "plan": getattr(user, 'subscription_plan', 'free') or 'free',
        "original_plan": orig_plan,
        "status": getattr(user, 'subscription_status', 'active') or 'active',
        "started_at": started_at.isoformat() if (started_at and hasattr(started_at, 'isoformat')) else None,
        "expires_at": expires_at.isoformat() if (expires_at and hasattr(expires_at, 'isoformat')) else None,
        "days_remaining": days_remaining,
        "custom_daily_limit": getattr(user, 'custom_daily_limit', None),
        "custom_max_accounts": getattr(user, 'custom_max_accounts', None),
        "custom_ai_replies": getattr(user, 'custom_ai_replies', None),
    }
