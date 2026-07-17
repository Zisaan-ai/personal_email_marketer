
import os, subprocess
print('--- PROCESSES ---')
try:
    print(subprocess.check_output(['ps', 'xwf']).decode('utf-8'))
except Exception as e:
    print('Error:', e)
