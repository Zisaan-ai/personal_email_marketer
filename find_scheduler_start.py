with open("main_live.py", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if "scheduler.start" in line:
            print(f"{i}: {line.strip()}")
