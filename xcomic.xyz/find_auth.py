import sys

lines = open('index.html', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'id="auth-page"' in line or 'login-form' in line:
        print(f"Line {i+1}: {line.strip()}")
