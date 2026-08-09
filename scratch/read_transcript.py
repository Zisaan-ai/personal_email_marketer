import json

log_path = r'C:\Users\higan\.gemini\antigravity\brain\54121d10-b457-4473-8930-be10e5c88a98\.system_generated\logs\transcript.jsonl'
lines = open(log_path, encoding='utf-8').readlines()

for line in lines[-120:]:
    try:
        d = json.loads(line)
        if d.get('type') in ('USER_INPUT', 'PLANNER_RESPONSE'):
            content = str(d.get('content', ''))[:250]
            idx = d['step_index']
            t = d['type']
            print(f"[{idx}] {t}: {content}")
            print("---")
    except:
        pass
