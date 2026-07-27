import requests, datetime, sys
print(f'[{datetime.datetime.now()}] Cron runner executing...')
try:
    requests.get('http://localhost:8000/api/cron/run', timeout=10)
except Exception as e:
    pass
