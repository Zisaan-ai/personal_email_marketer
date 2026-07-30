import os
import subprocess

def force_cleanup():
    print("==================================================")
    print(" FORCE CLEANING READ-ONLY GIT FOLDERS ")
    print("==================================================")
    
    folders_to_delete = [
        r"C:\Users\higan\.antigravity-ide\personal_email_marketer",
        r"C:\Users\higan\.gemini\antigravity\personal_email_marketer"
    ]
    
    for folder in folders_to_delete:
        if os.path.exists(folder):
            try:
                print(f"Force deleting: {folder} ...")
                # Windows command to silently and forcefully delete a directory
                subprocess.run(["cmd.exe", "/c", "rmdir", "/s", "/q", folder], check=True)
                print(f"  -> Successfully deleted!")
            except Exception as e:
                print(f"  -> Failed: {e}")
                
    print("\nDONE! All old versions are completely removed from your PC.")

if __name__ == "__main__":
    force_cleanup()
