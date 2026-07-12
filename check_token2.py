with open('backend/main.py', encoding='utf-8') as f:
    text = f.read()
    idx = text.find('@app.post("/api/auth/token", response_model=Token)')
    print(text[max(0, idx-200):idx+500])
