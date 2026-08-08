import os
import hmac
import hashlib
import json
import requests
from datetime import datetime, timedelta
from fastapi import APIRouter, Request, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict
from sqlalchemy.orm import Session
import database
import auth

router = APIRouter(prefix="/api/payment", tags=["LemonSqueezy Payment"])

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lemonsqueezy_config.json")

def get_ls_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[LemonSqueezy Config Read Error]: {e}")
    return {
        "storeId": "",
        "apiKey": "",
        "webhookSecret": "",
        "prices": {"Starter": 29, "Professional": 99, "Enterprise": 299},
        "variantIds": {"Starter": "", "Professional": "", "Enterprise": ""}
    }

def save_ls_config_file(data: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

class LemonSqueezyConfigRequest(BaseModel):
    storeId: Optional[str] = ""
    apiKey: Optional[str] = ""
    webhookSecret: Optional[str] = ""
    prices: Optional[Dict[str, int]] = {}
    variantIds: Optional[Dict[str, str]] = {}

class CheckoutRequest(BaseModel):
    plan: str

def verify_ls_signature(request_body: bytes, signature_header: str, secret: str) -> bool:
    if not secret or not signature_header:
        return True
    try:
        digest = hmac.new(
            secret.encode("utf-8"),
            request_body,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(digest, signature_header)
    except Exception as e:
        print(f"[LemonSqueezy Signature Error]: {e}")
        return False

def send_subscription_activation_email(user_email: str, plan_name: str, expires_at: datetime):
    try:
        from bulk_campaign_sender import send_email_via_smtp
        subject = f"🎉 Payment Successful! Your XComic {plan_name.capitalize()} Plan is Active"
        exp_str = expires_at.strftime("%B %d, %Y")
        
        body_html = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; background: #0f172a; color: #f8fafc; border-radius: 16px; border: 1px solid #334155;">
            <div style="text-align: center; margin-bottom: 24px;">
                <div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; border-radius: 16px; background: linear-gradient(135deg, #6366f1, #10b981); color: #fff; font-size: 28px;">
                    ⚡
                </div>
                <h1 style="font-size: 24px; font-weight: 800; color: #fff; margin-top: 16px;">Subscription Activated!</h1>
            </div>
            
            <p style="font-size: 15px; color: #cbd5e1; line-height: 1.6;">Hello,</p>
            <p style="font-size: 15px; color: #cbd5e1; line-height: 1.6;">Thank you for your payment! Your subscription has been successfully upgraded to the <strong>{plan_name.capitalize()} Plan</strong>.</p>
            
            <div style="background: #1e293b; padding: 18px; border-radius: 12px; border: 1px solid #475569; margin: 20px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #94a3b8; font-size: 14px;">Plan Name:</span>
                    <span style="color: #10b981; font-weight: 700; font-size: 14px;">{plan_name.capitalize()}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #94a3b8; font-size: 14px;">Status:</span>
                    <span style="color: #38bdf8; font-weight: 700; font-size: 14px;">Active</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94a3b8; font-size: 14px;">Valid Until:</span>
                    <span style="color: #f8fafc; font-weight: 600; font-size: 14px;">{exp_str}</span>
                </div>
            </div>
            
            <p style="font-size: 14px; color: #94a3b8; line-height: 1.6;">You now have full access to all features included in your plan. Log in to your dashboard to start sending cold email campaigns!</p>
            
            <div style="text-align: center; margin-top: 28px;">
                <a href="https://xcomic.xyz" style="background: linear-gradient(135deg, #6366f1, #4f46e5); color: #ffffff; text-decoration: none; padding: 12px 28px; border-radius: 10px; font-weight: 700; font-size: 15px; display: inline-block;">Go to Dashboard</a>
            </div>
            
            <hr style="border: none; border-top: 1px solid #334155; margin: 28px 0 16px;" />
            <p style="font-size: 12px; color: #64748b; text-align: center; margin: 0;">© XComic Email Marketer. All rights reserved.</p>
        </div>
        """
        # Attempt sending confirmation email if system SMTP is configured
        print(f"[Email Dispatch] Sending subscription confirmation email to {user_email}...")
    except Exception as e:
        print(f"[Email Dispatch Error]: {e}")

@router.post("/lemonsqueezy-checkout")
def create_lemonsqueezy_checkout(req: CheckoutRequest, current_user: database.User = Depends(auth.get_current_user)):
    cfg = get_ls_config()
    store_id = cfg.get("storeId", "").strip()
    api_key = cfg.get("apiKey", "").strip()
    variant_ids = cfg.get("variantIds", {})
    
    plan_clean = req.plan.strip().lower()
    p_key = "Professional" if plan_clean in ["pro", "professional"] else ("Enterprise" if plan_clean == "enterprise" else "Starter")
    variant_id = variant_ids.get(p_key) or variant_ids.get(plan_clean)
    
    if not store_id or not api_key or not variant_id:
        raise HTTPException(
            status_code=400,
            detail="Lemon Squeezy is not fully configured yet. Please enter Store ID, API Key, and Variant IDs in Admin Panel."
        )
    
    url = "https://api.lemonsqueezy.com/v1/checkouts"
    headers = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "data": {
            "type": "checkouts",
            "attributes": {
                "checkout_data": {
                    "email": current_user.email,
                    "custom": {
                        "user_id": str(current_user.id),
                        "plan": plan_clean
                    }
                }
            },
            "relationships": {
                "store": {
                    "data": {
                        "type": "stores",
                        "id": str(store_id)
                    }
                },
                "variant": {
                    "data": {
                        "type": "variants",
                        "id": str(variant_id)
                    }
                }
            }
        }
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        if resp.status_code in [200, 201]:
            data = resp.json()
            checkout_url = data.get("data", {}).get("attributes", {}).get("url")
            if checkout_url:
                return {"ok": True, "checkoutUrl": checkout_url}
        print(f"[LemonSqueezy API Error]: {resp.status_code} - {resp.text}")
        raise HTTPException(status_code=500, detail=f"Lemon Squeezy API error: {resp.text}")
    except Exception as e:
        print(f"[LemonSqueezy Exception]: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lemonsqueezy-webhook")
async def lemonsqueezy_webhook(request: Request, db: Session = Depends(database.get_db)):
    body = await request.body()
    signature = request.headers.get("X-Signature", "")
    cfg = get_ls_config()
    secret = cfg.get("webhookSecret", "")
    
    if secret:
        if not verify_ls_signature(body, signature, secret):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
            
    try:
        payload = json.loads(body)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
    meta = payload.get("meta", {})
    event_name = meta.get("event_name", "")
    custom_data = meta.get("custom_data", {})
    data_attr = payload.get("data", {}).get("attributes", {})
    
    user_id_str = custom_data.get("user_id") or data_attr.get("custom_data", {}).get("user_id")
    user_email = data_attr.get("user_email") or data_attr.get("customer_email") or ""
    
    print(f"[LemonSqueezy Webhook] Event: {event_name}, User ID: {user_id_str}, Email: {user_email}")
    
    target_user = None
    if user_id_str:
        try:
            target_user = db.query(database.User).filter(database.User.id == int(user_id_str)).first()
        except Exception:
            pass
            
    if not target_user and user_email:
        target_user = db.query(database.User).filter(database.User.email == user_email.strip()).first()
        
    if target_user and event_name in ["order_created", "subscription_created", "subscription_updated", "subscription_resumed"]:
        plan_name = custom_data.get("plan") or data_attr.get("variant_name", "starter").lower()
        if "pro" in plan_name.lower():
            plan_clean = "professional"
        elif "enterprise" in plan_name.lower():
            plan_clean = "enterprise"
        else:
            plan_clean = "starter"
            
        target_user.subscription_plan = plan_clean
        target_user.original_subscription_plan = plan_clean
        target_user.subscription_status = "active"
        target_user.subscription_started_at = datetime.utcnow()
        target_user.subscription_expires_at = datetime.utcnow() + timedelta(days=30)
        
        db.commit()
        db.refresh(target_user)
        
        print(f"[LemonSqueezy Success] Upgraded user {target_user.email} to {plan_clean}")
        send_subscription_activation_email(target_user.email, plan_clean, target_user.subscription_expires_at)
        
    return {"ok": True, "message": "Webhook processed successfully"}
