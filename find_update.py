import sys
with open('backend/main.py', encoding='utf-8') as f:
    text = f.read()
idx = text.find('@app.put("/api/sending-accounts/{acc_id}")')
if idx == -1: idx = text.find('def update_sending_account')
if idx == -1: 
    print('NOT FOUND')
else: 
    print(text[max(0, idx-100):idx+1500])
