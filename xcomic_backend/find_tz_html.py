import os

local_file = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_app_js.js"

with open(local_file, "r", encoding="utf-8") as f:
    content = f.read()

# Find the HTML template containing 'Timezone Configuration' or 'user-timezone'
# Search in broader context
lines = content.split("\n")

for i, line in enumerate(lines):
    if 'Timezone' in line and ('Configuration' in line or 'config' in line.lower()):
        start = max(0, i - 5)
        end = min(len(lines), i + 25)
        print(f"=== Found at line {i+1}, showing context ===")
        for j in range(start, end):
            print(f"  {j+1}: {lines[j][:200]}")
        print("---\n")

# Also look for the HTML input/select with id user-timezone
for i, line in enumerate(lines):
    if 'user-timezone' in line and ('<input' in line.lower() or '<select' in line.lower() or 'id=' in line):
        start = max(0, i - 5)
        end = min(len(lines), i + 5)
        print(f"=== HTML element at line {i+1} ===")
        for j in range(start, end):
            print(f"  {j+1}: {lines[j][:200]}")
        print("---\n")

# Search for 'Your Timezone' label
for i, line in enumerate(lines):
    if 'Your Timezone' in line:
        start = max(0, i - 3)
        end = min(len(lines), i + 10)
        print(f"=== 'Your Timezone' at line {i+1} ===")
        for j in range(start, end):
            print(f"  {j+1}: {lines[j][:200]}")
        print("---\n")
