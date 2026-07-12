with open('backend/email_service.py', encoding='utf-8') as f:
    text = f.read()

orig = '''def validate_email_address(email: str) -> dict:
    """Validate email format and MX record before sending."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return {'valid': False, 'reason': 'Invalid format'}
    
    domain = email.split('@')[1]
    try:
        # Check MX record to ensure domain can receive email
        records = dns.resolver.resolve(domain, 'MX')
        if not records:
            return {'valid': False, 'reason': 'No MX record found'}
    except Exception:
        return {'valid': False, 'reason': 'No MX record - domain cannot receive email'}
    
    return {'valid': True, 'reason': 'OK'}'''

new_val = '''MX_CACHE = {}

def validate_email_address(email: str) -> dict:
    """Validate email format and MX record before sending."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return {'valid': False, 'reason': 'Invalid format'}
    
    domain = email.split('@')[1].lower()
    
    if domain in MX_CACHE:
        if not MX_CACHE[domain]:
            return {'valid': False, 'reason': 'No MX record - domain cannot receive email'}
        return {'valid': True, 'reason': 'OK'}
        
    try:
        # Check MX record to ensure domain can receive email
        records = dns.resolver.resolve(domain, 'MX')
        if not records:
            MX_CACHE[domain] = False
            return {'valid': False, 'reason': 'No MX record found'}
        MX_CACHE[domain] = True
    except Exception:
        MX_CACHE[domain] = False
        return {'valid': False, 'reason': 'No MX record - domain cannot receive email'}
    
    return {'valid': True, 'reason': 'OK'}'''

text = text.replace(orig, new_val)

with open('backend/email_service.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated email_service MX cache")
