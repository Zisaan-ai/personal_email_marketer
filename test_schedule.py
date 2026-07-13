import requests

BASE_URL = 'https://xcomic.xyz/api'
username = 'zmonemrahman@gmail.com'
password = '76008972'

r = requests.post(f'{BASE_URL}/auth/token', data={'username': username, 'password': password})
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

payload = {
    "subject": "Untitled Newsletter",
    "body": "",
    "type": "newsletter",
    "leads": [],
    "is_draft": True,
    "sending_days": "[\"Mon\",\"Tue\",\"Wed\",\"Thu\",\"Fri\",\"Sat\",\"Sun\"]",
    "start_hour": 0,
    "end_hour": 24,
    "timezone": "UTC",
    "delay_min": 30,
    "delay_max": 90
}

r2 = requests.post(f'{BASE_URL}/campaigns/send', json=payload, headers=headers)
print("Status:", r2.status_code)
print("Response:", r2.text)
