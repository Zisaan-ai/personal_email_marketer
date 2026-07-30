import ftplib

ftp_host = "167.235.11.154"
ftp_user = "terapkco"
ftp_pass = "(3#JCk2Vyn94hY"

local_file = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_index_html.html"

# Fresh download
ftp = ftplib.FTP(ftp_host)
ftp.login(ftp_user, ftp_pass)
ftp.cwd("/xcomic.xyz")
with open(local_file, "wb") as f:
    ftp.retrbinary("RETR index.html", f.write)
ftp.quit()
print("✅ Downloaded fresh")

with open(local_file, "r", encoding="utf-8") as f:
    content = f.read()

# Show lines after 18575
lines = content.split('\n')
print("\n=== Lines 18575-18620 ===")
for i in range(18574, min(18620, len(lines))):
    print(f"{i+1}: {lines[i]}")
