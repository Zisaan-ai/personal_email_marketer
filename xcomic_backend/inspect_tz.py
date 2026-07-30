import ftplib
import re

ftp_host = "167.235.11.154"
ftp_user = "terapkco"
ftp_pass = "(3#JCk2Vyn94hY"

local_file = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_index_html.html"

# Re-download fresh index.html from server
ftp = ftplib.FTP(ftp_host)
ftp.login(ftp_user, ftp_pass)
ftp.cwd("/xcomic.xyz")
with open(local_file, "wb") as f:
    ftp.retrbinary("RETR index.html", f.write)
ftp.quit()
print("✅ Downloaded fresh index.html")

with open(local_file, "r", encoding="utf-8") as f:
    content = f.read()

# Show exact lines around user-timezone to understand current state
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'user-timezone' in line or 'tz-search' in line or 'tz-dropdown' in line:
        start = max(0, i-2)
        end = min(len(lines), i+3)
        for j in range(start, end):
            marker = ">>>" if j == i else "   "
            print(f"{marker} {j+1}: {lines[j][:180]}")
        print("---")

# Find the entire timezone configuration card/block
for i, line in enumerate(lines):
    if 'Timezone Configuration' in line:
        # Show a big chunk around it
        start = max(0, i-3)
        end = min(len(lines), i+40)
        print(f"\n=== TIMEZONE CONFIG BLOCK (lines {start+1}-{end}) ===")
        for j in range(start, end):
            print(f"  {j+1}: {lines[j][:200]}")
        break
