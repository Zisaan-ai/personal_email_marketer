import os

local_file = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_app_js.js"

with open(local_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'daily statistics reset and warmup scheduling' in line:
        start = max(0, i - 3)
        end = min(len(lines), i + 5)
        print(f"=== Found at line {i+1} ===")
        for j in range(start, end):
            print(f"  {j+1}: {lines[j].rstrip()[:200]}")
        print("---")
