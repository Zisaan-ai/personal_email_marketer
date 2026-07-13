import requests

BASE_URL = 'https://xcomic.xyz/api'
username = 'zmonemrahman@gmail.com'
password = '76008972'

r = requests.post(f'{BASE_URL}/auth/token', data={'username': username, 'password': password})
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

campaign_id = 'a30c4150-1f85-438a-a303-bacd36ab07ef'
print(requests.get(f'{BASE_URL}/campaigns/{campaign_id}/leads', headers=headers).text)
