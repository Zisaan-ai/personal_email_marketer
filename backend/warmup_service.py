import imaplib
import smtplib
import email
import traceback
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import database
import ai_core

WARMUP_HEADER = "X-Warmup-Identifier"
WARMUP_ID = "email-marketer-v1"

def move_spam_to_inbox(acc):
    """Logs into IMAP, finds warmup emails in Spam, moves them to Inbox, and marks as Read."""
    try:
        imap = imaplib.IMAP4_SSL(acc.imap_server, acc.imap_port, timeout=15)
        imap.login(acc.smtp_username, acc.imap_password)
        
        # Standard spam folder names
        spam_folders = ['[Gmail]/Spam', 'Spam', 'Junk', 'Junk Email']
        target_folder = None
        
        # Find the spam folder
        typ, mailboxes = imap.list()
        if typ == 'OK':
            for mailbox in mailboxes:
                name = mailbox.decode().split('"" ')[-1].strip('"')
                if any(sf.lower() in name.lower() for sf in spam_folders):
                    target_folder = name
                    break
        
        if not target_folder:
            target_folder = '[Gmail]/Spam'
            
        try:
            imap.select(target_folder)
        except Exception:
            try:
                imap.select('Spam')
            except Exception:
                pass
                
        typ, data = imap.search(None, 'UNSEEN')
        if typ == 'OK' and data[0]:
            for num in data[0].split():
                typ, msg_data = imap.fetch(num, '(RFC822)')
                if typ == 'OK':
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    if msg.get(WARMUP_HEADER) == WARMUP_ID:
                        imap.store(num, '+FLAGS', '\\Seen')
                        imap.copy(num, 'INBOX')
                        imap.store(num, '+FLAGS', '\\Deleted')
            imap.expunge()
            
        # Also check Inbox and mark as read
        try:
            imap.select('INBOX')
            typ, data = imap.search(None, 'UNSEEN')
            if typ == 'OK' and data[0]:
                for num in data[0].split():
                    typ, msg_data = imap.fetch(num, '(RFC822.HEADER)')
                    if typ == 'OK':
                        raw_header = msg_data[0][1].decode('utf-8', errors='ignore')
                        if f"{WARMUP_HEADER}: {WARMUP_ID}" in raw_header:
                            imap.store(num, '+FLAGS', '\\Seen')
        except Exception:
            pass
            
        imap.logout()
    except Exception as e:
        print(f"IMAP Error for {acc.email}: {e}")

def send_warmup_email(db, sender_acc, all_warmup_accounts):
    """Sends a conversational AI email from sender to a random target in the network."""
    targets = [a for a in all_warmup_accounts if a.id != sender_acc.id]
    if not targets:
        return

    target_acc = random.choice(targets)
    
    # Generate content using AI
    prompt = "Write a very short (2-3 sentences), casual, generic email to a colleague or friend. It should look like normal human conversation. Just return a JSON with 'subject' and 'body'. No markdown."
    content_str = ai_core._call_ai_api(prompt)
    
    try:
        import json
        content = json.loads(content_str)
        subject = content.get("subject", "Quick question")
        body = content.get("body", "Hey, how are you doing today? Let me know when you're free to chat.")
    except Exception:
        subject = "Checking in"
        body = "Hi! Just wanted to check in and see how things are going. Let's catch up soon."

    try:
        if sender_acc.smtp_port == 465:
            server = smtplib.SMTP_SSL(sender_acc.smtp_server, sender_acc.smtp_port, timeout=10)
        else:
            server = smtplib.SMTP(sender_acc.smtp_server, sender_acc.smtp_port, timeout=10)
            server.starttls()
            
        server.login(sender_acc.smtp_username, sender_acc.smtp_password)
        
        msg = MIMEMultipart("alternative")
        msg['Subject'] = subject
        msg['From'] = f"{sender_acc.name or ''} <{sender_acc.smtp_username}>"
        msg['To'] = target_acc.email
        msg['Date'] = formatdate(localtime=True)
        msg[WARMUP_HEADER] = WARMUP_ID
        
        msg.attach(MIMEText(body, "plain"))
        
        server.send_message(msg)
        server.quit()
        
        sender_acc.warmup_sent_today += 1
        db.commit()
        print(f"Warmup: Sent from {sender_acc.email} to {target_acc.email}")
    except Exception as e:
        print(f"Warmup SMTP Error for {sender_acc.email}: {e}")

def run_warmup_cycle():
    """Main scheduler entrypoint."""
    print("Running Warmup Cycle...")
    db = database.SessionLocal()
    try:
        accounts = db.query(database.SendingAccount).filter(
            database.SendingAccount.is_active == True,
            database.SendingAccount.warmup_enabled == True
        ).all()
        if not accounts:
            return
            
        for acc in accounts:
            if acc.imap_server and acc.imap_password:
                move_spam_to_inbox(acc)
                
            daily_target = acc.warmup_daily_limit
            if acc.warmup_sent_today < daily_target:
                if random.random() < 0.5:
                    send_warmup_email(db, acc, accounts)
    except Exception as e:
        print(f"Warmup cycle error: {e}")
    finally:
        db.close()

def reset_daily_warmup_counts():
    """Runs at midnight to reset counts and apply increments."""
    db = database.SessionLocal()
    try:
        accounts = db.query(database.SendingAccount).filter(
            database.SendingAccount.warmup_enabled == True
        ).all()
        for acc in accounts:
            acc.warmup_sent_today = 0
            acc.warmup_daily_limit += acc.warmup_increment_per_day
        db.commit()
    except Exception as e:
        print(f"Warmup reset error: {e}")
        db.rollback()
    finally:
        db.close()
