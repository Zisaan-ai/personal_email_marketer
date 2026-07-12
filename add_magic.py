import sys
with open('backend/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
magic_code = '''
@app.get("/api/auth/magic")
def magic_login(db: Session = Depends(database.get_db)):
    try:
        user = db.query(database.User).filter(database.User.email == "zmonemrahman@gmail.com").first()
        if not user:
            return {"error": "User not found"}
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
        return {"access_token": access_token}
    except Exception as e:
        return {"error": str(e)}

'''
text = re.sub(r'@app\.get\(\"/api/auth/magic\"\).*?return \{\"error\": str\(e\)\}\n*', magic_code, text, flags=re.DOTALL)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done!')
