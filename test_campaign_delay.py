import requests

BASE_URL = 'https://xcomic.xyz/api'
username = 'zmonemrahman@gmail.com'
password = '76008972'

r = requests.post(f'{BASE_URL}/auth/token', data={'username': username, 'password': password})
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Simulate creating a draft campaign in Cold Mail with custom delay
draft_payload = {
    'subject': 'Draft Campaign Test',
    'body': 'Draft body',
    'type': 'cold_mail',
    'leads': [],
    'is_draft': True,
    'delay_min': 415,
    'delay_max': 815
}
r2 = requests.post(f'{BASE_URL}/campaigns/send', headers=headers, json=draft_payload)
print('Draft Response:', r2.json())
campaign_id = r2.json()['campaign_id']

# Simulate updating the schedule
schedule_payload = {
    'delay_min': 500,
    'delay_max': 900
}
r3 = requests.post(f'{BASE_URL}/campaigns/{campaign_id}/save-schedule', headers=headers, json=schedule_payload)
print('Schedule Save Response:', r3.json())

# Fetch it back to verify
r4 = requests.get(f'{BASE_URL}/campaigns', headers=headers)
c = next((x for x in r4.json() if x['id'] == campaign_id), None)
print(f"Verified Campaign ID: {c['id']}, Min Delay: {c.get('delay_min')}, Max Delay: {c.get('delay_max')}")
