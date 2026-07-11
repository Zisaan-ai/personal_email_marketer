"""
Domain Intelligence Engine
===========================
Checks domain health for email deliverability: SPF, DKIM, DMARC, Blacklists, Catch-all detection.

Used by:
- Domain Health Dashboard (frontend)
- Scheduled periodic audits
- Pre-send checks
"""

import dns.resolver
import smtplib
import socket
from datetime import datetime
import database


# ============================================================
# SPF CHECK
# ============================================================
def check_spf(domain: str) -> dict:
    """Check if domain has a valid SPF record."""
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            txt = rdata.to_text().strip('"')
            if txt.startswith('v=spf1'):
                return {"has_spf": True, "record": txt}
        return {"has_spf": False, "record": None}
    except Exception:
        return {"has_spf": False, "record": None}


# ============================================================
# DKIM CHECK
# ============================================================
def check_dkim(domain: str, selector: str = "google") -> dict:
    """
    Check if domain has a DKIM record.
    Common selectors: google, default, selector1, selector2, dkim, mail
    """
    selectors_to_try = [selector, "google", "default", "selector1", "selector2", "dkim", "s1", "k1"]
    
    for sel in selectors_to_try:
        try:
            dkim_domain = f"{sel}._domainkey.{domain}"
            answers = dns.resolver.resolve(dkim_domain, 'TXT')
            for rdata in answers:
                txt = rdata.to_text().strip('"')
                if 'v=DKIM1' in txt or 'p=' in txt:
                    return {"has_dkim": True, "selector": sel, "record": txt[:100]}
        except Exception:
            continue

    return {"has_dkim": False, "selector": None, "record": None}


# ============================================================
# DMARC CHECK
# ============================================================
def check_dmarc(domain: str) -> dict:
    """Check if domain has a DMARC record."""
    try:
        dmarc_domain = f"_dmarc.{domain}"
        answers = dns.resolver.resolve(dmarc_domain, 'TXT')
        for rdata in answers:
            txt = rdata.to_text().strip('"')
            if txt.startswith('v=DMARC1'):
                return {"has_dmarc": True, "record": txt}
        return {"has_dmarc": False, "record": None}
    except Exception:
        return {"has_dmarc": False, "record": None}


# ============================================================
# BLACKLIST CHECK
# ============================================================
def check_blacklists(domain: str) -> dict:
    """
    Check if domain/IP is on known email blacklists.
    Uses DNS-based blacklist (DNSBL) lookups.
    """
    blacklists = [
        ("zen.spamhaus.org", "Spamhaus"),
        ("b.barracudacentral.org", "Barracuda"),
        ("bl.spamcop.net", "SpamCop"),
        ("dnsbl.sorbs.net", "SORBS"),
    ]

    listed_on = []

    # First resolve domain to IP
    try:
        ip_answers = dns.resolver.resolve(domain, 'A')
        ip = str(ip_answers[0])
    except Exception:
        # If domain doesn't resolve to IP, skip IP-based checks
        return {"is_blacklisted": False, "details": [], "checked": len(blacklists)}

    # Reverse the IP for DNSBL lookup
    reversed_ip = '.'.join(reversed(ip.split('.')))

    for bl_domain, bl_name in blacklists:
        try:
            lookup = f"{reversed_ip}.{bl_domain}"
            dns.resolver.resolve(lookup, 'A')
            # If we get a response, the IP is listed
            listed_on.append(bl_name)
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            pass  # Not listed — this is good
        except Exception:
            pass

    return {
        "is_blacklisted": len(listed_on) > 0,
        "details": listed_on,
        "checked": len(blacklists)
    }


# ============================================================
# CATCH-ALL DETECTION
# ============================================================
def detect_catch_all(domain: str) -> dict:
    """
    Detect if a domain is a catch-all (accepts all email addresses).
    Sends an SMTP RCPT TO for a random non-existent address.
    """
    import random
    import string

    random_user = ''.join(random.choices(string.ascii_lowercase, k=20))
    test_email = f"{random_user}@{domain}"

    try:
        # Get MX record
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_host = str(sorted(mx_records, key=lambda r: r.preference)[0].exchange).rstrip('.')
    except Exception:
        return {"is_catch_all": False, "reason": "Could not resolve MX record"}

    try:
        server = smtplib.SMTP(mx_host, 25, timeout=10)
        server.ehlo('test.com')
        
        # Try RCPT TO with random address
        server.mail('test@test.com')
        code, _ = server.rcpt(test_email)
        server.quit()

        # 250 = accepted (catch-all), 550/551/552/553 = rejected (not catch-all)
        if code == 250:
            return {"is_catch_all": True, "reason": "Domain accepts all email addresses"}
        else:
            return {"is_catch_all": False, "reason": "Domain properly rejects invalid addresses"}
    except smtplib.SMTPServerDisconnected:
        return {"is_catch_all": False, "reason": "SMTP connection closed"}
    except Exception as e:
        return {"is_catch_all": False, "reason": f"Could not determine: {str(e)[:100]}"}


# ============================================================
# FULL DOMAIN AUDIT
# ============================================================
def full_domain_audit(domain: str) -> dict:
    """Run a complete domain health audit (SPF + DKIM + DMARC + Blacklist + Catch-all)."""
    spf = check_spf(domain)
    dkim = check_dkim(domain)
    dmarc = check_dmarc(domain)
    blacklist = check_blacklists(domain)
    catch_all = detect_catch_all(domain)

    # Calculate overall domain score
    score = 0
    max_score = 5
    if spf["has_spf"]:
        score += 1
    if dkim["has_dkim"]:
        score += 1
    if dmarc["has_dmarc"]:
        score += 1
    if not blacklist["is_blacklisted"]:
        score += 1
    if not catch_all["is_catch_all"]:
        score += 1

    # Recommendations
    recommendations = []
    if not spf["has_spf"]:
        recommendations.append("Add SPF record to your DNS. Example: v=spf1 include:_spf.google.com ~all")
    if not dkim["has_dkim"]:
        recommendations.append("Enable DKIM signing for your domain. Check your email provider's documentation.")
    if not dmarc["has_dmarc"]:
        recommendations.append("Add DMARC record. Example: v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com")
    if blacklist["is_blacklisted"]:
        recommendations.append(f"Your domain IP is blacklisted on: {', '.join(blacklist['details'])}. Request delisting.")
    if catch_all["is_catch_all"]:
        recommendations.append("Domain is a catch-all. Consider disabling to reduce bounce risk.")

    return {
        "domain": domain,
        "score": score,
        "max_score": max_score,
        "score_label": f"{score}/{max_score}",
        "spf": spf,
        "dkim": dkim,
        "dmarc": dmarc,
        "blacklist": blacklist,
        "catch_all": catch_all,
        "recommendations": recommendations,
        "checked_at": datetime.utcnow().isoformat()
    }


# ============================================================
# CACHE DOMAIN HEALTH IN DB
# ============================================================
def cache_domain_health(db, domain: str, audit_result: dict):
    """Save domain health audit result to database cache."""
    existing = db.query(database.DomainHealthCache).filter(
        database.DomainHealthCache.domain == domain
    ).first()

    if existing:
        existing.has_spf = audit_result["spf"]["has_spf"]
        existing.has_dkim = audit_result["dkim"]["has_dkim"]
        existing.has_dmarc = audit_result["dmarc"]["has_dmarc"]
        existing.spf_record = audit_result["spf"].get("record")
        existing.dmarc_record = audit_result["dmarc"].get("record")
        existing.is_blacklisted = audit_result["blacklist"]["is_blacklisted"]
        existing.blacklist_details = ','.join(audit_result["blacklist"]["details"]) if audit_result["blacklist"]["details"] else None
        existing.is_catch_all = audit_result["catch_all"]["is_catch_all"]
        existing.last_checked = datetime.utcnow()
    else:
        cache = database.DomainHealthCache(
            domain=domain,
            has_spf=audit_result["spf"]["has_spf"],
            has_dkim=audit_result["dkim"]["has_dkim"],
            has_dmarc=audit_result["dmarc"]["has_dmarc"],
            spf_record=audit_result["spf"].get("record"),
            dmarc_record=audit_result["dmarc"].get("record"),
            is_blacklisted=audit_result["blacklist"]["is_blacklisted"],
            blacklist_details=','.join(audit_result["blacklist"]["details"]) if audit_result["blacklist"]["details"] else None,
            is_catch_all=audit_result["catch_all"]["is_catch_all"],
        )
        db.add(cache)

    db.commit()


# ============================================================
# SCHEDULED DOMAIN HEALTH CHECK
# ============================================================
def run_domain_health_check():
    """Scheduled job — checks domain health for all sending accounts."""
    print("[Domain Checker] Starting domain health check...")
    db = database.SessionLocal()
    try:
        accounts = db.query(database.SendingAccount).filter(
            database.SendingAccount.is_active == True
        ).all()

        # Collect unique domains
        domains = set()
        for acc in accounts:
            if '@' in acc.email:
                domain = acc.email.split('@')[1]
                domains.add(domain)

        checked = 0
        for domain in domains:
            try:
                result = full_domain_audit(domain)
                cache_domain_health(db, domain, result)
                checked += 1
                print(f"[Domain Checker] {domain}: {result['score_label']}")
            except Exception as e:
                print(f"[Domain Checker] Error checking {domain}: {e}")

        print(f"[Domain Checker] Completed. {checked}/{len(domains)} domains checked.")
    except Exception as e:
        print(f"[Domain Checker] Error: {e}")
    finally:
        db.close()
