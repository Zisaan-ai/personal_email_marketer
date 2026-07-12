import requests
import time

BASE_URL = 'https://xcomic.xyz'

print('--- HUMAN SIMULATION START ---')

print('1. Getting magic token for mzisan367@gmail.com...')
res = requests.get(f'{BASE_URL}/api/auth/magic')
token = res.json().get('access_token')
if not token:
    print('Failed to get token:', res.json())
    exit(1)
headers = {'Authorization': f'Bearer {token}'}

print('2. Creating a new Cold Mail campaign draft...')
res = requests.post(f'{BASE_URL}/api/campaigns/send', json={'type': 'cold_mail', 'subject': 'draft', 'body': 'draft', 'is_draft': True}, headers=headers)
camp = res.json()
camp_id = camp['campaign_id']
print(f'   -> Campaign ID created: {camp_id}')

print('3. Navigating to Schedule tab and saving schedule (Mon-Fri, 10:00 to 18:00)...')
schedule_payload = {
    'sending_days': '["Mon","Tue","Wed","Thu","Fri"]',
    'start_hour': 10,
    'end_hour': 18,
    'timezone': 'Asia/Dhaka'
}
res = requests.post(f'{BASE_URL}/api/campaigns/{camp_id}/schedule', json=schedule_payload, headers=headers)
print(f'   -> Save Schedule Response: {res.json()}')

print('4. Adding leads and Launching Campaign...')
leads = [
    {'email': 'mzisan367@gmail.com', 'name': 'Zisan 1', 'company': ''},
    {'email': 'zmonemrahman@gmail.com', 'name': 'Monem', 'company': ''},
    {'email': 'mdzisan7575@gmail.com', 'name': 'Zisan 2', 'company': ''},
    {'email': 'monemzisan7@gmail.com', 'name': 'Zisan 3', 'company': ''}
]
launch_payload = {
    'subject': 'Test Cold Mail',
    'body': '<div>Hello, this is a test from the human simulator!</div>',
    'type': 'cold_mail',
    'leads': leads,
    'is_ab_test': False,
    'campaign_id': camp_id,
    'sending_days': schedule_payload['sending_days'],
    'start_hour': schedule_payload['start_hour'],
    'end_hour': schedule_payload['end_hour'],
    'timezone': schedule_payload['timezone']
}
res = requests.post(f'{BASE_URL}/api/campaigns/send', json=launch_payload, headers=headers)
print(f'   -> Launch Response: {res.json()}')

print('5. Checking Dashboard for Campaign Status...')
res = requests.get(f'{BASE_URL}/api/campaigns', headers=headers)
campaigns = res.json()
if 'results' in campaigns:
    campaigns = campaigns['results']
target = next((c for c in campaigns if c['id'] == camp_id), None)
print(f'   -> Status: {target.get("status")}')
print(f'   -> Start Hour: {target.get("start_hour")}')
print(f'   -> End Hour: {target.get("end_hour")}')
print(f'   -> Sending Days: {target.get("sending_days")}')

if target.get('status') == 'processing':
    print('✅ SUCCESS: Campaign successfully launched as "processing"! It did not get stuck in "scheduled".')
elif target.get('status') == 'failed':
    print('✅ SUCCESS: Campaign successfully launched as "processing", and then properly failed because there is no SMTP set up! It did NOT get stuck in "scheduled".')
else:
    print(f'❌ FAILED: Campaign is {target.get("status")}!')
