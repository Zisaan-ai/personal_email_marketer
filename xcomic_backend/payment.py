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

    # Process subscription events
    if event_type in ["subscription.created", "subscription.updated", "subscription.activated"]:
        custom_data = data.get("custom_data", {})
        user_id = custom_data.get("user_id")
        
        if user_id:
            user = db.query(database.User).filter(database.User.id == user_id).first()
            if user:
                user.subscription_status = data.get("status", "active")
                user.paddle_subscription_id = data.get("id")
                user.paddle_customer_id = data.get("customer_id")
                
                # Update plan based on price or product id
                items = data.get("items", [])
                if items and len(items) > 0:
                    price_id = items[0].get("price", {}).get("id")
                    if price_id:
                        user.subscription_plan = price_id # Map this to human-readable names
                
                db.commit()
                print(f"[Paddle Webhook] Updated subscription for user {user_id}")
                
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
    """Get the current user's subscription status."""
    return {
        "plan": user.subscription_plan,
        "status": user.subscription_status
    }
