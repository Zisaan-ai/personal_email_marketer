
import os, subprocess, sys
print('Killing uvicorn and cron_runner...')
try:
    os.system('pkill -9 -f uvicorn')
    os.system('pkill -9 -f cron_runner.py')
    print('Killed successfully.')
except Exception as e:
    print(e)
