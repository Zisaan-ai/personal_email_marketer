with open("main_live.py", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if "@app.get" in line or "@app.post" in line or "@app.put" in line or "@app.delete" in line:
            print(f"{i}: {line.strip()}")
