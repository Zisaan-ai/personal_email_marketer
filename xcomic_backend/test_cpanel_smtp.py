import smtplib

server = "xcomic.xyz"  # or mail.xcomic.xyz
port = 465 # or 587
user = "support@xcomic.xyz"
password = "(3#JCk2Vyn94hY"

try:
    print("Connecting with SSL to 465...")
    smtp = smtplib.SMTP_SSL(server, port, timeout=10)
    print("Logging in...")
    smtp.login(user, password)
    print("Success on 465!")
    smtp.quit()
except Exception as e:
    print(f"Failed on 465 SSL: {e}")

try:
    print("Connecting with TLS to 587...")
    smtp = smtplib.SMTP(server, 587, timeout=10)
    smtp.starttls()
    print("Logging in...")
    smtp.login(user, password)
    print("Success on 587!")
    smtp.quit()
except Exception as e:
    print(f"Failed on 587 TLS: {e}")
