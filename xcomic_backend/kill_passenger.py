import os
import signal
import psutil

my_pid = os.getpid()
killed = 0

for p in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        if p.pid == my_pid:
            continue
        if p.name().startswith('python') or 'litespeed' in p.name().lower() or 'lsphp' in p.name().lower():
            cmd = ' '.join(p.cmdline()).lower()
            if 'passenger' in cmd or 'xcomic' in cmd or 'main' in cmd:
                os.kill(p.pid, signal.SIGKILL)
                killed += 1
    except:
        pass

print(f'Killed {killed} processes.')
