import os
import sys
import ftplib
import time
import argparse
import subprocess
from dotenv import load_dotenv

# Ensure terminal uses UTF-8 to avoid encoding errors on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Setup base directories
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT_DIR, "xcomic.xyz")
BACKEND_DIR = os.path.join(ROOT_DIR, "xcomic_backend")

# FTP Configurations
FTP_HOST = "terapk.com"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"
FTP_FRONTEND_REMOTE = "/xcomic.xyz"
FTP_BACKEND_REMOTE = "/xcomic_backend"

# Excluded patterns for backend FTP uploads
EXCLUDE_LIST = [
    ".git", ".gitignore", ".env", "wsgi_debug.log", "fastapi_error.log",
    "fastapi_errors.log", "stderr.log", "stderr_new.log", "stderr_again.log",
    "stderr_fastapi.log", "stderr_fastapi2.log", "stderr_final.log",
    "stderr_hanging.log", "stderr_new.log", "recent_stderr.log", "live_stderr.log",
    "live_stderr_new.log", "live_stderr_recent.log", "startup_error.log",
    "__pycache__", ".agents", "tmp", "sql_app.db", "sql_app_latest.db",
    "sql_app_temp.db", "sql_app_temp2.db", "live_sql_app.db",
    "live_sql_app_after_save.db", "live_sql_app_check.db", "live_sql_app_fix.db",
    "live_sql_app_pwd.db", "live_sql_app_pwd2.db", "live_sql_app_test.db",
    "temp_live_sql_app.db", ".legacy_scripts"
]

def load_backend_env():
    env_path = os.path.join(BACKEND_DIR, ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print("Loaded backend configuration from .env file.")
    else:
        print("Warning: No local .env file found in xcomic_backend directory.")

def run_local_server(port=8000):
    load_backend_env()
    print(f"\n--- Starting Local Backend Server on port {port} ---")
    print("Press Ctrl+C to terminate the server.\n")
    try:
        # Launch Uvicorn in xcomic_backend
        subprocess.run(
            [sys.executable, "-m", "uvicorn", "main:app", "--reload", "--port", str(port)],
            cwd=BACKEND_DIR,
            check=True
        )
    except KeyboardInterrupt:
        print("\nLocal server terminated.")
    except Exception as e:
        print(f"Error starting local server: {e}")

def run_git_sync(message=None):
    print("\n--- Running Git Synchronization ---")
    try:
        # Show status
        print("Checking Git status...")
        subprocess.run(["git", "status"], cwd=ROOT_DIR, check=True)
        
        # Ask for commit message if not provided
        if not message:
            try:
                message = input("\nEnter commit message (leave empty to cancel): ").strip()
            except KeyboardInterrupt:
                print("\nGit synchronization cancelled.")
                return
            if not message:
                print("No commit message. Git synchronization cancelled.")
                return
        
        print("\nStaging files...")
        subprocess.run(["git", "add", "."], cwd=ROOT_DIR, check=True)
        
        print("Committing changes...")
        subprocess.run(["git", "commit", "-m", message], cwd=ROOT_DIR, check=True)
        
        print("Pushing to remote origin master...")
        subprocess.run(["git", "push", "origin", "master"], cwd=ROOT_DIR, check=True)
        print("\nGit synchronization completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")

def ftp_upload_file(ftp, local_path, remote_path, max_attempts=3):
    filename = os.path.basename(local_path)
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"  Uploading {filename} (Attempt {attempt}/{max_attempts})...")
            with open(local_path, "rb") as f:
                ftp.storbinary(f"STOR {remote_path}", f)
            print(f"  Successfully uploaded {filename}")
            return True
        except Exception as e:
            print(f"  Warning: Attempt {attempt} failed: {e}")
            if attempt < max_attempts:
                time.sleep(2)
    print(f"  Error: Failed to upload {filename} after {max_attempts} attempts.")
    return False

def deploy_frontend_ftp(ftp):
    print("\n--- Uploading Frontend Files ---")
    # Upload root files
    ftp.cwd(FTP_FRONTEND_REMOTE)
    for f in ["index.html", "auth.html"]:
        local_path = os.path.join(FRONTEND_DIR, f)
        if os.path.exists(local_path):
            ftp_upload_file(ftp, local_path, f)

    # Upload asset directory
    assets_local = os.path.join(FRONTEND_DIR, "assets")
    if os.path.exists(assets_local):
        try:
            ftp.mkd(f"{FTP_FRONTEND_REMOTE}/assets")
        except:
            pass # Directory might already exist
        
        ftp.cwd(f"{FTP_FRONTEND_REMOTE}/assets")
        for f in os.listdir(assets_local):
            local_path = os.path.join(assets_local, f)
            if os.path.isfile(local_path):
                ftp_upload_file(ftp, local_path, f)

def deploy_backend_ftp(ftp):
    print("\n--- Uploading Backend Files ---")
    # Recursive upload for backend files
    def upload_dir_recursive(local_dir, remote_dir):
        try:
            ftp.mkd(remote_dir)
        except:
            pass
        
        ftp.cwd(remote_dir)
        for item in os.listdir(local_dir):
            if item in EXCLUDE_LIST:
                continue
                
            local_path = os.path.join(local_dir, item)
            remote_path = f"{remote_dir}/{item}" if remote_dir != "/" else f"/{item}"
            
            if os.path.isdir(local_path):
                upload_dir_recursive(local_path, remote_path)
                ftp.cwd(remote_dir) # Go back up
            elif os.path.isfile(local_path):
                # Check extension excludes
                if item.endswith(".pyc") or item.endswith(".db") or item.endswith(".log"):
                    continue
                ftp_upload_file(ftp, local_path, item)

    upload_dir_recursive(BACKEND_DIR, FTP_BACKEND_REMOTE)

def trigger_app_restart(ftp):
    print("\n--- Triggering Live App Restart ---")
    # Write a local restart timestamp
    restart_local_path = os.path.join(ROOT_DIR, "restart.txt")
    with open(restart_local_path, "w") as f:
        f.write(str(time.time()))
        
    try:
        # Create tmp directory on live server if not exists
        try:
            ftp.mkd(f"{FTP_BACKEND_REMOTE}/tmp")
        except:
            pass
        
        # Upload restart.txt to tmp folder
        ftp.cwd(f"{FTP_BACKEND_REMOTE}/tmp")
        ftp_upload_file(ftp, restart_local_path, "restart.txt")
        
        # Upload restart.txt directly to backend root as double guard
        ftp.cwd(FTP_BACKEND_REMOTE)
        ftp_upload_file(ftp, restart_local_path, "restart.txt")
        
        print("Application restart triggered on live server.")
    except Exception as e:
        print(f"Warning: Failed to trigger application restart: {e}")
    finally:
        if os.path.exists(restart_local_path):
            try:
                os.remove(restart_local_path)
            except:
                pass

def run_ftp_deploy(deploy_type="all"):
    print(f"\n--- Initiating Live Deploy ({deploy_type.upper()}) ---")
    try:
        print("Connecting to FTP server...")
        ftp = ftplib.FTP(timeout=60)
        ftp.connect(FTP_HOST, 21)
        ftp.login(FTP_USER, FTP_PASS)
        print("FTP connection established.")

        if deploy_type in ["frontend", "all"]:
            deploy_frontend_ftp(ftp)
            
        if deploy_type in ["backend", "all"]:
            deploy_backend_ftp(ftp)
            trigger_app_restart(ftp)
            
        ftp.quit()
        print("\nLive deployment completed successfully!")
    except Exception as e:
        print(f"FTP Deployment failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Unified local, git, and live deployment manager for XComic.")
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument("--run", action="store_true", help="Start local development FastAPI server.")
    group.add_argument("--git", action="store_true", help="Sync local repository changes with GitHub remote.")
    group.add_argument("--deploy", choices=["frontend", "backend", "all"], help="Deploy files to the live FTP server.")
    
    parser.add_argument("--port", type=int, default=8000, help="Specify port for local server (default: 8000).")
    parser.add_argument("-m", "--message", type=str, help="Commit message for git sync.")
    
    args = parser.parse_args()

    if args.run:
        run_local_server(args.port)
    elif args.git:
        run_git_sync(args.message)
    elif args.deploy:
        run_ftp_deploy(args.deploy)

if __name__ == "__main__":
    main()
