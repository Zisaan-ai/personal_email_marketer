with open(r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_app_js.js", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "Choices" in line:
        print(f"Line {i+1}: {line.strip()}")
