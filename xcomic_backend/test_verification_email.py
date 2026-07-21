from email_service import send_verification_email
import os

print("Testing send_verification_email...")
result = send_verification_email("mzisan367+test5@gmail.com", "123456")
print(f"Result: {result}")
