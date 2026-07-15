import codecs
import re

js_path = 'frontend/assets/app_v2.js'

with codecs.open(js_path, 'r', 'utf-8') as f:
    js_content = f.read()

# 1. Add fetching of new keys from DOM in saveGeminiBtn handler
old_fetch = """            const groqKeyEl = document.getElementById('groq-api-key');
            const groqKey = groqKeyEl ? groqKeyEl.value : null;"""

new_fetch = """            const groqKeyEl = document.getElementById('groq-api-key');
            const groqKey = groqKeyEl ? groqKeyEl.value : null;
            
            const openaiKeyEl = document.getElementById('openai-api-key');
            const openaiKey = openaiKeyEl ? openaiKeyEl.value : null;
            
            const anthropicKeyEl = document.getElementById('anthropic-api-key');
            const anthropicKey = anthropicKeyEl ? anthropicKeyEl.value : null;
            
            const deepseekKeyEl = document.getElementById('deepseek-api-key');
            const deepseekKey = deepseekKeyEl ? deepseekKeyEl.value : null;"""

js_content = js_content.replace(old_fetch, new_fetch)

# 2. Add API calls to save the keys
old_save = """                if (groqKey) {
                    await apiCall('/settings/groq', 'POST', { groq_api_key: groqKey });
                }"""

new_save = """                if (groqKey) {
                    await apiCall('/settings/groq', 'POST', { groq_api_key: groqKey });
                }
                if (openaiKey) {
                    await apiCall('/settings/openai', 'POST', { openai_api_key: openaiKey });
                }
                if (anthropicKey) {
                    await apiCall('/settings/anthropic', 'POST', { anthropic_api_key: anthropicKey });
                }
                if (deepseekKey) {
                    await apiCall('/settings/deepseek', 'POST', { deepseek_api_key: deepseekKey });
                }"""

js_content = js_content.replace(old_save, new_save)

# 3. Add logic to load keys into inputs when Settings page opens
old_load = """        setVal('gemini-api-key', s.gemini_api_key);
        setVal('groq-api-key', s.groq_api_key);"""

new_load = """        setVal('gemini-api-key', s.gemini_api_key);
        setVal('groq-api-key', s.groq_api_key);
        setVal('openai-api-key', s.openai_api_key);
        setVal('anthropic-api-key', s.anthropic_api_key);
        setVal('deepseek-api-key', s.deepseek_api_key);"""

js_content = js_content.replace(old_load, new_load)

with codecs.open(js_path, 'w', 'utf-8') as f:
    f.write(js_content)

print("Successfully updated frontend/assets/app_v2.js")
