"""Compare live vs local app.js to find differences"""
import requests

# Download live version
r = requests.get('https://xcomic.xyz/assets/app.js', timeout=15)
live = r.text

with open(r'C:\Users\higan\.antigravity-ide\personal_email_marketer\frontend\assets\app.js', encoding='utf-8') as f:
    local = f.read()

print(f"Live chars: {len(live)}")
print(f"Local chars: {len(local)}")
print(f"Difference: {len(live) - len(local)} chars")

# Check key sections
for keyword in ['sendSeqBtn', 'inst-send-seq-btn', 'runPreflightAsync', 'campaigns/send', 'Launch Campaign', 'sch-day-mon', 'sending_days', 'saveStep']:
    live_count = live.count(keyword)
    local_count = local.count(keyword)
    match = "OK" if live_count == local_count else "MISMATCH"
    print(f"  '{keyword}': live={live_count} local={local_count} {match}")

# Check if the critical sendSeqBtn click handler exists in live
idx = live.find("inst-send-seq-btn")
if idx >= 0:
    snippet = live[max(0,idx-50):idx+200].replace('\n', '\\n').replace('\r', '')
    print(f"\nLive has inst-send-seq-btn at char {idx}:")
    print(f"  ...{snippet[:200]}...")
else:
    print("\n!!! CRITICAL: Live file does NOT contain inst-send-seq-btn !!!")

# Check sendBtn (visual builder)
idx2 = live.find("sendBtn.innerHTML")
if idx2 >= 0:
    print(f"\nLive has sendBtn.innerHTML at char {idx2}")
else:
    print("\n!!! CRITICAL: Live file does NOT contain sendBtn.innerHTML !!!")

# Compare the critical campaign launch section
live_launch = live.find("apiCall('/campaigns/send', 'POST', payload)")
local_launch = local.find("apiCall('/campaigns/send', 'POST', payload)")
print(f"\nLive apiCall campaigns/send at: {live_launch}")
print(f"Local apiCall campaigns/send at: {local_launch}")

# Count how many times the apiCall to campaigns/send appears
search_str = "apiCall('/campaigns/send'"
live_cnt = live.count(search_str)
local_cnt = local.count(search_str)
print(f"\nLive count of campaigns/send POST: {live_cnt}")
print(f"Local count of campaigns/send POST: {local_cnt}")

# Save live version for comparison
with open('live_app.js', 'w', encoding='utf-8') as f:
    f.write(live)
print("\nSaved live version to live_app.js for comparison")
