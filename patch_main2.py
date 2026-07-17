import ftplib
import io
import re

host = '167.235.11.154'
user = 'terapkco'
password = '(3#JCk2Vyn94hY'

try:
    ftp = ftplib.FTP(host, user, password, timeout=10)
    ftp.cwd('xcomic_backend')
    
    # Download main.py
    main_buf = io.BytesIO()
    ftp.retrbinary('RETR main.py', main_buf.write)
    main_py = main_buf.getvalue().decode('utf-8')
    
    # Patch main.py
    patch = '''
@app.get("/api/test-accounts")
def test_accounts(db: Session = Depends(database.get_db)):
    admin = db.query(database.User).filter(database.User.email == "zmonemrahman@gmail.com").first()
    accounts = db.query(database.SendingAccount).filter(database.SendingAccount.user_id == str(admin.id)).all()
    
    result = []
    for acc in accounts:
        try:
            result.append({"id": str(acc.id), "email": acc.email, "health": acc.health_score})
        except Exception as e:
            result.append({"id": str(acc.id), "error": str(e)})
            
    return {"admin_id": str(admin.id), "length": len(accounts), "accounts": result}

@app.get("/api/sending-accounts")
'''
    main_py = main_py.replace('@app.get("/api/sending-accounts")', patch)
    
    # Upload patched main.py
    ftp.storbinary('STOR main.py', io.BytesIO(main_py.encode('utf-8')))
    
    # Restart
    ftp.cwd('../tmp')
    ftp.storbinary('STOR restart.txt', io.BytesIO(b''))
    ftp.quit()
    print("Patched and restarted")
except Exception as e:
    print(f"Error: {e}")
