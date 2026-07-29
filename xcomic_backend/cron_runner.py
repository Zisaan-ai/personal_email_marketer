import requests, datetime, sys
print(f'[{datetime.datetime.now()}] Cron runner executing...')
try:
    requests.get('https://xcomic.xyz/api/cron/run', timeout=10)
    requests.get('https://xcomic.xyz/api/cron/warmup_reset', timeout=10)
except Exception as e:
    pass
