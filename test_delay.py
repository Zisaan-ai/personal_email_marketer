import requests
import json
import time

BASE_URL = 'https://xcomic.xyz/api'
username = 'zmonemrahman@gmail.com'
password = '76008972'

r = requests.post(f'{BASE_URL}/auth/token', data={'username': username, 'password': password})
if not r.ok:
    print('Auth failed')
    exit(1)
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

payload = {
    'subject': 'Delay Test Campaign from AI',
    'body': 'This is a test to verify if the new delay settings are being respected. <br/>Best, AI',
    'type': 'newsletter',
    'leads': [
        {'email': 'mdzisan7575@gmail.com', 'name': 'Zisan'},
        {'email': 'monemzisan7@gmail.com', 'name': 'Monem'}
    ],
    'is_draft': False,
    'delay_min': 5,
    'delay_max': 10,
    'sending_days': json.dumps(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]),
    'start_hour': 0,
    'end_hour': 24,
    'timezone': 'UTC'
}

r2 = requests.post(f'{BASE_URL}/campaigns/send', json=payload, headers=headers)
if not r2.ok:
    print('Campaign creation failed:', r2.text)
    exit(1)

campaign_id = r2.json().get('campaign_id')
print(f'Campaign created successfully! ID: {campaign_id}')

print('Monitoring leads for the next 45 seconds...')
for i in range(9):
    r3 = requests.get(f'{BASE_URL}/campaigns/{campaign_id}/leads', headers=headers)
    if r3.ok:
        leads = r3.json()
        statuses = [l.get('status') for l in leads]
        print(f'[{i*5}s] Lead Statuses:', statuses)
        if all(s in ['sent', 'bounced'] for s in statuses):
            print('All leads processed!')
            break
    time.sleep(5)
