from email_service import send_password_reset_email
import os

print("Testing send_password_reset_email...")
result = send_password_reset_email("mzisan367+test6@gmail.com", "987654")
print(f"Result: {result}")
