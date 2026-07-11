@echo off
cd /d "C:\Users\higan\.antigravity-ide\personal_email_marketer\backend"
"C:\Users\higan\.antigravity-ide\personal_email_marketer\backend\venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8000
