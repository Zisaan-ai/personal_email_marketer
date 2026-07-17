import requests

try:
    r = requests.get('https://xcomic.xyz/', timeout=10)
    print('Main Page Status:', r.status_code)
    print('Main Page length:', len(r.text))
except Exception as e:
    print('Main Page Error:', e)

try:
    r = requests.get('https://xcomic.xyz/api/test-db', timeout=10)
    print('API test-db Status:', r.status_code)
    print('API test-db Response:', r.text)
except Exception as e:
    print('API test-db Error:', e)
