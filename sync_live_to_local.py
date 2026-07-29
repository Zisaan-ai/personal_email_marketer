"""
Live server theke local e sync kore ana.
Live FTP -> Local files (xcomic_backend + xcomic.xyz)
"""
import ftplib, os, io

FTP_HOST = "terapk.com"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_LOCAL = os.path.join(ROOT, "xcomic_backend")
FRONTEND_LOCAL = os.path.join(ROOT, "xcomic.xyz")

EXCLUDE = {'.git', '__pycache__', 'tmp', '.agents', '.env', 'sql_app.db', 
            'sql_app_latest.db', 'sql_app_temp.db', 'live_sql_app.db',
            '.legacy_scripts'}

def download_file(ftp, remote_name, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, 'wb') as f:
        ftp.retrbinary(f'RETR {remote_name}', f.write)

def sync_dir(ftp, remote_dir, local_dir, depth=0):
    """Download all files from remote_dir to local_dir"""
    try:
        ftp.cwd(remote_dir)
    except:
        print(f"{'  '*depth}❌ Cannot access {remote_dir}")
        return
    
    items = []
    ftp.retrlines('NLST', items.append)
    
    os.makedirs(local_dir, exist_ok=True)
    
    for item in items:
        if item in ('.', '..') or item in EXCLUDE:
            continue
        if item.endswith('.db') or item.endswith('.log') or item.endswith('.pyc'):
            continue
            
        remote_path = f"{remote_dir}/{item}"
        local_path = os.path.join(local_dir, item)
        
        # Try to cwd into it - if success, it's a directory
        try:
            ftp.cwd(remote_path)
            ftp.cwd(remote_dir)  # go back
            print(f"{'  '*depth}📁 {item}/")
            sync_dir(ftp, remote_path, local_path, depth+1)
            ftp.cwd(remote_dir)  # go back after recursive call
        except:
            # It's a file
            try:
                print(f"{'  '*depth}📄 {item}")
                download_file(ftp, item, local_path)
            except Exception as e:
                print(f"{'  '*depth}⚠️ Failed: {item} ({e})")

def main():
    ftp = ftplib.FTP(FTP_HOST, timeout=30)
    ftp.login(FTP_USER, FTP_PASS)
    
    print("=" * 50)
    print("SYNCING LIVE → LOCAL")
    print("=" * 50)
    
    # Sync backend
    print("\n[1/2] Syncing Backend (/xcomic_backend → local)")
    print("-" * 40)
    sync_dir(ftp, '/xcomic_backend', BACKEND_LOCAL)
    
    # Sync frontend (only key files, not all assets)
    print("\n[2/2] Syncing Frontend (/xcomic.xyz → local)")
    print("-" * 40)
    # Only sync important frontend files
    ftp.cwd('/xcomic.xyz')
    
    for f in ['index.html']:
        try:
            local_path = os.path.join(FRONTEND_LOCAL, f)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            print(f"📄 {f}")
            with open(local_path, 'wb') as fh:
                ftp.retrbinary(f'RETR {f}', fh.write)
        except Exception as e:
            print(f"⚠️ {f}: {e}")
    
    # Sync assets
    ftp.cwd('/xcomic.xyz/assets')
    assets_local = os.path.join(FRONTEND_LOCAL, 'assets')
    os.makedirs(assets_local, exist_ok=True)
    
    for f in ['app.js']:
        try:
            local_path = os.path.join(assets_local, f)
            print(f"📄 assets/{f}")
            with open(local_path, 'wb') as fh:
                ftp.retrbinary(f'RETR {f}', fh.write)
        except Exception as e:
            print(f"⚠️ assets/{f}: {e}")
    
    ftp.quit()
    
    print("\n" + "=" * 50)
    print("✅ SYNC COMPLETE!")
    print(f"Backend: {BACKEND_LOCAL}")
    print(f"Frontend: {FRONTEND_LOCAL}")
    print("=" * 50)

if __name__ == "__main__":
    main()
