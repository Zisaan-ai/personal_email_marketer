import urllib.request
import json
import urllib.parse
import sys

base_url = 'https://xcomic.xyz/api'
email = 'zmonemrahman@gmail.com'
password = '76008972'

data = urllib.parse.urlencode({'username': email, 'password': password}).encode('utf-8')
login_req = urllib.request.Request(f'{base_url}/auth/token', data=data, method='POST')
try:
    login_res = urllib.request.urlopen(login_req)
    token = json.loads(login_res.read().decode('utf-8'))['access_token']
except urllib.error.HTTPError as e:
    sys.exit(1)

def req(url, data=None, method='POST'):
    req_obj = urllib.request.Request(url, method=method)
    req_obj.add_header('Content-Type', 'application/json')
    req_obj.add_header('Authorization', f'Bearer {token}')
    if data:
        data_bytes = json.dumps(data).encode('utf-8')
        try:
            res = urllib.request.urlopen(req_obj, data=data_bytes)
            return json.loads(res.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return {'error': e.code, 'detail': e.read().decode('utf-8')}
    else:
        try:
            res = urllib.request.urlopen(req_obj)
            return json.loads(res.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return {'error': e.code, 'detail': e.read().decode('utf-8')}

# Payload imitating Visual Builder
payload = {
    'subject': 'VB Test Launch from script',
    'body': '<html><body>Hello from VB</body></html>',
    'type': 'newsletter',
    'campaign_id': None,
    'sending_days': '["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]',
    'start_hour': 0,
    'end_hour': 24,
    'timezone': 'UTC',
    'leads': [{'email': 'mzisan367@gmail.com', 'name': '', 'company': ''}]
}
res = req(f'{base_url}/campaigns/send', data=payload)
print('Launch response:', res)
