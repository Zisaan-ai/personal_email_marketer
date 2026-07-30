local_main = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\xcomic_backend\main.py"

with open(local_main, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split('\n')
for i, line in enumerate(lines):
    if '@app.post' in line or '@app.put' in line or '@app.get' in line:
        if 'campaign' in line.lower():
            print(f"Line {i+1}: {line.strip()}")
