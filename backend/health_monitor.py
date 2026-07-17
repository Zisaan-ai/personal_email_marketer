"""
Email Health Intelligence Engine
================================
Monitors and manages the health of sending accounts to maximize inbox delivery rate.

Features:
- Real-time health score calculation after each send
- Auto-pause accounts with poor health
- Smart daily limit suggestions based on account age & health
- Per-account daily stats tracking
- Periodic health audits
"""

from datetime import datetime, timedelta
import database


# ============================================================
# HEALTH SCORE CALCULATION
# ============================================================
def calculate_health_score(account) -> int:
    """
    Calculate health score (0-100) based on account metrics.
    
    Formula:
    - Start at 100
    - Subtract bounce rate penalty (up to 80 points)
    - Subtract bounce streak penalty (up to 30 points)
    - Add open rate bonus (up to 15 points)
    - Add reply rate bonus (up to 10 points)
    """
    total_sent = account.total_sent or 0
    total_bounced = account.total_bounced or 0
    total_opened = account.total_opened or 0
    total_replied = account.total_replied or 0
    bounce_streak = account.bounce_streak or 0

    if total_sent == 0:
        return 0  # New account, no data yet

    # Base score grows with total_sent up to 100 (reaches 100 after 100 emails)
    base_score = min(100, total_sent)

    # Bounce rate penalty (heaviest weight - up to 80 points)
    bounce_rate = total_bounced / total_sent
    bounce_penalty = bounce_rate * 80

    # Consecutive bounce streak penalty (up to 30 points)
    streak_penalty = min(bounce_streak * 5, 30)

    # Open rate bonus (up to 15 points)
    open_rate = total_opened / total_sent
    open_bonus = min(open_rate * 20, 15)

    # Reply rate bonus (up to 10 points)
    reply_rate = total_replied / total_sent
    reply_bonus = min(reply_rate * 40, 10)

    # Calculate final score
    score = base_score - bounce_penalty - streak_penalty + open_bonus + reply_bonus
    return max(0, min(100, int(score)))

def calculate_provider_reputation(db, account_id: str, provider_name: str) -> dict:
    """
    Calculates the provider-specific reputation score based on strict penalties.
    Updates the ProviderReputation table.
    """
    stats = db.query(database.AccountDailyStats).filter(
        database.AccountDailyStats.account_id == account_id,
        database.AccountDailyStats.provider_name == provider_name
    ).all()
    
    total_sent = sum(s.sent for s in stats)
    if total_sent < 10:
        return None # Not enough data
        
    total_bounced = sum(s.bounced for s in stats)
    total_complaints = 0 # Future proofing
    total_replied = sum(s.replied for s in stats)
    
    bounce_rate = total_bounced / total_sent
    complaint_rate = total_complaints / total_sent
    reply_rate = total_replied / total_sent
    
    base = 100.0
    penalty_bounce = (bounce_rate / 0.5) * 5.0
    penalty_complaint = (complaint_rate / 0.1) * 10.0
    bonus_reply = min((reply_rate / 1.0) * 2.0, 15.0)
    
    reputation = base - penalty_bounce - penalty_complaint + bonus_reply
    reputation = max(0.0, min(100.0, reputation))
    
    # Strategy
    if reputation >= 85:
        warmup_pct, camp_pct = 30, 70
    elif reputation >= 70:
        warmup_pct, camp_pct = 50, 50
    else:
        warmup_pct, camp_pct = 80, 20
        
    rep_record = db.query(database.ProviderReputation).filter(
        database.ProviderReputation.account_id == account_id,
        database.ProviderReputation.provider_name == provider_name
    ).first()
    
    if not rep_record:
        rep_record = database.ProviderReputation(
            account_id=account_id,
            provider_name=provider_name
        )
        db.add(rep_record)
        
    rep_record.reputation_score = int(reputation)
    rep_record.warmup_percent = warmup_pct
    rep_record.campaign_percent = camp_pct
    rep_record.updated_at = datetime.utcnow()
    db.commit()
    
    return {"reputation": int(reputation), "warmup_percent": warmup_pct}


# ============================================================
# HEALTH UPDATE FUNCTIONS
# ============================================================
def update_health_after_send(db, account_id: str, success: bool):
    """Called after each email send attempt to update health metrics."""
    account = db.query(database.SendingAccount).filter(
        database.SendingAccount.id == account_id
    ).first()
    if not account:
        return

    account.total_sent = (account.total_sent or 0) + 1

    if success:
        account.bounce_streak = 0
    else:
        account.total_bounced = (account.total_bounced or 0) + 1
        account.bounce_streak = (account.bounce_streak or 0) + 1

    # Recalculate health score
    account.health_score = calculate_health_score(account)
    account.last_health_check = datetime.utcnow()
    db.flush()

    # Record daily stats
    _record_daily_stat(db, account_id, "sent" if success else "bounced")

    # Check if we need to auto-pause
    if not success:
        check_auto_pause(db, account)


def update_health_after_open(db, account_id: str):
    """Called when an email open is tracked."""
    account = db.query(database.SendingAccount).filter(
        database.SendingAccount.id == account_id
    ).first()
    if not account:
        return

    account.total_opened = (account.total_opened or 0) + 1
    account.health_score = calculate_health_score(account)
    db.flush()

    _record_daily_stat(db, account_id, "opened")


def update_health_after_reply(db, account_id: str):
    """Called when a reply is detected for an account."""
    account = db.query(database.SendingAccount).filter(
        database.SendingAccount.id == account_id
    ).first()
    if not account:
        return

    account.total_replied = (account.total_replied or 0) + 1
    account.health_score = calculate_health_score(account)
    db.flush()

    _record_daily_stat(db, account_id, "replied")


def update_health_after_click(db, account_id: str):
    """Called when a click is tracked."""
    _record_daily_stat(db, account_id, "clicked")


# ============================================================
# AUTO-PAUSE LOGIC
# ============================================================
def check_auto_pause(db, account) -> bool:
    """
    Check if an account should be auto-paused.
    Returns True if account was paused.
    
    Auto-pause triggers:
    1. Health score drops below 50
    2. 5 or more consecutive bounces
    """
    if account.auto_paused:
        return False  # Already paused

    reason = None

    # Only auto-pause for low health if the account has sent at least 50 emails
    # Since health grows from 0, early health is naturally low
    current_health = account.health_score if account.health_score is not None else 0
    if (account.total_sent or 0) >= 50 and current_health < 50:
        reason = f"Health score critically low ({current_health}/100)"

    elif (account.bounce_streak or 0) >= 5:
        reason = f"5+ consecutive bounces (streak: {account.bounce_streak})"

    if reason:
        account.auto_paused = True
        account.auto_paused_reason = reason
        account.is_active = False
        db.commit()
        print(f"[Health Monitor] ⚠️ Auto-paused account {account.email}: {reason}")
        return True

    return False


def reactivate_account(db, account_id: str) -> dict:
    """Manually reactivate an auto-paused account."""
    account = db.query(database.SendingAccount).filter(
        database.SendingAccount.id == account_id
    ).first()
    if not account:
        return {"status": "error", "detail": "Account not found"}

    if not account.auto_paused:
        return {"status": "error", "detail": "Account is not auto-paused"}

    # Reset health metrics partially
    account.auto_paused = False
    account.auto_paused_reason = None
    account.is_active = True
    account.bounce_streak = 0
    # Give a slight health boost on reactivation (but not full reset)
    account.health_score = max(account.health_score or 0, 60)
    db.commit()

    print(f"[Health Monitor] ✅ Reactivated account {account.email}")
    return {"status": "success", "health_score": account.health_score}


# ============================================================
# SMART WARMUP LIMIT SUGGESTION
# ============================================================
def suggest_warmup_limit(account) -> int:
    """
    Suggest a safe daily warmup limit based on account health and age.
    
    Rules:
    - New account (< 3 days): 5/day
    - Account age < 7 days: 10/day
    - Account age < 14 days: 20/day
    - Account age < 30 days: 30/day
    - Account age >= 30 days: 40/day
    
    If health is poor, reduce warmup limits appropriately.
    """
    # Check account age
    if account.created_at:
        age_days = (datetime.utcnow() - account.created_at).days
    else:
        age_days = 999
        
    limit = 5
    if age_days >= 14:
        limit = 20
    elif age_days >= 7:
        limit = 15
    elif age_days >= 3:
        limit = 10
        
    # Adjust for health
    health = account.health_score if account.health_score is not None else 0
    if health < 70:
        # If health is low, keep warmup very safe
        limit = min(limit, 15)
    elif health < 85:
        # Medium health
        limit = min(limit, 25)
        
    return limit

# ============================================================
# SMART DAILY LIMIT SUGGESTION
# ============================================================
def suggest_daily_limit(account) -> int:
    """
    Suggest a safe daily sending limit based on account health and age.
    
    Rules:
    - New account (< 3 days): 5/day
    - Account age < 7 days: 20/day
    - Account age < 14 days: 50/day
    - Account age < 30 days: 100/day
    - Warmup mode: use warmup_daily_limit
    - Low health (50-70): 50/day
    - Medium health (70-85): 150/day
    - Good health (85-95): 300/day
    - Excellent (95-100): 500/day
    """
    # NOTE: Warmup and Campaign are INDEPENDENT modules.
    # Warmup has its own limit (warmup_daily_limit) tracked by warmup_sent_today.
    # Campaign has its own limit (daily_limit) tracked by sent_today.
    # DO NOT reduce campaign limit based on warmup status.

    # Check account age
    if account.created_at:
        age_days = (datetime.utcnow() - account.created_at).days
    else:
        age_days = 999  # Unknown age, assume old

    user_limit = account.daily_limit or 5000
    
    # If user explicitly turned off smart limit, just use their limit (with a minor check for critical health)
    if not getattr(account, 'smart_limit_enabled', False):
        if account.health_score is not None and account.health_score < 50:
            return min(user_limit, 20)
        return user_limit
    
    # Age-based limits (for new accounts) when Smart Limit is ON
    if age_days < 3:
        return min(user_limit, 5)
    elif age_days < 7:
        return min(user_limit, 20)
    elif age_days < 14:
        return min(user_limit, 50)
    elif age_days < 30:
        return min(user_limit, 100)

    # Health-based limits (for established accounts) when Smart Limit is ON
    health = account.health_score if account.health_score is not None else 0

    if health < 50:
        return min(user_limit, 20)  # Critical - minimal sending
    elif health < 70:
        return min(user_limit, 50)
    elif health < 85:
        return min(user_limit, 150)
    elif health < 95:
        return min(user_limit, 300)
    else:
        return user_limit


# ============================================================
# DAILY STATS TRACKING
# ============================================================
def _record_daily_stat(db, account_id: str, event_type: str, provider_name: str = None):
    """Record a daily stat event for analytics."""
    today = datetime.utcnow().strftime("%Y-%m-%d")

    stat = db.query(database.AccountDailyStats).filter(
        database.AccountDailyStats.account_id == account_id,
        database.AccountDailyStats.date == today,
        database.AccountDailyStats.provider_name == provider_name
    ).first()

    if not stat:
        stat = database.AccountDailyStats(
            account_id=account_id,
            date=today,
            provider_name=provider_name
        )
        db.add(stat)
        db.flush()

    if event_type == "sent":
        stat.sent = (stat.sent or 0) + 1
    elif event_type == "bounced":
        stat.bounced = (stat.bounced or 0) + 1
    elif event_type == "opened":
        stat.opened = (stat.opened or 0) + 1
    elif event_type == "clicked":
        stat.clicked = (stat.clicked or 0) + 1
    elif event_type == "replied":
        stat.replied = (stat.replied or 0) + 1

    db.commit()


def get_account_stats(db, account_id: str, days: int = 30) -> list:
    """Get daily stats for an account over the last N days."""
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    stats = db.query(database.AccountDailyStats).filter(
        database.AccountDailyStats.account_id == account_id,
        database.AccountDailyStats.date >= cutoff
    ).order_by(database.AccountDailyStats.date.asc()).all()

    return [{
        "date": s.date,
        "sent": s.sent or 0,
        "bounced": s.bounced or 0,
        "opened": s.opened or 0,
        "clicked": s.clicked or 0,
        "replied": s.replied or 0
    } for s in stats]


# ============================================================
# SCHEDULED HEALTH AUDIT
# ============================================================
def run_health_audit():
    """
    Scheduled job (every 2 hours) — audits all active sending accounts.
    Recalculates health scores and auto-pauses unhealthy accounts.
    """
    print("[Health Audit] Starting periodic health audit...")
    db = database.SessionLocal()
    try:
        accounts = db.query(database.SendingAccount).filter(
            database.SendingAccount.is_active == True
        ).all()

        paused_count = 0
        for acc in accounts:
            # Recalculate health
            acc.health_score = calculate_health_score(acc)
            acc.last_health_check = datetime.utcnow()

            # Check auto-pause
            if check_auto_pause(db, acc):
                paused_count += 1

        db.commit()
        print(f"[Health Audit] Completed. {len(accounts)} accounts audited, {paused_count} auto-paused.")
    except Exception as e:
        print(f"[Health Audit] Error: {e}")
        db.rollback()
    finally:
        db.close()


def get_health_report(db, account_id: str) -> dict:
    """Get a detailed health report for a specific account."""
    account = db.query(database.SendingAccount).filter(
        database.SendingAccount.id == account_id
    ).first()
    if not account:
        return {"error": "Account not found"}

    total_sent = account.total_sent or 0
    total_bounced = account.total_bounced or 0
    total_opened = account.total_opened or 0
    total_replied = account.total_replied or 0

    bounce_rate = (total_bounced / total_sent * 100) if total_sent > 0 else 0
    open_rate = (total_opened / total_sent * 100) if total_sent > 0 else 0
    reply_rate = (total_replied / total_sent * 100) if total_sent > 0 else 0

    # Determine health status
    health = account.health_score if account.health_score is not None else 0
    if health >= 95:
        status = "excellent"
        status_label = "Excellent 🟢"
    elif health >= 85:
        status = "good"
        status_label = "Good 🟢"
    elif health >= 70:
        status = "fair"
        status_label = "Fair 🟡"
    elif health >= 50:
        status = "warning"
        status_label = "Warning 🟠"
    else:
        status = "critical"
        status_label = "Critical 🔴"

    # Generate recommendations
    recommendations = []
    if bounce_rate > 5:
        recommendations.append("High bounce rate! Clean your lead list and verify emails before sending.")
    if bounce_rate > 2:
        recommendations.append("Consider enabling email validation before campaigns.")
    if open_rate < 10 and total_sent > 50:
        recommendations.append("Low open rate. Improve subject lines and send during business hours.")
    if account.bounce_streak and account.bounce_streak >= 3:
        recommendations.append(f"Warning: {account.bounce_streak} consecutive bounces. Check SMTP credentials.")
    if not recommendations:
        recommendations.append("Account health looks good! Keep it up.")

    return {
        "account_id": account_id,
        "email": account.email,
        "health_score": health,
        "status": status,
        "status_label": status_label,
        "auto_paused": account.auto_paused or False,
        "auto_paused_reason": account.auto_paused_reason,
        "metrics": {
            "total_sent": total_sent,
            "total_bounced": total_bounced,
            "total_opened": total_opened,
            "total_replied": total_replied,
            "bounce_rate": round(bounce_rate, 2),
            "open_rate": round(open_rate, 2),
            "reply_rate": round(reply_rate, 2),
            "bounce_streak": account.bounce_streak or 0,
        },
        "suggested_daily_limit": suggest_daily_limit(account),
        "current_daily_limit": account.daily_limit,
        "recommendations": recommendations,
        "last_health_check": str(account.last_health_check) if account.last_health_check else None
    }
