import sys

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 4. get_available_account() replacement
old_get_avail = """    def get_available_account():
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
            # Enforce warmup limits
            if acc_doc.warmup_enabled:
                effective_limit = acc_doc.warmup_daily_limit or 5
                if acc_doc.warmup_sent_today >= effective_limit:
                    continue
            # Use smart suggested limit instead of raw daily_limit
            smart_limit = health_monitor.suggest_daily_limit(acc_doc)
            effective_daily = min(acc_doc.daily_limit or 500, smart_limit)
            if acc_doc.sent_today < effective_daily:
                # Track domain for rotation
                _last_domain_used[0] = acc_doc.email.split('@')[-1] if '@' in acc_doc.email else ''
                return acc_doc
        return None"""

new_get_avail = """    def get_available_account():
        # SMART SELECTION: Health-based ordering, skip auto-paused, check sending window
        all_accounts = db.query(database.SendingAccount).filter(
            database.SendingAccount.is_active == True,
            database.SendingAccount.user_id == campaign.user_id
        ).all()

        if not all_accounts:
            return None, "No active accounts found"
            
        active_accounts = [a for a in all_accounts if not a.auto_paused]
        if not active_accounts:
            return None, "All accounts are auto-paused due to poor health"
            
        active_accounts.sort(key=lambda a: a.health_score or 0, reverse=True)

        # Multi-domain rotation: prefer accounts from a different domain
        last_domain = _last_domain_used[0]
        preferred = []
        fallback = []
        for acc_doc in active_accounts:
            domain = acc_doc.email.split('@')[-1] if '@' in acc_doc.email else ''
            if last_domain and domain == last_domain:
                fallback.append(acc_doc)
            else:
                preferred.append(acc_doc)

        ordered = preferred + fallback  # Try different domain first
        
        last_reason = "No accounts met the criteria"
        for acc_doc in ordered:
            # Check sending window
            if not is_within_sending_window(acc_doc):
                last_reason = "Outside campaign sending window or days"
                continue
            # Enforce warmup limits
            if acc_doc.warmup_enabled:
                effective_limit = acc_doc.warmup_daily_limit or 5
                if acc_doc.warmup_sent_today >= effective_limit:
                    last_reason = f"Warmup limit reached ({effective_limit}/day) for {acc_doc.email}"
                    continue
            # Use smart suggested limit instead of raw daily_limit
            smart_limit = health_monitor.suggest_daily_limit(acc_doc)
            effective_daily = min(acc_doc.daily_limit or 500, smart_limit)
            if acc_doc.sent_today >= effective_daily:
                last_reason = f"Daily limit reached ({effective_daily}/day) for {acc_doc.email}"
                continue
            
            # Track domain for rotation
            _last_domain_used[0] = acc_doc.email.split('@')[-1] if '@' in acc_doc.email else ''
            return acc_doc, None
            
        return None, last_reason"""
        
content = content.replace(old_get_avail, new_get_avail)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Pass 2 get_avail done")
