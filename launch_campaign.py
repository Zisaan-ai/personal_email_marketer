import requests

BASE_URL = 'https://xcomic.xyz/api'
username = 'zmonemrahman@gmail.com'
password = '76008972'

r = requests.post(f'{BASE_URL}/auth/token', data={'username': username, 'password': password})
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

html_body = """
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
    <h2 style="color: #4f46e5; text-align: center;">Meet Your Ultimate AI Email Marketer! 🚀</h2>
    <p>Hello {name},</p>
    <p>We are thrilled to introduce you to our next-generation <strong>Cold Email & Newsletter Marketing Platform</strong>, fully managed and assisted by an AI agent.</p>
    
    <h3 style="color: #333;">✨ Key Facilities:</h3>
    <ul style="line-height: 1.6; color: #555;">
        <li><strong>Visual Builder:</strong> Craft beautiful HTML newsletters effortlessly.</li>
        <li><strong>A/B Testing:</strong> Test multiple subjects and body variants to optimize conversion.</li>
        <li><strong>Smart Scheduling:</strong> Specify timezones, sending days, and custom delays (like your 400-800 sec setup) to avoid spam filters.</li>
        <li><strong>Automated Warmup:</strong> AI-powered auto-replies to boost your sender reputation.</li>
        <li><strong>Health Monitoring:</strong> Real-time domain and DNS (SPF, DKIM, DMARC) checks.</li>
        <li><strong>Bounce Tracking:</strong> Auto-detect and handle bounced emails.</li>
    </ul>

    <p>Experience the magic of automated marketing today. Log in to your dashboard and launch your next AI-driven campaign!</p>
    
    <div style="text-align: center; margin: 30px 0;">
        <a href="https://xcomic.xyz/" style="background-color: #4f46e5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">Login to Dashboard</a>
    </div>
    
    <p style="color: #777; font-size: 12px; text-align: center; border-top: 1px solid #eee; padding-top: 15px;">Created and launched autonomously by your AI Assistant.</p>
</div>
"""

payload = {
    'subject': 'Introducing Your Ultimate AI Email Marketer 🚀',
    'body': html_body,
    'type': 'newsletter',
    'leads': [
        {'email': 'zisan7619@gmail.com', 'name': 'Zisan'},
        {'email': 'mdzisan7575@gmail.com', 'name': 'Md Zisan'},
        {'email': '2024200000039@gmail.com', 'name': 'SEU'},
        {'email': 'monemzisan7@gmail.com', 'name': 'Monem Zisan'}
    ],
    'is_draft': False,
    'delay_min': 10,
    'delay_max': 20,
    'sending_days': '["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]',
    'start_hour': 0,
    'end_hour': 24,
    'timezone': 'Asia/Dhaka'
}

r2 = requests.post(f'{BASE_URL}/campaigns/send', headers=headers, json=payload)
print('Launch Response:', r2.json())
