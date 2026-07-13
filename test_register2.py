import requests

url = 'https://xcomic.xyz/api/auth/token'
data = {'username': 'zonemrahman@gmail.com', 'password': 'password76008972'}
res = requests.post(url, data=data)
if res.status_code == 200:
    token = res.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    fetch_url = 'https://xcomic.xyz/api/campaigns'
    fetch_res = requests.get(fetch_url, headers=headers)
    if fetch_res.status_code == 200:
        campaigns = fetch_res.json()
        if len(campaigns) > 0:
            print(campaigns[0])
