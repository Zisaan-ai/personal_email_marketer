import os
import ftplib
import time

def deploy():
    print("=========================================")
    print("🚀 Auto-Deploying Fixes to cPanel Server")
    print("=========================================")
    
    # FTP Credentials from screenshot
    ftp_host = "167.235.11.154"
    ftp_user = "terapkco"
    ftp_pass = "(3#JCk2Vyn94hY"
    
    # Local Files
    local_main_py = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\xcomic_backend\main.py"
    local_db_py = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\xcomic_backend\database.py"
    local_app_js = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\xcomic.xyz\assets\app.js"
    
    # Check if local files exist
    if not os.path.exists(local_main_py):
        print(f"❌ Error: Could not find {local_main_py}")
        return
    if not os.path.exists(local_db_py):
        print(f"❌ Error: Could not find {local_db_py}")
        return
    if not os.path.exists(local_app_js):
        print(f"❌ Error: Could not find {local_app_js}")
        return

    try:
        print("\n⏳ Connecting to FTP server...")
        ftp = ftplib.FTP(ftp_host)
        ftp.login(ftp_user, ftp_pass)
        print("✅ Connected successfully!")
        
        # 1. Upload main.py to xcomic_backend
        print("\n📤 Uploading files to /xcomic_backend/ ...")
        ftp.cwd("/xcomic_backend")
        with open(local_main_py, "rb") as f:
            ftp.storbinary("STOR main.py", f)
        print("✅ main.py uploaded successfully!")
        
        with open(local_db_py, "rb") as f:
            ftp.storbinary("STOR database.py", f)
        print("✅ database.py uploaded successfully!")
        
        # 2. Touch tmp/restart.txt to restart Python app
        print("\n🔄 Restarting Python Backend Server...")
        try:
            ftp.cwd("/xcomic_backend/tmp")
            # Create a temporary local file to upload
            with open("temp_restart.txt", "w") as f:
                f.write(str(time.time()))
            with open("temp_restart.txt", "rb") as f:
                ftp.storbinary("STOR restart.txt", f)
            os.remove("temp_restart.txt")
            print("✅ Backend server restarted successfully (restart.txt updated)!")
        except Exception as e:
            print(f"⚠️ Could not automatically restart via tmp/restart.txt: {e}")
            print("   You may need to click 'Restart' manually in cPanel Setup Python App.")
            
        # 3. Upload app.js to xcomic.xyz/assets/
        print("\n📤 Uploading app.js to public_html or xcomic.xyz ...")
        # Try finding the correct public folder
        ftp.cwd("/")
        folders = ftp.nlst()
        public_dir = ""
        if "xcomic.xyz" in folders:
            public_dir = "/xcomic.xyz/assets"
        elif "public_html" in folders:
            # Let's check if it's inside public_html
            ftp.cwd("/public_html")
            subfolders = ftp.nlst()
            if "assets" in subfolders:
                public_dir = "/public_html/assets"
            elif "xcomic.xyz" in subfolders:
                public_dir = "/public_html/xcomic.xyz/assets"
                
        if public_dir:
            try:
                ftp.cwd(public_dir)
                with open(local_app_js, "rb") as f:
                    ftp.storbinary("STOR app.js", f)
                print(f"✅ app.js uploaded successfully to {public_dir}!")
            except Exception as e:
                print(f"❌ Failed to upload app.js to {public_dir}: {e}")
        else:
            print("⚠️ Could not automatically locate the assets folder for app.js.")
            print("   You may need to upload app.js manually via cPanel File Manager.")

        ftp.quit()
        print("\n🎉 ALL DONE! The system has been fully updated.")
        print("👉 Press Ctrl + F5 on your website and try saving the API key now!")
        
    except Exception as e:
        print(f"\n❌ FTP Connection/Upload Error: {e}")

if __name__ == "__main__":
    deploy()
