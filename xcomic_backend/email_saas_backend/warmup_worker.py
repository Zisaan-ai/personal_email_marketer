import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time

class WarmupWorker:
    """
    Handles the execution of email warmup. 
    1. Sends emails to the seed network via SMTP.
    2. Logs into the seed accounts via IMAP to simulate human behavior (Unspam, Read, Reply).
    """
    
    def __init__(self, sender_email: str, sender_password: str, smtp_host: str, smtp_port: int, imap_host: str, imap_port: int):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.imap_host = imap_host
        self.imap_port = imap_port

    def generate_human_like_content(self) -> dict:
        """
        Generates conversational, non-spammy content to build reputation.
        In a production environment, this could hook into an LLM (OpenAI/Gemini).
        """
        subjects = [
            "Following up on our last discussion",
            "Quick question about the upcoming project",
            "Are we still meeting on Thursday?",
            "Notes from yesterday's sync"
        ]
        body_templates = [
            "Hi there,\n\nJust wanted to check if you had time to review the document I sent over earlier? Let me know your thoughts.\n\nBest,\nSender",
            "Hey,\n\nI hope you're having a good week. Can we reschedule our call to next Tuesday? Let me know what time works best for you.\n\nThanks,\nSender",
            "Hello,\n\nI'm following up to see if you need any additional information from my side to proceed. I'm happy to jump on a quick call if needed.\n\nRegards,\nSender"
        ]
        return {
            "subject": random.choice(subjects),
            "body": random.choice(body_templates)
        }

    def send_warmup_email(self, target_seed_email: str):
        """
        Sends an email from the user's mailbox to a seed network mailbox.
        """
        content = self.generate_human_like_content()
        
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = target_seed_email
        msg['Subject'] = content["subject"]
        msg.attach(MIMEText(content["body"], 'plain'))
        
        try:
            print(f"[SMTP] Connecting to {self.smtp_host}...")
            # Using SMTP_SSL for standard secure port 465, or TLS for 587
            if self.smtp_port == 465:
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()
                
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            print(f"[SMTP] Successfully sent warmup email to {target_seed_email}")
            return True
        except Exception as e:
            print(f"[SMTP ERROR] Failed to send warmup email: {e}")
            return False

    def process_seed_inbox(self, seed_email: str, seed_password: str, sender_to_look_for: str):
        """
        Logs into a seed mailbox (the receiver) and simulates positive human interactions:
        1. Checks Spam folder, moves email to Inbox (Not Spam).
        2. Opens the email (Marks as Read).
        3. Marks as Important (Stars the email).
        4. Sends a conversational reply.
        """
        try:
            print(f"[IMAP] Logging into seed mailbox {seed_email}...")
            mail = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
            mail.login(seed_email, seed_password)
            
            # Step 1: Check Spam Folder
            # Note: Folder names vary by provider ('[Gmail]/Spam', 'Junk', etc.)
            mail.select('"[Gmail]/Spam"') 
            
            # Search for emails from the warmup sender
            status, messages = mail.search(None, f'FROM "{sender_to_look_for}"')
            if status == "OK" and messages[0]:
                for num in messages[0].split():
                    print(f"[IMAP] Found email in SPAM. Moving to Inbox...")
                    # Copy to Inbox and delete from Spam (Unspam)
                    mail.copy(num, 'INBOX')
                    mail.store(num, '+FLAGS', '\\Deleted')
                mail.expunge()
            
            # Step 2 & 3: Go to Inbox, Mark as Read and Important
            mail.select('INBOX')
            status, messages = mail.search(None, f'FROM "{sender_to_look_for}" UNSEEN')
            if status == "OK" and messages[0]:
                for num in messages[0].split():
                    print(f"[IMAP] Reading email and marking as IMPORTANT...")
                    # Mark as read
                    mail.store(num, '+FLAGS', '\\Seen')
                    # Mark as important (Flagged)
                    mail.store(num, '+FLAGS', '\\Flagged')
                    
                    # Step 4: Simulate sending a reply
                    self._simulate_reply(seed_email, seed_password, sender_to_look_for)
                    
            mail.logout()
            print(f"[IMAP] Seed mailbox processing complete.")
        except Exception as e:
            print(f"[IMAP ERROR] Failed to process seed inbox: {e}")

    def _simulate_reply(self, seed_email: str, seed_password: str, original_sender: str):
        """
        Helper method to send a reply back to the original sender to boost Reply Rate.
        """
        print(f"[SMTP] Seed {seed_email} is replying to {original_sender}...")
        reply_msg = MIMEMultipart()
        reply_msg['From'] = seed_email
        reply_msg['To'] = original_sender
        reply_msg['Subject'] = "Re: Following up"
        reply_msg.attach(MIMEText("Thanks for reaching out! I'll take a look and get back to you shortly.", 'plain'))
        
        try:
            # Assuming seed uses same SMTP host for simplicity in this example
            server = smtplib.SMTP_SSL(self.smtp_host, 465)
            server.login(seed_email, seed_password)
            server.send_message(reply_msg)
            server.quit()
        except Exception as e:
            print(f"[SMTP ERROR] Seed failed to reply: {e}")

# Example Usage:
# worker = WarmupWorker("user@domain.com", "pass123", "smtp.gmail.com", 465, "imap.gmail.com", 993)
# worker.send_warmup_email("seed1@gmail.com")
# worker.process_seed_inbox("seed1@gmail.com", "seedpass123", "user@domain.com")
