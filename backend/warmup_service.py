import imaplib
import smtplib
import email
import traceback
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import database
import health_monitor

WARMUP_HEADER = "X-Warmup-Identifier"
WARMUP_ID = "email-marketer-v1"

# ============================================================
# LARGE DIVERSE MESSAGE BANK — No AI needed
# 60+ unique messages across many natural topics
# ============================================================
WARMUP_MESSAGES = [
    # Project / work updates
    {"subject": "Quick project update", "body": "Hey! Just wanted to drop a quick note that we wrapped up the design phase yesterday. Things are moving along nicely — let me know if you want to sync up this week."},
    {"subject": "Re: That proposal", "body": "Hi there, just circling back on the proposal we discussed last time. Did you get a chance to look it over? Happy to jump on a quick call if needed."},
    {"subject": "Heads up on the deadline", "body": "Hey, just a heads up that the deadline for the report is this Friday. I've finished my section — let me know if you need anything from my end!"},
    {"subject": "Update on the client call", "body": "Hi! The client call went really well today. They loved the new approach. I'll share the notes shortly so we can align on next steps."},
    {"subject": "Files are ready", "body": "Hey, I've finished putting together those files you asked for. I'll send them over in a separate email. Let me know if anything looks off."},
    {"subject": "Small issue on my end", "body": "Hi, wanted to give you a heads up — I hit a small snag with the data formatting. It's not a blocker, but I wanted to keep you in the loop. I should have it sorted by tomorrow."},
    {"subject": "Good news!", "body": "Hey! Just got off the phone with the team — looks like we're good to move forward with the next phase. Super exciting stuff. Let's celebrate with coffee soon 😄"},
    {"subject": "Quick check-in", "body": "Hi there! Just wanted to check in and see how things are going on your end. It's been a bit quiet and wanted to make sure everything is okay."},
    {"subject": "Finished the review", "body": "Hi, I just finished reviewing the document you shared. Overall it looks great — left a few minor comments. Let me know what you think!"},
    {"subject": "Following up", "body": "Hey, just following up from our conversation earlier this week. Did you have a chance to look into that issue? No rush, just wanted to check in."},
    
    # Meeting / scheduling
    {"subject": "Free this week?", "body": "Hey! Are you free sometime this week for a quick chat? I have a few ideas I'd love to run by you. Even 20 minutes would be great."},
    {"subject": "Coffee chat?", "body": "Hi! It's been a while since we've caught up properly. Would love to grab coffee sometime soon if you're around. Let me know what works!"},
    {"subject": "Meeting rescheduled", "body": "Hey, just a quick note — I need to move our meeting to Thursday if that works for you. Let me know and I'll update the calendar invite."},
    {"subject": "Let's sync soon", "body": "Hi! Been meaning to reach out — would love to sync up sometime this week or next. Lots to catch up on. What does your schedule look like?"},
    {"subject": "Available tomorrow?", "body": "Hey, quick question — are you free tomorrow afternoon? I'd love to go over a few things before the end of the week. Just 15-20 mins should do it."},
    {"subject": "Planning lunch", "body": "Hey team! Thinking about organizing a team lunch next Friday. Nothing fancy, just a chance to get together outside the office. Let me know if you're in!"},
    {"subject": "Drinks after work?", "body": "Hi! A few of us are thinking of heading out for drinks after work on Friday. You should come! It'll be a good chance to unwind. Let me know!"},
    
    # Recommendations / advice
    {"subject": "Tool recommendation?", "body": "Hey, quick question — do you have any recommendations for a good project management tool? We're thinking of switching things up on the team and would love your input."},
    {"subject": "Book recommendation", "body": "Hi! I just finished a really great book on productivity and immediately thought of you. Would love to share — do you want me to send the title over?"},
    {"subject": "You should try this", "body": "Hey! Tried a new way of organizing tasks this week and it's been a game changer. Thought you might find it useful too. I'll share the details — let me know if you're curious!"},
    {"subject": "Podcast rec", "body": "Hi there! Listening to a great podcast lately that I think you'd really enjoy. It's right up your alley. Remind me to share it next time we chat!"},
    
    # Casual / social
    {"subject": "Hope you're well!", "body": "Hey! Just thinking of you and wanted to say hi. Hope everything is going well on your end. Let's catch up soon!"},
    {"subject": "Happy Friday!", "body": "Hi! Hope you have an amazing weekend ahead. You've been working so hard lately — definitely deserve some rest. Talk soon!"},
    {"subject": "Long time no talk!", "body": "Hey! It's been a while — feels like ages since we properly caught up. How have things been? Would love to hear what you've been up to."},
    {"subject": "Thinking of you", "body": "Hi! Was just in a meeting and something came up that reminded me of that project we did together. Good times! Hope all is well with you."},
    {"subject": "Happy Monday!", "body": "Hey! Hope you had a great weekend. Starting the week fresh over here — feeling motivated. How about you? Let's make it a good one!"},
    {"subject": "Midweek check-in", "body": "Hi! Can you believe it's already Wednesday? This week is flying by. Hope yours is going smoothly. Drop me a line if you want to chat!"},
    
    # Feedback / review
    {"subject": "Thoughts on the presentation?", "body": "Hey! I just finished putting together the presentation for next week. Would love a second pair of eyes if you have a few minutes. Let me know!"},
    {"subject": "Quick feedback request", "body": "Hi! Working on something and would love your honest take on it. It's a quick read — do you have 10 mins sometime this week?"},
    {"subject": "Reviewed your doc", "body": "Hey! Just went through the doc you shared yesterday. Really solid work — I left a couple of small notes but overall it's great. Nice job!"},
    {"subject": "What do you think?", "body": "Hi! Curious about your take on what happened in the meeting today. Felt like there was more to discuss. Would love to hear your thoughts over coffee."},
    
    # After vacation / absence
    {"subject": "Back at it!", "body": "Hey! Just got back from vacation and slowly getting back into the swing of things. Hope nothing too crazy happened while I was out 😄 Let's catch up!"},
    {"subject": "Hope you're feeling better", "body": "Hi! Heard you weren't feeling great — hope you're on the mend! Take all the rest you need. Things are under control here, so no worries."},
    {"subject": "Welcome back!", "body": "Hey, welcome back! Hope the trip was amazing. You'll have to fill me in on all the highlights. When you're settled, let's grab lunch!"},
    {"subject": "Miss seeing you around", "body": "Hey! It's been quiet without you around. Hope you're enjoying the break — you definitely earned it. See you when you're back!"},
    
    # Industry / trends
    {"subject": "Interesting article I saw", "body": "Hi! Came across this article about changes in the industry and immediately thought of our conversation last month. I'll forward it — would love your take."},
    {"subject": "Have you heard about this?", "body": "Hey! Have you been following what's been happening in the space lately? Things are moving fast. Would love to pick your brain on it sometime."},
    {"subject": "Big changes coming", "body": "Hi there! Read some interesting news this morning about where the industry is heading. Feels like things are about to shift in a big way. What's your read on it?"},
    {"subject": "Thoughts on the latest trends?", "body": "Hey! Been reading a lot about the latest trends lately and finding it all pretty exciting. Would love to get your perspective — when are you free to chat?"},
    
    # Personal / casual professional
    {"subject": "Congrats!", "body": "Hey! Just heard the news — huge congrats to you! Really well deserved. You've put in so much work and it's great to see it paying off. Let's celebrate!"},
    {"subject": "Quick favor", "body": "Hey! Quick question — would you mind introducing me to someone on your team? I'm working on something they might be able to help with. No pressure at all!"},
    {"subject": "Thanks for your help!", "body": "Hi! Just wanted to say a big thank you for your help last week. It made a real difference. Really appreciate you taking the time. I owe you one!"},
    {"subject": "Appreciate your time", "body": "Hey! Just wanted to follow up and say how much I appreciated your insights during our call. Really gave me a lot to think about. Thanks again!"},
    {"subject": "Loved your idea", "body": "Hi! Still thinking about the idea you mentioned in the meeting yesterday. I think it could really work. Would love to explore it further if you're up for it."},
    
    # Planning / goals
    {"subject": "Q3 planning thoughts", "body": "Hey! As we head into the next quarter, I've been thinking about our goals and wanted to share a few ideas. Would love to align on priorities — are you free this week?"},
    {"subject": "Goals for this month", "body": "Hi! Setting my goals for this month and wanted to check in on yours too. Maybe we can keep each other accountable? Let me know if you're interested!"},
    {"subject": "Planning for next year", "body": "Hey! Hard to believe we're already thinking about next year's plans. I've started putting some ideas together and would love your input. When can we talk?"},
    
    # Short casual ones
    {"subject": "Quick hello", "body": "Hey! Just dropping a quick note to say hello. Hope all is going well. Nothing urgent — just been thinking about reaching out for a while. Chat soon!"},
    {"subject": "Any updates?", "body": "Hi! Any updates on your end? Last we spoke things were in motion — curious to hear how it went. Let me know when you get a chance!"},
    {"subject": "Let me know if you need anything", "body": "Hey! Just wanted to say — if you need anything from me this week, don't hesitate to reach out. Happy to help wherever I can. Hope things are going smoothly!"},
    {"subject": "Checking in", "body": "Hi! Just a quick check-in to see how things are going. It's been a while since we've connected. Would love to catch up whenever you're free!"},
    {"subject": "Hope the week's going well", "body": "Hey! Just wanted to drop a quick line and hope your week is off to a great start. Mine's been busy but good. Let me know if you want to chat!"},
    {"subject": "Great seeing you!", "body": "Hey! It was so great seeing you the other day. We should do it more often! Hope the rest of your week goes well. Talk soon!"},
    {"subject": "Reminder about Friday", "body": "Hi! Just a friendly reminder that we have that call on Friday afternoon. Looking forward to it — I'll have everything prepped by then. See you then!"},
]


def move_spam_to_inbox(acc):
    """Logs into IMAP, finds warmup emails in Spam, moves them to Inbox, and marks as Read."""
    try:
        imap = imaplib.IMAP4_SSL(acc.imap_server, acc.imap_port, timeout=8)
        imap.login(acc.smtp_username, acc.imap_password)
        
        # Try to find and select spam folder
        spam_selected = False
        spam_candidates = ['[Gmail]/Spam', 'Spam', 'Junk', 'Junk Email']
        for folder in spam_candidates:
            try:
                status, _ = imap.select(folder)
                if status == 'OK':
                    spam_selected = True
                    break
            except Exception:
                continue
        
        if spam_selected:
            typ, data = imap.search(None, 'UNSEEN')
            if typ == 'OK' and data[0]:
                for num in data[0].split():
                    try:
                        typ, msg_data = imap.fetch(num, '(RFC822)')
                        if typ == 'OK':
                            raw_email = msg_data[0][1]
                            msg = email.message_from_bytes(raw_email)
                            if msg.get(WARMUP_HEADER) == WARMUP_ID:
                                imap.store(num, '+FLAGS', '\\Seen')
                                imap.copy(num, 'INBOX')
                                imap.store(num, '+FLAGS', '\\Deleted')
                    except Exception:
                        continue
                try:
                    imap.expunge()
                except Exception:
                    pass
            
        # Mark warmup emails in inbox as read
        try:
            status, _ = imap.select('INBOX')
            if status == 'OK':
                typ, data = imap.search(None, 'UNSEEN')
                if typ == 'OK' and data[0]:
                    for num in data[0].split():
                        try:
                            typ, msg_data = imap.fetch(num, '(RFC822.HEADER)')
                            if typ == 'OK':
                                raw_header = msg_data[0][1].decode('utf-8', errors='ignore')
                                if f"{WARMUP_HEADER}: {WARMUP_ID}" in raw_header:
                                    imap.store(num, '+FLAGS', '\\Seen')
                        except Exception:
                            continue
        except Exception:
            pass
            
        imap.logout()
    except Exception as e:
        print(f"IMAP Error for {acc.email}: {e}")


def _get_warmup_message():
    """Returns a random unique warmup message from the large message bank."""
    return random.choice(WARMUP_MESSAGES)


def send_warmup_email(db, sender_acc, all_warmup_accounts):
    """Sends a conversational email from sender to a random target in the network."""
    targets = [a for a in all_warmup_accounts if a.id != sender_acc.id]
    if not targets:
        return

    target_acc = random.choice(targets)
    
    # Pick a random message from the large built-in bank
    msg_data = _get_warmup_message()
    subject = msg_data["subject"]
    body = msg_data["body"]

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
        print(f"Warmup: Sent from {sender_acc.email} to {target_acc.email} | Subject: {subject}")
    except Exception as e:
        print(f"Warmup SMTP Error for {sender_acc.email}: {e}")


def run_warmup_cycle():
    """Main scheduler entrypoint. Runs every 10 minutes, paced over 24 hours.
    Also handles midnight BD reset internally using a file-based tracker.
    This ensures reset works even after process restarts on shared hosting.
    """
    import datetime
    import pytz
    import traceback
    import os

    BD_TZ = pytz.timezone("Asia/Dhaka")
    now_bd = datetime.datetime.now(BD_TZ)
    today_bd_str = now_bd.strftime("%Y-%m-%d")

    # --- Self-resetting: check if a BD-midnight increment is needed ---
    # We track the last reset date in a file to survive process restarts
    reset_flag_path = os.path.join(os.path.dirname(__file__), "tmp", "warmup_last_reset.txt")
    try:
        os.makedirs(os.path.dirname(reset_flag_path), exist_ok=True)
        last_reset_date = ""
        if os.path.exists(reset_flag_path):
            with open(reset_flag_path, "r") as f:
                last_reset_date = f.read().strip()

        if last_reset_date != today_bd_str:
            print(f"[Warmup Auto-Reset] New BD day detected ({today_bd_str}). Running increment...")
            reset_daily_warmup_counts()
            with open(reset_flag_path, "w") as f:
                f.write(today_bd_str)
            print(f"[Warmup Auto-Reset] Reset flag updated to {today_bd_str}.")
    except Exception as e:
        print(f"[Warmup Auto-Reset] Error checking/writing reset flag: {e}")

    print("Running Warmup Cycle...")
    db = database.SessionLocal()
    try:
        accounts = db.query(database.SendingAccount).filter(
            database.SendingAccount.is_active == True,
            database.SendingAccount.warmup_enabled == True
        ).all()
        if not accounts:
            return

        # Pacing: Reset at midnight BD Time.
        now_utc = datetime.datetime.now(pytz.utc)
        last_reset_utc = now_utc.replace(hour=18, minute=0, second=0, microsecond=0)
        if now_utc < last_reset_utc:
            last_reset_utc -= datetime.timedelta(days=1)

        minutes_passed = (now_utc - last_reset_utc).total_seconds() / 60.0
        fraction_of_day = min(1.0, max(0.01, minutes_passed / 1440.0))

        for acc in accounts:
            try:
                # Try IMAP cleanup (non-blocking, skip on error)
                if acc.imap_server and acc.imap_password:
                    move_spam_to_inbox(acc)

                if getattr(acc, "smart_warmup_enabled", False):
                    daily_target = health_monitor.suggest_warmup_limit(acc)
                    if acc.warmup_daily_limit != daily_target:
                        acc.warmup_daily_limit = daily_target
                        db.commit()
                else:
                    daily_target = acc.warmup_daily_limit or 0

                sent_today = acc.warmup_sent_today or 0
                expected_sent_by_now = int(daily_target * fraction_of_day)

                if sent_today < daily_target and sent_today <= expected_sent_by_now:
                    send_warmup_email(db, acc, accounts)
            except Exception as e:
                print(f"Warmup cycle error for {acc.email}: {e}")
                continue
    except Exception as e:
        print(f"Warmup cycle fatal error: {e}\n{traceback.format_exc()}")
    finally:
        db.close()


def reset_daily_warmup_counts():
    """Resets sent counts and applies daily increments for all warmup-enabled accounts."""
    print("Resetting daily warmup counts...")
    db = database.SessionLocal()
    try:
        accounts = db.query(database.SendingAccount).filter(
            database.SendingAccount.warmup_enabled == True
        ).all()
        for acc in accounts:
            acc.warmup_sent_today = 0

            if getattr(acc, "smart_warmup_enabled", False):
                new_limit = health_monitor.suggest_warmup_limit(acc)
                acc.warmup_daily_limit = new_limit
                print(f"  Smart Warmup: {acc.email} -> limit={new_limit}")
            else:
                current_limit = acc.warmup_daily_limit or 0
                increment = acc.warmup_increment_per_day or 0
                new_limit = min(50, current_limit + increment)
                acc.warmup_daily_limit = new_limit
                print(f"  Manual Warmup: {acc.email} -> {current_limit} + {increment} = {new_limit}")

        db.commit()
        print("Warmup reset complete.")
    except Exception as e:
        import traceback
        print(f"Warmup reset error: {e}\n{traceback.format_exc()}")
        db.rollback()
    finally:
        db.close()

