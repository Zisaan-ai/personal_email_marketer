
import os
import subprocess
try:
    subprocess.check_call(['pkill', '-f', 'passenger'])
except Exception as e:
    print('passenger pkill error:', e)

try:
    subprocess.check_call(['pkill', '-f', 'python'])
except Exception as e:
    print('python pkill error:', e)
