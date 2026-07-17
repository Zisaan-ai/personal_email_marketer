import filecmp
import os

comparisons = [
    ('live_code/main.py', 'xcomic_backend/main.py'),
    ('live_code/database.py', 'xcomic_backend/database.py'),
    ('live_code/ai_core.py', 'xcomic_backend/ai_core.py'),
    ('live_code/bounce_processor.py', 'xcomic_backend/bounce_processor.py'),
    ('live_code/health_monitor.py', 'xcomic_backend/health_monitor.py'),
    ('live_code/warmup_service.py', 'xcomic_backend/warmup_service.py'),
    ('live_code/passenger_wsgi.py', 'passenger_wsgi.py'),
    ('live_code/index.html', 'xcomic.xyz/index.html'),
    ('live_code/app.js', 'xcomic.xyz/assets/app.js'),
    ('live_code/sending_accounts.js', 'xcomic.xyz/assets/sending_accounts.js'),
]

for live_file, local_file in comparisons:
    if not os.path.exists(live_file):
        print(f"MISSING LIVE: {live_file}")
        continue
    if not os.path.exists(local_file):
        print(f"MISSING LOCAL: {local_file}")
        continue
    
    if not filecmp.cmp(live_file, local_file, shallow=False):
        print(f"DIFFERENT: {live_file} != {local_file}")
    else:
        print(f"SAME: {live_file} == {local_file}")
