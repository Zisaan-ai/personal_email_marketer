import ftplib
import os

ftp_host = "167.235.11.154"
ftp_user = "terapkco"
ftp_pass = "(3#JCk2Vyn94hY"

local_file = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_app_js.js"

try:
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)
    ftp.cwd("/xcomic.xyz/assets")
    
    with open(local_file, "wb") as f:
        ftp.retrbinary("RETR app.js", f.write)
    print(f"Downloaded app.js to {local_file}")
    
    ftp.quit()
    
    # Now search for timezone related code
    with open(local_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    print(f"\nTotal lines: {len(lines)}")
    print("\n=== Lines containing 'timezone' (case insensitive) ===")
    for i, line in enumerate(lines):
        if 'timezone' in line.lower() or 'Timezone' in line:
            print(f"  Line {i+1}: {line.rstrip()[:120]}")
            
except Exception as e:
    print(f"Error: {e}")
