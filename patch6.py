with open('main_live.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix the warmup_limit
text = text.replace('"suggested_warmup_limit": health_monitor.suggest_warmup_limit(acc),', '"suggested_warmup_limit": getattr(acc, "warmup_daily_limit", 5),')

# 2. Fix created_at datetime just in case
text = text.replace('"created_at": acc.created_at,', '"created_at": str(acc.created_at),')

with open('main_live.py', 'w', encoding='utf-8') as f:
    f.write(text)
