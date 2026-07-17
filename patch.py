with open('main_live.py', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace('"provider": acc.provider,', '"provider": getattr(acc, "provider", "smtp"),')

with open('main_live.py', 'w', encoding='utf-8') as f:
    f.write(js)
