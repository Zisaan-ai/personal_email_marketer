with open('backend/main.py', encoding='utf-8') as f:
    text = f.read()
    if '@app.post("/api/replies' in text or '@app.post(\'/api/replies' in text:
        print('POST /api/replies exists')
    else:
        print('No POST for replies')
