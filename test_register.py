import requests
import time

# Login
url = 'https://xcomic.xyz/api/auth/token'
data = {'username': 'zonemrahman@gmail.com', 'password': 'password76008972'}
res = requests.post(url, data=data)
if res.status_code == 200:
    token = res.json().get('access_token')
    print('Login successful!')
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Create campaign
    create_url = 'https://xcomic.xyz/api/campaigns/send'
    payload = {
        'subject': 'Test Campaign Options',
        'body': 'This is a test',
        'type': 'newsletter',
        'is_draft': True,
        'max_emails_per_day': 42,
        'daily_ramp_up': 7,
        'track_opens': False,
        'track_clicks': False,
        'use_unsubscribe': False
    }
    create_res = requests.post(create_url, json=payload, headers=headers)
    print('Create Campaign:', create_res.status_code, create_res.text)
    
    time.sleep(2)
    
    # Fetch campaigns
    fetch_url = 'https://xcomic.xyz/api/campaigns'
    fetch_res = requests.get(fetch_url, headers=headers)
    if fetch_res.status_code == 200:
        campaigns = fetch_res.json()
        print('Fetched campaigns. Total:', len(campaigns))
        if len(campaigns) > 0:
            c = campaigns[0]
            print('Latest Campaign Settings:')
            print('Subject:', c.get('subject'))
            print('Max Emails:', c.get('max_emails_per_day'))
            print('Ramp Up:', c.get('daily_ramp_up'))
            print('Track Opens:', c.get('track_opens'))
            print('Track Clicks:', c.get('track_clicks'))
            print('Unsubscribe:', c.get('use_unsubscribe'))
else:
    print('Login failed:', res.status_code, res.text)
