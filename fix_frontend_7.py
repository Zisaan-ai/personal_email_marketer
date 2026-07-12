import sys

with open('frontend/assets/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_js = """window.saveSchedule = async function() {
    if (!window.currentCampaignId) {
        showToast('Please Launch the campaign first before saving the schedule.', 'error');
        return;
    }"""

new_js = """window.saveSchedule = async function() {
    if (!window.currentCampaignId) {
        showToast('Schedule settings will be saved automatically when you Launch the campaign!', 'success');
        return;
    }"""

if old_js in content:
    content = content.replace(old_js, new_js)

with open('frontend/assets/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Pass 7 frontend done")
