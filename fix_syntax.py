with open('live_code/xcomic_backend/warmup_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the syntax error by removing the extra try: at line 367
fixed_content = content.replace('    try:\n        print(\"[Warmup] ══ Starting warmup cycle ══\")\n        db = database.SessionLocal()\n        detached_accounts = []', '    print(\"[Warmup] ══ Starting warmup cycle ══\")\n    db = database.SessionLocal()\n    detached_accounts = []')

with open('xcomic_backend/warmup_service.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print('Fixed warmup_service.py locally.')
