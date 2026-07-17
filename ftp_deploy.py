import ftplib
import io
import os

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

try:
    print("Connecting to FTP...")
    ftp = ftplib.FTP(host, user, password, timeout=10)
    print("Connected.")
    
    print("Navigating to xcomic_backend...")
    ftp.cwd('xcomic_backend')
    
    # Upload health_monitor.py
    with open(r"C:\Users\higan\.gemini\antigravity\scratch\xcomic_sync\xcomic_backend\health_monitor.py", 'rb') as f:
        print("Uploading health_monitor.py...")
        ftp.storbinary('STOR health_monitor.py', f)
        
    # Upload database.py
    with open(r"C:\Users\higan\.gemini\antigravity\scratch\xcomic_sync\xcomic_backend\database.py", 'rb') as f:
        print("Uploading database.py...")
        ftp.storbinary('STOR database.py', f)
        
    # Ensure tmp directory exists
    directories = []
    ftp.retrlines('NLST', directories.append)
    if 'tmp' not in directories:
        print("Creating tmp directory...")
        ftp.mkd('tmp')
        
    print("Navigating to tmp...")
    ftp.cwd('tmp')
    
    print("Creating/updating restart.txt...")
    bio = io.BytesIO(b"Restart app\n")
    ftp.storbinary('STOR restart.txt', bio)
    print("Done! Application restarted.")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    try:
        ftp.quit()
        print("Disconnected.")
    except:
        pass
