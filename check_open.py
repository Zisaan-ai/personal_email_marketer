with open('backend/main.py', encoding='utf-8') as f:
    text = f.read()
    idx = text.find('@app.get("/api/track/lead_open')
    if idx != -1:
        print(text[idx:idx+1500])
