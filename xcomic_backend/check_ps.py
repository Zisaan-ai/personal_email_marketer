
import os, subprocess
print('Processes:')
try:
    print(subprocess.check_output(['ps', 'aux']).decode('utf-8'))
except Exception as e:
    print(e)
