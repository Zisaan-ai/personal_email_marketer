import requests
import json
import urllib3
urllib3.disable_warnings()
BASE = 'https://xcomic.xyz/api'
r = requests.post(f'{BASE}/auth/token', data={'username': 'zmonemrahman@gmail.com', 'password': '76008972'}, timeout=15)
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
r = requests.get(f'{BASE}/domain-health/gmail.com', headers=headers)
print(json.dumps(r.json(), indent=2))
