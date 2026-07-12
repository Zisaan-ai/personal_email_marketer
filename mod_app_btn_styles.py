import sys

with open('frontend/assets/app.js', encoding='utf-8') as f:
    text = f.read()

# Replace the specific button HTML blocks to make them flex:1 to match the layout!

old_cold_pause = """<button class="btn" style="padding:12px 24px;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;font-weight:600;display:flex;align-items:center;" onclick="pauseCampaign('${c.id}')">"""
new_cold_pause = """<button class="btn" style="padding:12px 24px;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;font-weight:600;display:flex;align-items:center;flex:1;justify-content:center;" onclick="pauseCampaign('${c.id}')">"""

old_cold_resume = """<button class="btn" style="padding:12px 24px;background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;font-weight:600;display:flex;align-items:center;" onclick="resumeCampaign('${c.id}')">"""
new_cold_resume = """<button class="btn" style="padding:12px 24px;background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;font-weight:600;display:flex;align-items:center;flex:1;justify-content:center;" onclick="resumeCampaign('${c.id}')">"""

old_vb_pause = """<button class="btn" style="padding:16px 32px;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;font-weight:600;display:flex;align-items:center;" onclick="pauseCampaign('${c.id}')">"""
new_vb_pause = """<button class="btn" style="padding:16px 32px;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;font-weight:600;display:flex;align-items:center;flex:1;justify-content:center;" onclick="pauseCampaign('${c.id}')">"""

old_vb_resume = """<button class="btn" style="padding:16px 32px;background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;font-weight:600;display:flex;align-items:center;" onclick="resumeCampaign('${c.id}')">"""
new_vb_resume = """<button class="btn" style="padding:16px 32px;background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;font-weight:600;display:flex;align-items:center;flex:1;justify-content:center;" onclick="resumeCampaign('${c.id}')">"""

text = text.replace(old_cold_pause, new_cold_pause)
text = text.replace(old_cold_resume, new_cold_resume)
text = text.replace(old_vb_pause, new_vb_pause)
text = text.replace(old_vb_resume, new_vb_resume)

with open('frontend/assets/app.js', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated button styling!")
