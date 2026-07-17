with open('main_live.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace get_sending_accounts with a wrapped version
start_str = "def get_sending_accounts(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):"
import_traceback = "import traceback\n"
new_func = """def get_sending_accounts(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
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
                "smart_limit_enabled": getattr(acc, "smart_limit_enabled", False),
                "smart_warmup_enabled": getattr(acc, "smart_warmup_enabled", False),
                "health_score": health_monitor.calculate_health_score(acc),
                "created_at": acc.created_at,
                # --- New health fields ---
                "total_sent": acc.total_sent or 0,
                "total_bounced": acc.total_bounced or 0,
                "total_opened": acc.total_opened or 0,
                "total_replied": acc.total_replied or 0,
                "bounce_streak": acc.bounce_streak or 0,
                "auto_paused": acc.auto_paused or False,
                "auto_paused_reason": acc.auto_paused_reason,
                "suggested_daily_limit": health_monitor.suggest_daily_limit(acc),
                "suggested_warmup_limit": getattr(acc, "warmup_daily_limit", 5),
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
        return result
    except Exception as e:
        import traceback
        err_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail=str(e) + '\\n' + err_str)
"""

if "except Exception as e" not in text:
    # Just to be safe, find the end of the function.
    # Actually, we can just replace the whole function block.
    # Let's do it simply using regex
    import re
    # We replace from def get_sending_accounts to @app.post("/api/sending-accounts")
    pattern = r"def get_sending_accounts\(.*?\):.*?return result\s+"
    text = re.sub(pattern, new_func + "\n", text, flags=re.DOTALL)
    
    with open('main_live.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Wrapped with try-except")
else:
    print("Already wrapped?")
