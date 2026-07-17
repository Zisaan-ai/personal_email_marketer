import os

content = open('xcomic.xyz/index.html', encoding='utf-8').read()

badge = ' <span style="background:#fee2e2;color:#ef4444;font-size:9px;font-weight:700;padding:2px 6px;border-radius:4px;margin-left:6px;"><span style="display:inline-block;width:4px;height:4px;background:#ef4444;border-radius:50%;margin-right:4px;vertical-align:middle;margin-bottom:1px;"></span>No Key</span>'

# Gemini
content = content.replace('<div style="font-size:14px;font-weight:700;">Google Gemini</div>', '<div style="font-size:14px;font-weight:700;">Google Gemini' + badge + '</div>')
content = content.replace('Best for creative email writing', 'Free & powerful - great for AI emails')

# Groq
content = content.replace('<span style="font-size:14px;font-weight:700;">Groq</span>\n                                        <span style="background:#dcfce7;color:#059669;font-size:11px;font-weight:700;padding:2px 8px;border-radius:20px;">⚡ Recommended</span>', '<span style="font-size:14px;font-weight:700;">Groq</span>' + badge)
content = content.replace('Ultra-fast, free — best for cold email', 'Ultra-fast & free - ideal for cold email')

# OpenAI
content = content.replace('<span style="font-size:14px;font-weight:700;">OpenAI (ChatGPT)</span>', '<span style="font-size:14px;font-weight:700;">OpenAI (ChatGPT)</span>' + badge)
content = content.replace('Industry standard AI models', 'Industry-leading AI - premium quality')

# Anthropic
content = content.replace('<span style="font-size:14px;font-weight:700;">Anthropic (Claude)</span>', '<span style="font-size:14px;font-weight:700;">Anthropic (Claude)</span>' + badge)
content = content.replace('Excellent for writing & coding', 'Best for writing, analysis & long emails')

# DeepSeek
content = content.replace('<span style="font-size:14px;font-weight:700;">DeepSeek</span>', '<span style="font-size:14px;font-weight:700;">DeepSeek</span>' + badge)
content = content.replace('Cost-effective & powerful', 'Cost-effective & highly capable')

# Button
content = content.replace('<i class="fa-solid fa-floppy-disk" style="margin-right:8px;"></i>Save AI Keys', '<i class="fa-solid fa-lock" style="margin-right:8px;"></i>Save AI Keys')

open('xcomic.xyz/index.html', 'w', encoding='utf-8').write(content)
print("Done")
