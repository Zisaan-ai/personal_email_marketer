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
                mail = imaplib.IMAP4_SSL(imap_server, imap_port, timeout=15)
                mail.login(account.smtp_username, account.imap_password or account.smtp_password)
                mail.select("inbox")
                
                date_since = (datetime.date.today() - datetime.timedelta(days=3)).strftime("%d-%b-%Y")
                
                status, messages = mail.search(None, f'(SINCE {date_since})')
                if status != "OK" or not messages[0]:
                    mail.logout()
                    continue

                msg_nums = messages[0].split()
                
                bounced_emails = set()
                replies_found = 0
                
                # Pre-fetch all leads for this account to quickly check for replies
                account_leads = set()
                if account.user_id:
                    account_leads = {lead.email.lower() for lead in db.query(database.CampaignLead).join(database.Campaign).filter(database.Campaign.user_id == account.user_id).all()}
                
                for num in msg_nums:
                    try:
                        # Fetch header first to determine if we need the body
                        status, header_data = mail.fetch(num, "(BODY.PEEK[HEADER])")
                        if status != "OK": continue
                        
                        header_msg = None
                        for response_part in header_data:
                            if isinstance(response_part, tuple):
                                header_msg = email.message_from_bytes(response_part[1])
                                break
                        
                        if not header_msg: continue
                        
                        subject = ""
                        if header_msg["Subject"]:
                            decoded_subj = decode_header(header_msg["Subject"])[0]
                            subject = decoded_subj[0].decode(decoded_subj[1] or "utf-8", errors="ignore") if isinstance(decoded_subj[0], bytes) else decoded_subj[0]
                        
                        from_header = header_msg.get("From", "")
                        sender_email = ""
                        # Extract email address using regex
                        email_match = re.search(r'<([^>]+)>', from_header)
                        if email_match:
                            sender_email = email_match.group(1).lower().strip()
                        else:
                            sender_email = from_header.lower().strip()
                            
                        message_id = header_msg.get("Message-ID", f"unknown-{num.decode()}")
                        
                        is_bounce = False
                        bounce_subjects = ["Undelivered Mail Returned to Sender", "Delivery Status Notification (Failure)", "Mail delivery failed", "Returned mail: see transcript for details"]
                        if any(bs.lower() in subject.lower() for bs in bounce_subjects) or "mailer-daemon" in sender_email:
                            is_bounce = True
                            
                        is_lead_reply = sender_email in account_leads
                        
                        # Process if it's a bounce or a lead reply
                        if is_bounce or is_lead_reply:
                            # Fetch full body
                            status, msg_data = mail.fetch(num, "(RFC822)")
                            if status != "OK": continue
                            
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
                                    
                                    if is_bounce:
                                        for pattern in bounce_patterns:
                                            match = pattern.search(body)
                                            if match:
                                                bounced_emails.add(match.group(1).lower().strip())
                                                break
                                                
                                    if is_lead_reply and not is_bounce:
                                        # Check if we already have this reply
                                        existing = db.query(database.Reply).filter_by(message_id=message_id).first()
                                        if not existing:
                                            new_reply = database.Reply(
                                                account_id=account.id,
                                                message_id=message_id,
                                                sender_email=sender_email,
                                                subject=subject,
                                                body=body
                                            )
                                            db.add(new_reply)
                                            
                                            # Update lead status to replied
                                            if account.user_id:
                                                target_campaign_ids = [c.id for c in db.query(database.Campaign.id).filter(database.Campaign.user_id == account.user_id).all()]
                                                if target_campaign_ids:
                                                    db.query(database.CampaignLead).filter(
                                                        database.CampaignLead.email == sender_email,
                                                        database.CampaignLead.campaign_id.in_(target_campaign_ids)
                                                    ).update({"status": "replied", "replied": True}, synchronize_session=False)
                                            
                                            replies_found += 1
                    except Exception as e:
                        print(f"Error reading message {num}: {e}")
                
                mail.logout()
                
                # Update leads in DB + health tracking for bounces
                if bounced_emails:
                    print(f"Found {len(bounced_emails)} bounced emails for account {account.smtp_username}")
                    import health_monitor
                    for email_address in bounced_emails:
                        db.query(database.CampaignLead).filter(
                            database.CampaignLead.email == email_address
                        ).update({"status": "bounced"})
                        # HEALTH TRACKING: Update account health for each bounce
                        health_monitor.update_health_after_send(db, str(account.id), False)
                        
                if replies_found > 0:
                    print(f"Found {replies_found} new replies for account {account.smtp_username}")
                    import health_monitor
                    for _ in range(replies_found):
                        health_monitor.update_health_after_reply(db, str(account.id))
                        
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
