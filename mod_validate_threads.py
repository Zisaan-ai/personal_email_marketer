with open('backend/main.py', encoding='utf-8') as f:
    text = f.read()

orig_validate = '''    for email in emails_to_check:
        if email in inactive_emails:
            results.append({"email": email, "valid": False, "reason": "Inactive Lead (No open > 90 days)"})
            continue
            
        val = email_service.validate_email_address(email)
        results.append({
            "email": email,
            "valid": val["valid"],
            "reason": val.get("reason", "")
        })
    return {"results": results}'''

new_validate = '''    import concurrent.futures
    
    def check_single(email):
        if email in inactive_emails:
            return {"email": email, "valid": False, "reason": "Inactive Lead (No open > 90 days)"}
        val = email_service.validate_email_address(email)
        return {
            "email": email,
            "valid": val["valid"],
            "reason": val.get("reason", "")
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(check_single, emails_to_check))
        
    return {"results": results}'''

if orig_validate in text:
    text = text.replace(orig_validate, new_validate)
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated validate_leads to multithreading.")
else:
    print("Could not find orig_validate block!")
