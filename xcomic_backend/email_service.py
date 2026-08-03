import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

from email.utils import formatdate, make_msgid

import os

import base64

from dotenv import load_dotenv

from bs4 import BeautifulSoup

import re

import random

import urllib.parse

import textwrap

import dns.resolver



load_dotenv()



# ============================================================
# SMTP VERIFICATION
# ============================================================

def verify_smtp_credentials(smtp_server: str, smtp_port: int, smtp_user: str, smtp_pass: str) -> dict:
    """Verify SMTP credentials by attempting a real connection and login."""
    import smtplib as _smtplib
    try:
        port = int(smtp_port) if smtp_port else 587
        if port == 465:
            # SSL connection
            with _smtplib.SMTP_SSL(smtp_server, port, timeout=15) as server:
                server.ehlo()
                server.login(smtp_user, smtp_pass)
        else:
            # STARTTLS connection (587, 25, etc.)
            with _smtplib.SMTP(smtp_server, port, timeout=15) as server:
                server.ehlo()
                server.starttls()
                server.login(smtp_user, smtp_pass)
        return {'status': 'success', 'detail': 'Connection and login successful.'}
    except _smtplib.SMTPAuthenticationError as e:
        return {'status': 'error', 'detail': f'Authentication failed: {str(e)}'}
    except _smtplib.SMTPConnectError as e:
        return {'status': 'error', 'detail': f'Cannot connect to SMTP server: {str(e)}'}
    except Exception as e:
        return {'status': 'error', 'detail': f'SMTP error: {str(e)}'}





SMTP_SERVER = os.getenv("SMTP_SERVER") or "smtp.gmail.com"

try:

    SMTP_PORT = int(os.getenv("SMTP_PORT") or 587)

except:

    SMTP_PORT = 587

    

SMTP_USERNAME = os.getenv("SMTP_USERNAME")

if SMTP_USERNAME == "your_email@gmail.com":

    SMTP_USERNAME = ""

SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

if SMTP_PASSWORD == "your_app_password_here":

    SMTP_PASSWORD = ""



# ============================================================

# SPAM TRIGGER WORDS - Comprehensive list from major ESPs

# ============================================================

SPAM_WORDS = [

    "free", "buy now", "guarantee", "risk-free", "winner", "prize",

    "cash", "bonus", "click here", "urgent", "make money", "$$$",

    "investment", "no catch", "hidden", "exclusive deal", "act now",

    "100%", "cheap", "limited time", "order now", "special promotion",

    "congratulations", "you have been selected", "double your",

    "earn extra cash", "no obligation", "no strings attached",

    "offer expires", "once in a lifetime", "take action now",

    "while supplies last", "you are a winner", "claim your",

    "instant access", "no fees", "satisfaction guaranteed",

    "unbelievable", "what are you waiting for", "don't delete",

    "not spam", "this isn't spam", "dear friend", "as seen on",

    "call now", "click below", "direct email", "do it today",

    "don't hesitate", "get it now", "increase your", "info you requested",

    "no questions asked", "remove", "subscribe", "you won't believe"

]



def process_spintax(text: str) -> str:

    pattern = re.compile(r'\{([^{}]*)\}')

    while pattern.search(text):

        match = pattern.search(text)

        options = match.group(1).split('|')

        text = text[:match.start()] + random.choice(options) + text[match.end():]

    return text



# ============================================================

# PERSONALIZATION - Merge tag replacement

# ============================================================

def personalize_content(text: str, lead_name: str = "", lead_company: str = "", sender_name: str = "") -> str:

    """Replace merge tags like {{name}}, {{firstName}}, {{company}} with actual lead data."""

    if not text:

        return text

    

    first_name = lead_name.split()[0] if lead_name and lead_name.strip() else ""

    last_name = lead_name.split()[-1] if lead_name and len(lead_name.split()) > 1 else ""

    

    replacements = {

        "{{name}}": lead_name or "there",

        "{{Name}}": lead_name or "There",

        "{{firstName}}": first_name or "there",

        "{{FirstName}}": first_name.capitalize() if first_name else "There",

        "{{first_name}}": first_name or "there",

        "{{lastName}}": last_name or "",

        "{{last_name}}": last_name or "",

        "{{company}}": lead_company or "your company",

        "{{Company}}": lead_company or "Your Company",

        "{{Your Name}}": sender_name or "",

        "{{your_name}}": sender_name or "",

        "{{Sender Name}}": sender_name or "",

    }

    

    for tag, value in replacements.items():

        text = text.replace(tag, value)

    

    return text





def inject_tracking_pixel(body_html: str, pixel_url: str) -> str:
    pixel_img = f'<img src="{pixel_url}" alt="" width="1" height="1" border="0" style="outline:none;text-decoration:none;" />'
    if "</body>" in body_html.lower():
        # Inject right before closing body tag
        return re.sub(r'(</body>)', lambda m: f'{pixel_img}{m.group(1)}', body_html, flags=re.IGNORECASE)
    else:
        # Just append at the end
        return body_html + pixel_img



def inject_click_tracking(body_html: str, base_tracking_url: str) -> str:

    soup = BeautifulSoup(body_html, "html.parser")

    for a_tag in soup.find_all('a', href=True):

        original_url = a_tag['href']

        if original_url.startswith(('mailto:', 'tel:', '#', 'http://localhost', base_tracking_url.split('/api')[0])):

            continue

        encoded_url = urllib.parse.quote(original_url)

        a_tag['href'] = f"{base_tracking_url}?url={encoded_url}"

    return str(soup)



def inject_unsubscribe(body_html: str, recipient: str) -> str:

    if "unsubscribe" not in body_html.lower():

        base_url = os.getenv("BACKEND_URL", "https://xcomic.xyz")

        token = base64.b64encode(recipient.encode('utf-8')).decode('utf-8')

        unsub_link = f"{base_url}/api/unsubscribe/{token}"

        unsub_html = f'<br><br><hr><p style="font-size:12px; color:#666;">If you no longer wish to receive these emails, you can <a href="{unsub_link}">unsubscribe here</a>.</p>'

        

        if "</body>" in body_html.lower():

            return re.sub(r'(</body>)', f'{unsub_html}\\1', body_html, flags=re.IGNORECASE)

        else:

            return body_html + unsub_html

    return body_html



def _get_unsubscribe_url(recipient: str) -> str:

    """Generate the HTTPS unsubscribe URL for a recipient."""

    base_url = os.getenv("BACKEND_URL", "https://xcomic.xyz")

    token = base64.b64encode(recipient.encode('utf-8')).decode('utf-8')

    return f"{base_url}/api/unsubscribe/{token}"



# ============================================================

# CLEAN PLAIN-TEXT GENERATION

# ============================================================

def generate_clean_plaintext(html: str) -> str:

    """Generate a properly formatted plain-text version from HTML.

    This is critical for deliverability - spam filters compare HTML/text ratio."""

    

    if not html:

        return ""

    

    soup = BeautifulSoup(html, "html.parser")

    

    # Remove script and style tags

    for tag in soup.find_all(['script', 'style', 'head']):

        tag.decompose()

    

    # Replace links with text + URL

    for a_tag in soup.find_all('a', href=True):

        href = a_tag.get('href', '')

        text = a_tag.get_text().strip()

        if href.startswith('mailto:'):

            a_tag.replace_with(text or href.replace('mailto:', ''))

        elif href.startswith('#') or not href:

            a_tag.replace_with(text)

        elif text and text != href:

            a_tag.replace_with(f"{text} ({href})")

        else:

            a_tag.replace_with(href)

    

    # Replace images with alt text

    for img in soup.find_all('img'):

        alt = img.get('alt', '').strip()

        if alt:

            img.replace_with(f"[{alt}]")

        else:

            img.replace_with("")

    

    # Replace <br> with newlines

    for br in soup.find_all('br'):

        br.replace_with('\n')

    

    # Replace <hr> with separator

    for hr in soup.find_all('hr'):

        hr.replace_with('\n' + '-' * 40 + '\n')

    

    # Add newlines around block elements

    block_tags = ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'tr', 'blockquote']

    for tag in soup.find_all(block_tags):

        tag.insert_before('\n')

        tag.insert_after('\n')

    

    # Get the text

    text = soup.get_text()

    

    # Clean up whitespace

    lines = text.split('\n')

    cleaned_lines = []

    prev_blank = False

    for line in lines:

        stripped = line.strip()

        if not stripped:

            if not prev_blank:

                cleaned_lines.append('')

                prev_blank = True

        else:

            # Wrap long lines at 72 characters for readability

            wrapped = textwrap.fill(stripped, width=72)

            cleaned_lines.append(wrapped)

            prev_blank = False

    

    result = '\n'.join(cleaned_lines).strip()

    return result





# ============================================================

# EMAIL VALIDATION (MX CHECK)

# ============================================================

import threading

MX_CACHE = {}

MX_CACHE_LOCK = threading.Lock()



def validate_email_address(email: str) -> dict:

    """Advanced validation: Syntax -> DNS MX -> SMTP Handshake (with fallback for blocked ports)."""

    email = email.strip()

    

    # 1. Syntax Check

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern, email):

        return {'valid': False, 'reason': 'Invalid syntax format'}

    

    domain = email.split('@')[1].lower()

    

    # Check cache first

    with MX_CACHE_LOCK:

        if email in MX_CACHE:

            return MX_CACHE[email]

    

    result = {'valid': True, 'reason': 'OK'}

    mx_host = None

    

    try:

        # 2. DNS/MX Check

        resolver = dns.resolver.Resolver()

        resolver.nameservers = ['8.8.8.8', '1.1.1.1']

        resolver.timeout = 2

        resolver.lifetime = 2

        

        try:

            records = resolver.resolve(domain, 'MX')

            mx_records = sorted(records, key=lambda r: r.preference)

            if not mx_records:

                result = {'valid': False, 'reason': 'Domain has no MX records'}

            else:

                mx_host = str(mx_records[0].exchange).rstrip('.')

        except dns.resolver.NXDOMAIN:

            result = {'valid': False, 'reason': 'Domain does not exist'}

        except dns.resolver.NoAnswer:

            result = {'valid': False, 'reason': 'Domain has no MX records'}

        except Exception as dns_e:

            # DNS lookup failed. On some VPS (like Cloud Hosting BD), this might be blocked.

            # We return valid=True as a fallback so we don't break the app, but note the reason.

            result = {'valid': True, 'reason': f'DNS check bypassed (VPS restriction?)'}

            

        # 3. SMTP Handshake (RCPT TO check)

        if result['valid'] and mx_host:

            try:

                # Set a very short timeout. We don't want to hang the app if port 25 is blocked.

                server = smtplib.SMTP(timeout=3)

                server.connect(mx_host, 25)

                server.ehlo_or_helo_if_needed()

                

                # Check if it's a catch-all domain first to avoid false positives

                catch_all_test = f"random_fake_email_xyz123@{domain}"

                code_catch_all, _ = server.docmd("MAIL FROM:", "<>")

                code_catch_all, _ = server.docmd("RCPT TO:", f"<{catch_all_test}>")

                

                if code_catch_all == 250:

                    # Domain is catch-all, we can't reliably verify mailbox existence

                    result = {'valid': True, 'reason': 'Domain accepts all emails (Catch-all)'}

                else:

                    # Check actual email

                    code, response = server.docmd("MAIL FROM:", "<>")

                    code, response = server.docmd("RCPT TO:", f"<{email}>")

                    

                    if code == 250:

                        result = {'valid': True, 'reason': 'Mailbox exists (SMTP Verified)'}

                    elif code >= 500:

                        resp_text = response.decode('utf-8', errors='ignore').lower() if isinstance(response, bytes) else str(response).lower()

                        

                        # Check if the rejection is specifically about the mailbox not existing

                        not_found_keywords = ['does not exist', 'not found', 'invalid recipient', 'no such user', 'unknown user', 'mailbox unavailable', 'bad address']

                        

                        is_mailbox_error = any(kw in resp_text for kw in not_found_keywords)

                        

                        if is_mailbox_error:

                            result = {'valid': False, 'reason': f'Mailbox does not exist (SMTP Rejected: {resp_text})'}

                        else:

                            # It might be a spam block, IP ban, or greylisting from the receiving server.

                            # We must fallback to True to avoid deleting valid emails.

                            result = {'valid': True, 'reason': f'Server rejected check, assuming valid (Code {code}: {resp_text})'}

                    else:

                        result = {'valid': True, 'reason': f'SMTP Unsure (Code {code})'}

                

                server.quit()

            except Exception as smtp_e:

                # SMTP connection failed (likely port 25 blocked by VPS).

                # Return valid=True as fallback.

                result = {'valid': True, 'reason': 'SMTP check bypassed (Port 25 blocked?)'}

                

    except Exception as e:

        result = {'valid': True, 'reason': f'Validation error bypassed: {e}'}



    with MX_CACHE_LOCK:

        MX_CACHE[email] = result

        

    return result



# ============================================================

# SPAM SCORE CHECKER (enhanced)

# ============================================================

def check_spam_score(subject: str, body: str) -> dict:

    """Enhanced spam score checker with structural analysis."""

    text = (subject + " " + body).lower()

    score = 10.0

    found_words = []

    warnings = []

    

    # Check spam trigger words

    for word in SPAM_WORDS:

        if re.search(r'\b' + re.escape(word) + r'\b', text):

            score -= 0.5

            found_words.append(word)

    

    # Check ALL CAPS words (more than 3 consecutive caps words)

    caps_pattern = re.findall(r'\b[A-Z]{3,}\b', subject + " " + body)

    if len(caps_pattern) > 2:

        score -= 1

        warnings.append(f"Too many ALL CAPS words ({len(caps_pattern)} found)")

    

    # Check exclamation marks

    excl_count = (subject + body).count('!')

    if excl_count > 3:

        score -= 0.5

        warnings.append(f"Too many exclamation marks ({excl_count} found)")

    

    # Check if subject is ALL CAPS

    if subject and subject == subject.upper() and len(subject) > 5:

        score -= 1.5

        warnings.append("Subject line is ALL CAPS")

    

    # Check for too many links

    link_count = len(re.findall(r'https?://', body))

    if link_count > 5:

        score -= 1

        warnings.append(f"Too many links ({link_count} found, keep under 5)")

    

    # Check for missing personalization

    if '{{' not in body and '{{' not in subject:

        score -= 0.5

        warnings.append("No personalization tags found. Use {{name}} or {{company}} for better delivery")

    

    # Check body length (too short = suspicious)

    plain_text = BeautifulSoup(body, "html.parser").get_text().strip() if '<' in body else body.strip()

    if len(plain_text) < 50:

        score -= 1

        warnings.append("Email body too short. Aim for at least 50 characters")

        

    # Check for Base64 embedded images (these trigger spam filters)

    soup = BeautifulSoup(body, 'html.parser')

    base64_images = 0

    for img in soup.find_all('img', src=True):

        if img['src'].startswith('data:image'):

            base64_images += 1

    if base64_images > 0:

        score -= 2

        warnings.append(f"Found {base64_images} base64 embedded images! Please host them externally (e.g. Imgur, AWS) and link to them.")

    

    # Check for missing unsubscribe mention

    if 'unsubscribe' not in body.lower():

        warnings.append("No unsubscribe link detected (will be auto-added)")

    

    score = max(0, min(10, round(score, 1)))

    

    return {

        "score": score,

        "found_words": found_words,

        "warnings": warnings,

        "rating": "Excellent" if score >= 9 else "Good" if score >= 7 else "Fair" if score >= 5 else "Poor"

    }





# ============================================================

# MAIN SEND FUNCTION - with full deliverability headers

# ============================================================

def send_single_email(subject: str, body_html: str, recipient: str, account=None, lead_name: str = "", lead_company: str = "", use_unsubscribe: bool = True) -> bool:

    if not account:

        print("No sending account provided.")

        return False



    active_server = account.smtp_server

    active_port = account.smtp_port

    active_user = account.smtp_username

    active_pass = account.smtp_password



    if not active_pass:

        print("SMTP Password not configured.")

        return False



    # FIX: If body_html is plain text, convert newlines to <br> so it renders correctly in Inbox

    if '<html' not in body_html.lower() and '<p>' not in body_html.lower() and '<br' not in body_html.lower() and '<div' not in body_html.lower():

        body_html = body_html.replace('\n', '<br>')



    # DELIVERABILITY FIX: Personalize content with merge tags

    

    sender_name = getattr(account, 'name', '') if account else ''
    body_html = personalize_content(body_html, lead_name, lead_company, sender_name)

    subject = personalize_content(subject, lead_name, lead_company, sender_name)



    # Inject unsubscribe link in body if enabled

    if use_unsubscribe:

        body_html = inject_unsubscribe(body_html, recipient)



    # Generate clean plain-text (CRITICAL for spam filters)

    body_text = generate_clean_plaintext(body_html)



    # Apply spintax

    spun_subject = process_spintax(subject)

    spun_html = process_spintax(body_html)

    spun_text = process_spintax(body_text)



    # Generate unsubscribe URL for headers

    unsub_url = _get_unsubscribe_url(recipient)



    



    try:

        # Brevo API

        if active_pass.startswith("xkeysib-"):

            import requests

            headers = {

                "accept": "application/json",

                "api-key": active_pass,

                "content-type": "application/json"

            }

            payload = {

                "sender": {"name": sender_name or getattr(account, 'email', active_user), "email": getattr(account, 'email', active_user)},

                "to": [{"email": recipient, "name": lead_name or recipient.split('@')[0]}],

                "subject": spun_subject,

                "htmlContent": spun_html,

                "textContent": spun_text

            }

            if use_unsubscribe:
                unsub_em = getattr(account, 'email', None) or active_user
                unsub_dom = unsub_em.split('@')[-1] if '@' in unsub_em else 'xcomic.xyz'
                unsub_mailto = f"mailto:unsubscribe@{unsub_dom}?subject=unsubscribe"
                payload["headers"] = {
                    "List-Unsubscribe": f"<{unsub_mailto}>, <{unsub_url}>",
                    "List-Unsubscribe-Post": "List-Unsubscribe=One-Click"
                }

            resp = requests.post("https://api.brevo.com/v3/smtp/email", headers=headers, json=payload, timeout=20)

            if resp.status_code in [200, 201, 202]:

                return True

            else:

                print(f"Brevo API error: {resp.text}")

                return False



        # Regular SMTP
        else:
            import smtplib
            import email.utils
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            sender_em = getattr(account, 'email', None) or active_user
            domain = sender_em.split('@')[-1] if '@' in sender_em else 'xcomic.xyz'

            msg = MIMEMultipart('alternative')
            msg['Subject'] = spun_subject
            msg['From'] = f"{sender_name} <{sender_em}>" if sender_name else sender_em
            msg['To'] = recipient
            msg['Reply-To'] = sender_em
            msg['Date'] = email.utils.formatdate(localtime=True)
            msg['Message-ID'] = email.utils.make_msgid(domain=domain)
            msg['MIME-Version'] = '1.0'

            if use_unsubscribe:
                unsub_mailto = f"mailto:unsubscribe@{domain}?subject=unsubscribe"
                msg.add_header('List-Unsubscribe', f"<{unsub_mailto}>, <{unsub_url}>")
                msg.add_header('List-Unsubscribe-Post', 'List-Unsubscribe=One-Click')

            msg.attach(MIMEText(spun_text, 'plain', 'utf-8'))
            msg.attach(MIMEText(spun_html, 'html', 'utf-8'))

            # BUG 5 FIX: Use SMTP_SSL for port 465, regular SMTP+STARTTLS for 587/other
            port = int(active_port) if active_port else 587
            if port == 465:
                with smtplib.SMTP_SSL(active_server, port, timeout=20) as server:
                    server.ehlo()
                    server.login(active_user, active_pass)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(active_server, port, timeout=20) as server:
                    server.ehlo()
                    server.starttls()
                    server.login(active_user, active_pass)
                    server.send_message(msg)

            return True



    except Exception as e:

        print(f"Error sending email: {str(e)}")

        return False



# ============================================================
# SYSTEM EMAILS (Verification, Password Reset)
# ============================================================

def _get_system_smtp_config():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    env_dict = {}
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    env_dict[k.strip()] = v.strip()
    return env_dict

def _send_system_email(recipient: str, subject: str, body_html: str) -> bool:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    config = _get_system_smtp_config()
    server = config.get("SMTP_SERVER")
    port = config.get("SMTP_PORT", "587")
    user = config.get("SMTP_USERNAME")
    password = config.get("SMTP_PASSWORD")
    from_name = config.get("SMTP_FROM_NAME", "System Admin")
    from_email = config.get("SMTP_FROM_EMAIL", "support@xcomic.xyz")
    
    if not server or not user or not password:
        print("System SMTP not configured properly.")
        return False
        
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = f"{from_name} <{from_email}>"
    msg['To'] = recipient
    msg.attach(MIMEText(body_html, "html"))
    
    try:
        with smtplib.SMTP(server, int(port), timeout=15) as s:
            s.ehlo()
            s.starttls()
            s.login(user, password)
            s.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send system email: {e}")
        return False

def send_verification_email(email: str, code: str) -> bool:
    subject = "Verify your XComic account"
    body = """<!DOCTYPE html>
<html>
<head>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f9fafb; margin: 0; padding: 0; }
  .container { max-width: 500px; margin: 40px auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border: 1px solid #f3f4f6; }
  .header { background: #0f172a; padding: 24px; text-align: center; }
  .content { padding: 32px; color: #374151; line-height: 1.6; font-size: 15px; }
  .h1 { font-size: 20px; font-weight: 600; color: #111827; margin-bottom: 16px; margin-top: 0; }
  .code-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; text-align: center; margin: 24px 0; }
  .code { font-size: 32px; font-weight: 700; color: #4f46e5; letter-spacing: 6px; margin: 0; }
  .footer { background: #f8fafc; padding: 24px; text-align: center; border-top: 1px solid #f1f5f9; }
  .signature { font-size: 14px; font-weight: 700; color: #334155; margin-bottom: 4px; }
  .copyright { font-size: 12px; color: #94a3b8; margin: 0; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div style="color: #ffffff; font-size: 24px; font-weight: 800; letter-spacing: 1px;">XComic</div>
  </div>
  <div class="content">
    <h1 class="h1">Verify your email address</h1>
    <p style="margin-top: 0;">Hi there,</p>
    <p>Thanks for getting started with XComic! To complete your sign up, please enter the following verification code in your browser:</p>
    
    <div class="code-box">
      <p class="code">_CODE_</p>
    </div>
    
    <p style="margin-bottom: 0;">If you didn't attempt to sign up for XComic, you can safely ignore this email.</p>
  </div>
  <div class="footer">
    <div class="signature">The XComic Team</div>
    <p class="copyright">&copy; 2026 XComic. All rights reserved.</p>
  </div>
</div>
</body>
</html>""".replace("_CODE_", code)
    return _send_system_email(email, subject, body)

def send_password_reset_email(email: str, code: str) -> bool:
    subject = "Reset your XComic password"
    body = """<!DOCTYPE html>
<html>
<head>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f9fafb; margin: 0; padding: 0; }
  .container { max-width: 500px; margin: 40px auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border: 1px solid #f3f4f6; }
  .header { background: #0f172a; padding: 24px; text-align: center; }
  .content { padding: 32px; color: #374151; line-height: 1.6; font-size: 15px; }
  .h1 { font-size: 20px; font-weight: 600; color: #111827; margin-bottom: 16px; margin-top: 0; }
  .code-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; text-align: center; margin: 24px 0; }
  .code { font-size: 32px; font-weight: 700; color: #4f46e5; letter-spacing: 6px; margin: 0; }
  .footer { background: #f8fafc; padding: 24px; text-align: center; border-top: 1px solid #f1f5f9; }
  .signature { font-size: 14px; font-weight: 700; color: #334155; margin-bottom: 4px; }
  .copyright { font-size: 12px; color: #94a3b8; margin: 0; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div style="color: #ffffff; font-size: 24px; font-weight: 800; letter-spacing: 1px;">XComic</div>
  </div>
  <div class="content">
    <h1 class="h1">Reset your password</h1>
    <p style="margin-top: 0;">Hi there,</p>
    <p>We received a request to reset the password for your XComic account. Enter the following code to securely reset your password:</p>
    
    <div class="code-box">
      <p class="code">_CODE_</p>
    </div>
    
    <p style="margin-bottom: 0;">If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.</p>
  </div>
  <div class="footer">
    <div class="signature">The XComic Team</div>
    <p class="copyright">&copy; 2026 XComic. All rights reserved.</p>
  </div>
</div>
</body>
</html>""".replace("_CODE_", code)
    return _send_system_email(email, subject, body)
