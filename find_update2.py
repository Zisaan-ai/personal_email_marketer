import sys
with open('backend/main.py', encoding='utf-8') as f:
    text = f.read()
idx = text.find('@app.put("/api/sending-accounts/{acc_id}")')
if idx != -1: 
    print(text[idx+1000:idx+3500])
