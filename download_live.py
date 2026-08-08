import ftplib
import os

FTP_HOST = "terapk.com"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"
FTP_FRONTEND_REMOTE = "/xcomic.xyz"

print("Connecting to FTP...")
ftp = ftplib.FTP(timeout=60)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)

def download_file(remote, local):
    try:
        with open(local, 'wb') as f:
            ftp.retrbinary('RETR ' + remote, f.write)
        print(f"Downloaded {remote} to {local}")
    except Exception as e:
        print(f"Failed to download {remote}: {e}")

ftp.cwd(FTP_FRONTEND_REMOTE)
download_file('index.html', 'xcomic.xyz/index.html')
download_file('auth.html', 'xcomic.xyz/auth.html')

ftp.cwd('assets')
download_file('app.js', 'xcomic.xyz/assets/app.js')
download_file('style.css', 'xcomic.xyz/assets/style.css')
download_file('support_patch.js', 'xcomic.xyz/assets/support_patch.js')
download_file('ai_features.js', 'xcomic.xyz/assets/ai_features.js')
download_file('deliverability_v2.js', 'xcomic.xyz/assets/deliverability_v2.js')
download_file('sending_accounts.js', 'xcomic.xyz/assets/sending_accounts.js')
download_file('templates.js', 'xcomic.xyz/assets/templates.js')

ftp.quit()
print("Download complete.")
