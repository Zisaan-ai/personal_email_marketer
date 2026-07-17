import requests

login_url = "https://xcomic.xyz/api/auth/token"
accounts_url = "https://xcomic.xyz/api/sending-accounts"

credentials = {
    "username": "zmonemrahman@gmail.com",
    "password": "76008972"
}

print("Attempting login...")
try:
    r = requests.post(login_url, data=credentials, timeout=15)
    print(f"Login Status: {r.status_code}")
    if r.status_code != 200:
        print(f"Login failed: {r.text}")
        exit(1)
        
    token_data = r.json()
    token = token_data.get("access_token")
    print("Login successful! Token acquired.")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print("\nFetching sending accounts...")
    r_accounts = requests.get(accounts_url, headers=headers, timeout=15)
    print(f"Accounts Status: {r_accounts.status_code}")
    print("Accounts JSON Payload:")
    print(r_accounts.text)
    
except Exception as e:
    print(f"Failed to verify: {e}")
