"""
Warmup Service - Reply-to-Reply Conversation System
====================================================
Each warmup cycle:
  1. Account A sends a fresh warmup email to Account B (unique content via AI)
  2. Account B checks its INBOX → finds the warmup email from A → replies with unique AI content
  3. Account A checks its INBOX → finds B's reply → optionally replies back

This creates real email conversation threads, which Gmail/Outlook treat as
high-trust signals and dramatically improve deliverability reputation.

Key headers used for threading:
  - Message-ID   : unique per email (set by us)
  - In-Reply-To  : Message-ID of the email being replied to
  - References   : full chain of Message-IDs (for thread grouping)
  - X-Warmup-Identifier : our internal marker (never shown to user)
"""

import imaplib
import smtplib
import email
import email.utils
import random
import uuid
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid
import database
import ai_core

WARMUP_HEADER = "X-Warmup-Identifier"
WARMUP_ID = "email-marketer-v1"

# ──────────────────────────────────────────────
# AI Content Generation
# ──────────────────────────────────────────────

def _generate_fresh_email():
    """Generate a brand-new warmup email subject + body via AI."""
    prompt = (
        "Write a very short (2-3 sentences), casual, human-sounding email "
        "to a colleague or friend. Topics can be: weekend plans, a project update, "
        "a funny observation, asking for advice, sharing good news, etc. "
        "Each email must be unique and NOT repeat the same topic. "
        "Return ONLY a JSON object with keys 'subject' and 'body'. No markdown, no extra text."
    )
    try:
        raw = ai_core._call_ai_api(prompt)
        content = json.loads(raw)
        return content.get("subject", "Quick update"), content.get("body", "Hey, just checking in! How's everything going?")
    except Exception as e:
        print(f"[Warmup] AI fresh email error: {e}")
        fallbacks = [
            ("Weekend plans?", "Hey! Any plans for the weekend? Would love to catch up over coffee if you're free."),
            ("Quick question", "Hi! Hope you're having a good week. Do you have 5 minutes to chat later today?"),
            ("Thought of you", "Hey, I came across something interesting today and immediately thought of you. I'll share it later!"),
            ("Great news!", "Just wanted to share — things are going really well on my end. Hope the same for you!"),
            ("Checking in", "Hi there! It's been a while. Just wanted to say hello and hope everything's great with you."),
        ]
        return random.choice(fallbacks)


def _generate_reply_body(original_subject: str, original_body: str):
    """Generate a unique, human-like reply to a given email via AI."""
    prompt = (
        f"You received this email:\n"
        f"Subject: {original_subject}\n"
        f"Body: {original_body}\n\n"
        "Write a very short (1-3 sentences), casual and natural reply. "
        "Sound like a real person responding in conversation. "
        "Do NOT repeat the original email. Just write the reply body text. "
        "Return ONLY a JSON with key 'body'. No markdown, no extra text."
    )
    try:
        raw = ai_core._call_ai_api(prompt)
        content = json.loads(raw)
        return content.get("body", "Thanks for reaching out! I'll get back to you shortly.")
    except Exception as e:
        print(f"[Warmup] AI reply generation error: {e}")
        fallbacks = [
            "Thanks for the message! I'll get back to you soon.",
            "Hey! Good to hear from you. Let's definitely catch up!",
            "Sounds great! I'll be in touch.",
            "Thanks! Really appreciate you reaching out.",
            "Haha, that's so true! We should talk more soon.",
        ]
        return random.choice(fallbacks)


# ──────────────────────────────────────────────
# SMTP Helpers
# ──────────────────────────────────────────────

def _smtp_connect(acc):
    """Connect and login to SMTP. Returns server object."""
    if acc.smtp_port == 465:
        server = smtplib.SMTP_SSL(acc.smtp_server, acc.smtp_port, timeout=15)
    else:
        server = smtplib.SMTP(acc.smtp_server, acc.smtp_port, timeout=15)
        server.ehlo()
        server.starttls()
        server.ehlo()
    server.login(acc.smtp_username, acc.smtp_password)
    return server


def _make_message_id(domain: str) -> str:
    """Generate a unique RFC-compliant Message-ID."""
    unique = uuid.uuid4().hex
    return f"<warmup-{unique}@{domain}>"


# ──────────────────────────────────────────────
# Step 1: Send a fresh warmup email
# ──────────────────────────────────────────────

def send_warmup_email(sender_acc, target_acc) -> dict:
    """
    Send a fresh warmup email from sender_acc to target_acc.
    Returns {'success': bool, 'message_id': str, 'subject': str, 'body': str}
    """
    subject, body = _generate_fresh_email()

    # Extract domain for Message-ID
    try:
        domain = sender_acc.smtp_username.split("@")[1]
    except Exception:
        domain = "mail.local"

    msg_id = _make_message_id(domain)

    try:
        server = _smtp_connect(sender_acc)

        msg = MIMEMultipart("alternative")
        msg["Message-ID"] = msg_id
        msg["Subject"] = subject
        msg["From"] = f"{sender_acc.name or ''} <{sender_acc.smtp_username}>".strip()
        msg["To"] = target_acc.email
        msg["Date"] = formatdate(localtime=True)
        msg[WARMUP_HEADER] = WARMUP_ID

        msg.attach(MIMEText(body, "plain"))
        server.send_message(msg)
        server.quit()

        print(f"[Warmup] ✉️  Sent: {sender_acc.email} → {target_acc.email} | Subject: {subject}")
        return {"success": True, "message_id": msg_id, "subject": subject, "body": body}

    except Exception as e:
        print(f"[Warmup] SMTP Error ({sender_acc.email}): {e}")
        return {"success": False, "message_id": None, "subject": subject, "body": body}


# ──────────────────────────────────────────────
# Step 2: Check INBOX and reply to warmup emails
# ──────────────────────────────────────────────

def check_inbox_and_reply(replier_acc, all_accounts: list, max_replies: int = None):
    """
    Checks replier_acc's INBOX for unread warmup emails.
    For each warmup email found → generates a unique AI reply → sends it back.
    Also moves any warmup spam to inbox.

    Returns number of replies sent.
    """
    if not replier_acc.imap_server or not replier_acc.imap_password:
        return 0

    replies_sent = 0

    try:
        imap = imaplib.IMAP4_SSL(replier_acc.imap_server, replier_acc.imap_port, timeout=20)
        imap.login(replier_acc.smtp_username, replier_acc.imap_password)

        # ── Step 2a: Move warmup emails from Spam to Inbox ──
        _rescue_spam(imap)

        # ── Step 2b: Find unread warmup emails in Inbox ──
        imap.select("INBOX")
        typ, data = imap.search(None, "UNSEEN")
        if typ != "OK" or not data[0]:
            imap.logout()
            return 0

        warmup_emails = []  # list of (num, from_addr, msg_id, subject, body)

        for num in data[0].split():
            if max_replies is not None and len(warmup_emails) >= max_replies:
                break
            
            typ2, msg_data = imap.fetch(num, "(RFC822)")
            if typ2 != "OK":
                continue

            raw = msg_data[0][1]
            msg = email.message_from_bytes(raw)

            # Only process our warmup emails
            if msg.get(WARMUP_HEADER) != WARMUP_ID:
                continue

            from_addr = email.utils.parseaddr(msg.get("From", ""))[1]
            original_msg_id = msg.get("Message-ID", "").strip()
            original_subject = msg.get("Subject", "Re: Hello")
            references = msg.get("References", "")

            # Extract plain text body
            original_body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            original_body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                        except Exception:
                            pass
                        break
            else:
                try:
                    original_body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                except Exception:
                    pass

            # Mark as read
            imap.store(num, "+FLAGS", "\\Seen")

            warmup_emails.append({
                "num": num,
                "from_addr": from_addr,
                "msg_id": original_msg_id,
                "subject": original_subject,
                "body": original_body,
                "references": references,
            })

        imap.logout()

        # ── Step 2c: Reply to each warmup email via SMTP ──
        for wm in warmup_emails:
            # Find the sender account object so we can connect to their SMTP
            sender_acc = None
            for a in all_accounts:
                if a.email.lower() == wm["from_addr"].lower():
                    sender_acc = a
                    break

            if not sender_acc:
                # We don't manage that account, skip
                print(f"[Warmup] Skipping reply — unknown sender: {wm['from_addr']}")
                continue

            # Build reply subject
            reply_subject = wm["subject"] if wm["subject"].startswith("Re:") else f"Re: {wm['subject']}"

            # Generate unique reply body via AI
            reply_body = _generate_reply_body(wm["subject"], wm["body"])

            # Build Message-ID threading chain
            try:
                domain = replier_acc.smtp_username.split("@")[1]
            except Exception:
                domain = "mail.local"

            new_msg_id = _make_message_id(domain)
            ref_chain = f"{wm['references']} {wm['msg_id']}".strip() if wm["references"] else wm["msg_id"]

            try:
                server = _smtp_connect(replier_acc)

                reply_msg = MIMEMultipart("alternative")
                reply_msg["Message-ID"] = new_msg_id
                reply_msg["Subject"] = reply_subject
                reply_msg["From"] = f"{replier_acc.name or ''} <{replier_acc.smtp_username}>".strip()
                reply_msg["To"] = wm["from_addr"]
                reply_msg["Date"] = formatdate(localtime=True)
                reply_msg["In-Reply-To"] = wm["msg_id"]
                reply_msg["References"] = ref_chain
                reply_msg[WARMUP_HEADER] = WARMUP_ID

                reply_msg.attach(MIMEText(reply_body, "plain"))
                server.send_message(reply_msg)
                server.quit()

                replies_sent += 1
                print(f"[Warmup] 💬 Reply: {replier_acc.email} → {wm['from_addr']} | {reply_subject}")

            except Exception as e:
                print(f"[Warmup] Reply SMTP error ({replier_acc.email}): {e}")

    except Exception as e:
        print(f"[Warmup] IMAP error ({replier_acc.email}): {e}")

    return replies_sent


# ──────────────────────────────────────────────
# Helper: Move Spam → Inbox
# ──────────────────────────────────────────────

def _rescue_spam(imap):
    """Move any warmup emails from Spam/Junk folder to Inbox."""
    spam_folders = ["[Gmail]/Spam", "Spam", "Junk", "Junk Email", "Bulk Mail"]
    target_folder = None

    try:
        typ, mailboxes = imap.list()
        if typ == "OK":
            for mailbox in mailboxes:
                name = mailbox.decode().split('"" ')[-1].strip('"')
                if any(sf.lower() in name.lower() for sf in spam_folders):
                    target_folder = name
                    break
    except Exception:
        pass

    if not target_folder:
        return

    try:
        imap.select(target_folder)
        typ, data = imap.search(None, "UNSEEN")
        if typ == "OK" and data[0]:
            for num in data[0].split():
                typ2, msg_data = imap.fetch(num, "(RFC822.HEADER)")
                if typ2 == "OK":
                    raw_header = msg_data[0][1].decode("utf-8", errors="ignore")
                    if f"{WARMUP_HEADER}: {WARMUP_ID}" in raw_header:
                        imap.store(num, "+FLAGS", "\\Seen")
                        try:
                            imap.copy(num, "INBOX")
                            imap.store(num, "+FLAGS", "\\Deleted")
                        except Exception:
                            pass
            try:
                imap.expunge()
            except Exception:
                pass
    except Exception as e:
        print(f"[Warmup] Spam rescue error: {e}")


# ──────────────────────────────────────────────
# Main Warmup Cycle
# ──────────────────────────────────────────────

def run_warmup_cycle():
    """
    Main scheduler entry point. Called every ~30 minutes by cron.
    """
    import os, time
    lock_file = os.path.join(os.path.dirname(__file__), "warmup.lock")
    if os.path.exists(lock_file):
        if time.time() - os.path.getmtime(lock_file) < 7200:
            print("[Warmup] Cycle already running (lock file exists). Skipping.")
            return
        else:
            print("[Warmup] Stale lock file found. Removing.")
            try: os.remove(lock_file)
            except: pass
            
    try:
        with open(lock_file, "w") as f: f.write(str(time.time()))
    except Exception as e:
        print(f"[Warmup] Could not create lock file: {e}")

    print("[Warmup] ══ Starting warmup cycle ══")
    db = database.SessionLocal()
    detached_accounts = []

    try:
        accounts = db.query(database.SendingAccount).filter(
            database.SendingAccount.is_active == True,
            database.SendingAccount.warmup_enabled == True
        ).all()

        class DetachedAccount:
            def __init__(self, acc):
                self.id = acc.id
                self.email = acc.smtp_username  # always use smtp_username as the actual email
                self.name = acc.name
                self.imap_server = acc.imap_server
                self.imap_port = acc.imap_port
                self.imap_password = acc.imap_password
                self.smtp_server = acc.smtp_server
                self.smtp_port = acc.smtp_port
                self.smtp_username = acc.smtp_username
                self.smtp_password = acc.smtp_password
                self.warmup_daily_limit = acc.warmup_daily_limit or 5
                self.warmup_sent_today = acc.warmup_sent_today or 0
                self.smart_warmup_enabled = getattr(acc, "smart_warmup_enabled", False)
                self.health_score = acc.health_score
                self.created_at = acc.created_at

        detached_accounts = [DetachedAccount(a) for a in accounts]

    except Exception as e:
        print(f"[Warmup] Fetch error: {e}")
    finally:
        db.close()

    if not detached_accounts:
        print("[Warmup] No warmup-enabled accounts found.")
        return

    print(f"[Warmup] {len(detached_accounts)} account(s) active for warmup.")

    # ── Phase 1: Check inbox and reply to pending warmup emails ──
    for acc in detached_accounts:
        if acc.imap_server and acc.imap_password:
            available_quota = acc.warmup_daily_limit - (acc.warmup_sent_today or 0)
            if available_quota <= 0:
                print(f"[Warmup] Skipping replies for {acc.email}, daily limit reached ({acc.warmup_sent_today}/{acc.warmup_daily_limit})")
                continue
                
            replied = check_inbox_and_reply(acc, detached_accounts, max_replies=available_quota)
            if replied > 0:
                _increment_warmup_count(acc.id, replied)
                acc.warmup_sent_today = (acc.warmup_sent_today or 0) + replied

    # ── Phase 2: Send fresh warmup emails (paced over 24 hours) ──
    import pytz
    from datetime import datetime
    import math
    import time
    import health_monitor

    # Calculate pacing progress based on current Bangladesh Time (UTC+6)
    # The cron resets counts at 18:00 UTC (12:00 AM BD Time)
    bst = pytz.timezone("Asia/Dhaka")
    now_bst = datetime.now(bst)
    minutes_passed = now_bst.hour * 60 + now_bst.minute
    total_minutes = 1440
    # Add 5% buffer so it aims to complete slightly before midnight
    progress = min(1.0, (minutes_passed / total_minutes) * 1.05)

    for acc in detached_accounts:
        if acc.smart_warmup_enabled:
            target_limit = health_monitor.suggest_warmup_limit(acc)
        else:
            target_limit = acc.warmup_daily_limit

        expected_sent = int(math.ceil(target_limit * progress))
        
        if acc.warmup_sent_today >= target_limit:
            print(f"[Warmup] Daily limit reached for {acc.email} ({acc.warmup_sent_today}/{target_limit})")
            continue

        if acc.warmup_sent_today >= expected_sent:
            print(f"[Warmup] {acc.email} is on track ({acc.warmup_sent_today}/{expected_sent} expected by now). Skipping.")
            continue
            
        # We are behind schedule! Calculate how many to send to catch up.
        # Cap at 3 emails per cycle to prevent sudden spam-like bursts if far behind.
        to_send = expected_sent - acc.warmup_sent_today
        to_send = min(to_send, 3)

        targets = [t for t in detached_accounts if t.id != acc.id]
        if not targets:
            continue
            
        print(f"[Warmup] {acc.email} needs to send {to_send} to catch up (progress: {progress:.2%}).")

        for _ in range(to_send):
            target = random.choice(targets)
            result = send_warmup_email(acc, target)
    
            if result["success"]:
                _increment_warmup_count(acc.id, 1)
                acc.warmup_sent_today += 1
            time.sleep(2)  # brief pause between sends in a burst

    print("[Warmup] ══ Warmup cycle complete ══")
    
    import os
    lock_file = os.path.join(os.path.dirname(__file__), "warmup.lock")
    if os.path.exists(lock_file):
        try: os.remove(lock_file)
        except: pass


def _increment_warmup_count(account_id: str, count: int = 1):
    """Increment warmup counters and recalculate health score."""
    db_write = database.SessionLocal()
    try:
        import health_monitor
        db_acc = db_write.query(database.SendingAccount).filter(
            database.SendingAccount.id == account_id
        ).first()
        if db_acc:
            db_acc.warmup_sent_today = (db_acc.warmup_sent_today or 0) + count
            # db_acc.warmup_total_sent does not exist in db model
            db_acc.health_score = health_monitor.calculate_health_score(db_acc)
            db_write.commit()
    except Exception as e:
        db_write.rollback()
        print(f"[Warmup] Failed to update count for {account_id}: {e}")
    finally:
        db_write.close()


# ──────────────────────────────────────────────
# Midnight Reset
# ──────────────────────────────────────────────

def reset_daily_warmup_counts():
    """Runs at midnight. Resets today's count and increments daily limit."""
    db = database.SessionLocal()
    try:
        accounts = db.query(database.SendingAccount).filter(
            database.SendingAccount.warmup_enabled == True
        ).all()
        for acc in accounts:
            acc.warmup_sent_today = 0
            # Gradually increase daily limit (ramp-up)
            new_limit = (acc.warmup_daily_limit or 5) + (acc.warmup_increment_per_day or 2)
            acc.warmup_daily_limit = min(new_limit, 50)  # cap at 50/day max for warmup
        db.commit()
        print(f"[Warmup] Reset daily counts for {len(accounts)} account(s).")
    except Exception as e:
        print(f"[Warmup] Reset error: {e}")
        db.rollback()
    finally:
        db.close()
