import os
import shutil

def cleanup_workspace():
    print("==================================================")
    print(" CLEANING UP ALL OLD AND UNUSED CODE ")
    print("==================================================")
    
    # 1. The ide scripts and old_chat_recovery folder
    ide_dir = r"C:\Users\higan\.antigravity-ide\personal_email_marketer"
    if os.path.exists(ide_dir):
        try:
            shutil.rmtree(ide_dir)
            print(f"DELETED: {ide_dir}")
        except Exception as e:
            print(f"Failed to delete {ide_dir}: {e}")
            
    # 2. The 6:02 AM folder
    gemini_dir = r"C:\Users\higan\.gemini\antigravity\personal_email_marketer"
    if os.path.exists(gemini_dir):
        try:
            shutil.rmtree(gemini_dir)
            print(f"DELETED: {gemini_dir}")
        except Exception as e:
            print(f"Failed to delete {gemini_dir}: {e}")
            
    # 3. Scratch folder loose files
    scratch_dir = r"C:\Users\higan\.gemini\antigravity\scratch"
    loose_files = ["index.html", "app.js", "style.css", "main.py", "app_live.js", "app_edit5.js"]
    for f in loose_files:
        p = os.path.join(scratch_dir, f)
        if os.path.exists(p):
            try:
                os.remove(p)
                print(f"DELETED: {p}")
            except Exception as e:
                pass
                
    # 4. Check if github_sync is safe
    sync_dir = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync"
    if os.path.exists(sync_dir):
        print("\nSUCCESS! Only the clean github_sync folder remains.")
    else:
        print("\nWARNING: github_sync folder is missing?!")

if __name__ == "__main__":
    cleanup_workspace()
