import os

with open('backend/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

# BUG: The warmup check inside get_available_account() is WRONG.
# It skips the account for CAMPAIGN sending if warmup limit is reached.
# Warmup and Campaign are INDEPENDENT modules.
# Campaign sending should ONLY check sent_today vs daily_limit.
# Warmup sending should ONLY check warmup_sent_today vs warmup_daily_limit.

old_warmup_block = """            # Enforce warmup limits
            if acc_doc.warmup_enabled:
                effective_limit = acc_doc.warmup_daily_limit or 5
                if acc_doc.warmup_sent_today >= effective_limit:
                    continue"""

# Remove the warmup check entirely from get_available_account
# Campaign sending should NEVER check warmup limits
new_warmup_block = """            # NOTE: Warmup limits are NOT checked here.
            # Warmup and Campaign are independent modules with separate counters.
            # Campaign only checks sent_today vs daily_limit below."""

if old_warmup_block in text:
    text = text.replace(old_warmup_block, new_warmup_block)
    print("Fixed: Removed warmup limit check from get_available_account()")
else:
    print("ERROR: Could not find warmup block in get_available_account()")

# Also fix the send_to_lead function - it increments warmup_sent_today on campaign sends!
old_warmup_increment = """                if acc.warmup_enabled:
                    acc.warmup_sent_today += 1
                    db.commit()"""

new_warmup_increment = """                # DO NOT increment warmup counter for campaign sends
                # Warmup and Campaign are independent modules"""

if old_warmup_increment in text:
    text = text.replace(old_warmup_increment, new_warmup_increment)
    print("Fixed: Removed warmup counter increment from campaign send_to_lead()")
else:
    print("WARNING: Could not find warmup increment block")

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("\nDone! Warmup and Campaign are now fully independent.")
