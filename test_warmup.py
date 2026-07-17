
import sys
import os
sys.path.append('.')
import warmup_service
print('Running warmup cycle manually...')
warmup_service.run_warmup_cycle()
print('Warmup cycle finished.')
