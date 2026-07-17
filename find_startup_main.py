with open("main_live.py", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if "startup" in line or "lifespan" in line or "@app.on" in line:
            print(f"{i}: {line.strip()}")
