with open('main_live.py', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace('"suggested_warmup_limit": health_monitor.suggest_warmup_limit(acc),', '"suggested_warmup_limit": getattr(acc, "warmup_daily_limit", 5),')

with open('main_live.py', 'w', encoding='utf-8') as f:
    f.write(js)
