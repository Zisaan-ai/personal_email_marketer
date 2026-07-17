with open('live_code/passenger_wsgi.py', 'r', encoding='utf-8') as f:
    live = f.readlines()
with open('passenger_wsgi.py', 'r', encoding='utf-8') as f:
    local = f.readlines()

import difflib
for line in difflib.unified_diff(local, live, fromfile='passenger_wsgi.py (local)', tofile='live_code/passenger_wsgi.py (live)'):
    print(line, end='')
