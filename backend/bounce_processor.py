import imaplib
import email
from email.header import decode_header
import re
import datetime
import os
import database

def check_bounces():
    """
    Connects to the IMAP server of active sending accounts and checks for bounce messages.
    If a bounce is detected, it marks the corresponding lead in the database as 'bounced'.
    """
    print("Starting IMAP Bounce Processor...")
    db = database.SessionLocal()
    try:
        accounts = db.query(database.SendingAccount).filter(
            database.SendingAccount.is_active == True
        ).all()
        
        bounce_patterns = [
            re.compile(r"Delivery to the following recipient failed permanently:\s*([\w\.-]+@[\w\.-]+)"),
            re.compile(r"Address not found\s*Your message wasn't delivered to ([\w\.-]+@[\w\.-]+)"),
            re.compile(r"Message not delivered\s*Your message couldn't be delivered to ([\w\.-]+@[\w\.-]+)"),
            re.compile(r"Action: failed\s*Status: \d\.\d\.\d\s*Remote-MTA: dns;.*\s*Diagnostic-Code: smtp;.*\s*Last-Attempt-Date:.*\s*Final-Recipient: rfc822; ([\w\.-]+@[\w\.-]+)", re.IGNORECASE | re.MULTILINE)
        ]
        
        for account in accounts:
            imap_server = account.imap_server
            imap_port = account.imap_port
            
            if not imap_server:
                if "gmail.com" in account.smtp_server:
                    imap_server = "imap.gmail.com"
                    imap_port = 993
                else:
                    imap_server = account.smtp_server.replace("smtp.", "imap.")
                    imap_port = 993
                
            try:
                print(f"Connecting to IMAP for {account.smtp_username}...")
                mail = imaplib.IMAP4_SSL(imap_server, imap_port)
                mail.login(account.smtp_username, account.imap_password or account.smtp_password)
                mail.select("inbox")
                
                date_since = (datetime.date.today() - datetime.timedelta(days=3)).strftime("%d-%b-%Y")
                
                subjects = [
                    "Undelivered Mail Returned to Sender",
                    "Delivery Status Notification (Failure)",
                    "Mail delivery failed",
                    "Returned mail: see transcript for details"
                ]
                
                all_bounce_msgs = []
                for subj in subjects:
                    status, messages = mail.search(None, f'(SENTSINCE {date_since} SUBJECT "{subj}")')
                    if status == "OK":
                        msg_nums = messages[0].split()
                        all_bounce_msgs.extend(msg_nums)
                
                all_bounce_msgs = list(set(all_bounce_msgs))
                
                bounced_emails = set()
                
                for num in all_bounce_msgs:
                    try:
                        status, msg_data = mail.fetch(num, "(RFC822)")
                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                msg = email.message_from_bytes(response_part[1])
                                body = ""
                                if msg.is_multipart():
                                    for part in msg.walk():
                                        if part.get_content_type() == "text/plain":
                                            body += part.get_payload(decode=True).decode(errors="ignore")
                                else:
                                    body = msg.get_payload(decode=True).decode(errors="ignore")
                                    
                                for pattern in bounce_patterns:
                                    match = pattern.search(body)
                                    if match:
                                        bounced_email = match.group(1).lower().strip()
                                        bounced_emails.add(bounced_email)
                                        break
                    except Exception as e:
                        print(f"Error reading message {num}: {e}")
                
                mail.logout()
                
                # Update leads in DB + health tracking
                if bounced_emails:
                    print(f"Found {len(bounced_emails)} bounced emails for account {account.smtp_username}")
                    import health_monitor
                    for email_address in bounced_emails:
                        db.query(database.CampaignLead).filter(
                            database.CampaignLead.email == email_address
                        ).update({"status": "bounced"})
                        # HEALTH TRACKING: Update account health for each bounce
                        health_monitor.update_health_after_send(db, str(account.id), False)
                    db.commit()
                        
            except Exception as e:
                print(f"Failed to process IMAP bounces for {account.smtp_username}: {e}")
                
        print("IMAP Bounce Processor finished.")
    except Exception as e:
        print(f"Bounce processor error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_bounces()
