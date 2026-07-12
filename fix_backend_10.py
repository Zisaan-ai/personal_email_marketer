import sys

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """        # Check time
        start = camp.start_hour if camp.start_hour is not None else 0
        end = camp.end_hour if camp.end_hour is not None else 24
        
        if start == 0 and end == 24:
            pass
        elif not (start <= now.hour < end):
            return False, f"Current time ({now.strftime('%H:%M')} {tz_str}) is outside allowed window ({start}:00 - {end}:00)"
            
        return True, None"""

new_logic = """        # Check time
        start = camp.start_hour if camp.start_hour is not None else 0
        end = camp.end_hour if camp.end_hour is not None else 24
        
        if start == 0 and end == 24:
            pass
        elif start <= end:
            # Normal window (e.g., 09:00 - 17:00)
            if not (start <= now.hour < end):
                return False, f"Current time ({now.strftime('%H:%M')} {tz_str}) is outside allowed window ({start}:00 - {end}:00)"
        else:
            # Overnight window (e.g., 22:00 - 05:00)
            if not (now.hour >= start or now.hour < end):
                return False, f"Current time ({now.strftime('%H:%M')} {tz_str}) is outside allowed window ({start}:00 - {end}:00)"
                
        return True, None"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed time window logic")
else:
    print("Could not find old logic")
