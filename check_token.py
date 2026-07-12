with open('backend/main.py', encoding='utf-8') as f:
    text = f.read()
    idx = text.find('@app.post("/api/auth/token"')
    print(text[max(0, idx-50):idx+1500])
