import requests
BASE = 'https://xcomic.xyz/api'
r = requests.post(f'{BASE}/auth/token', data={'username': 'zmonemrahman@gmail.com', 'password': '76008972'})
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

payload = {
    'subject': 'Test',
    'body': 'Test body',
    'type': 'cold_mail',
    'leads': [{'email': 'test@example.com'}],
    'is_ab_test': False,
    'subject_b': '',
    'body_b': '',
    'delay_min': 30,
    'delay_max': 90,
    'campaign_id': None,
    'sending_days': '[" Mon\,\Tue\,\Wed\,\Thu\,\Fri\,\Sat\,\Sun\]',
 'start_hour': 0,
 'end_hour': 24,
 'timezone': 'UTC'
}
res = requests.post(f'{BASE}/campaigns/send', json=payload, headers=headers)
print(res.status_code)
print(res.text)
