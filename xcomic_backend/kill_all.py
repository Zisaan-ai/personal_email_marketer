
import os
os.system('pkill -f uvicorn')
os.system('pkill -f passenger')
print('Killed')
