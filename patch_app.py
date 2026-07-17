import os

with open('xcomic.xyz/assets/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

verify_fn = """
    async function verifyAllAIKeys() {
        const providers = ['gemini', 'groq', 'openai', 'anthropic', 'deepseek'];
        for (const provider of providers) {
            const keyEl = document.getElementById(provider + '-api-key');
            const key = keyEl ? keyEl.value : '';
            const badge = document.getElementById('badge-' + provider);
            if (!badge) continue;

            if (!key) {
                badge.innerHTML = `<span style="display:inline-block;width:4px;height:4px;background:#ef4444;border-radius:50%;margin-right:4px;vertical-align:middle;margin-bottom:1px;"></span>No Key`;
                badge.style.background = '#fee2e2';
                badge.style.color = '#ef4444';
                continue;
            }
            
            badge.innerHTML = `<i class="fa-solid fa-spinner fa-spin" style="margin-right:4px;font-size:9px;"></i>Checking`;
            badge.style.background = '#e0e7ff';
            badge.style.color = '#4338ca';

            try {
                const res = await apiCall('/settings/verify_key', 'POST', { provider, api_key: key });
                const data = await res.json();
                
                if (data.status === 'valid') {
                    badge.innerHTML = `<span style="display:inline-block;width:4px;height:4px;background:#10b981;border-radius:50%;margin-right:4px;vertical-align:middle;margin-bottom:1px;"></span>Key Active`;
                    badge.style.background = '#dcfce7';
                    badge.style.color = '#059669';
                } else if (data.status === 'invalid') {
                    badge.innerHTML = `<span style="display:inline-block;width:4px;height:4px;background:#ca8a04;border-radius:50%;margin-right:4px;vertical-align:middle;margin-bottom:1px;"></span>Invalid Key`;
                    badge.style.background = '#fef08a';
                    badge.style.color = '#ca8a04';
                } else {
                    badge.innerHTML = `<span style="display:inline-block;width:4px;height:4px;background:#ef4444;border-radius:50%;margin-right:4px;vertical-align:middle;margin-bottom:1px;"></span>No Key`;
                    badge.style.background = '#fee2e2';
                    badge.style.color = '#ef4444';
                }
            } catch (e) {
                badge.innerHTML = `<span style="display:inline-block;width:4px;height:4px;background:#ca8a04;border-radius:50%;margin-right:4px;vertical-align:middle;margin-bottom:1px;"></span>Error`;
                badge.style.background = '#fef08a';
                badge.style.color = '#ca8a04';
            }
        }
    }
"""

content = content.replace("// Load existing settings", verify_fn + "\n    // Load existing settings")

content = content.replace("setVal('deepseek-api-key', s.deepseek_api_key);", "setVal('deepseek-api-key', s.deepseek_api_key);\n        verifyAllAIKeys();")

content = content.replace("setTimeout(() => { geminiStatus.style.display = 'none'; }, 3000);\n\n                }", "setTimeout(() => { geminiStatus.style.display = 'none'; }, 3000);\n\n                }\n                verifyAllAIKeys();")

with open('xcomic.xyz/assets/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('Modified app.js')
