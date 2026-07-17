with open('main_live.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
text = re.sub(r'raise HTTPException\(status_code=500, detail=str\(e\) \+.*?traceback\.format_exc\(\)\)',
              r'return {"debug_error": str(e), "traceback": traceback.format_exc()}', text, flags=re.DOTALL)

with open('main_live.py', 'w', encoding='utf-8') as f:
    f.write(text)
