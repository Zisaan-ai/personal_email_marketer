import sys

with open('frontend/assets/app.js', encoding='utf-8') as f:
    text = f.read()

# 1. Cold Mail block injection
cold_injection_target = "window.switchColdTab('sequences');\n\n        showToast('Cold Mail sequence loaded for editing');"
cold_status_logic = """
        const coldStatus = c.status || 'draft';
        const sendBtn = document.getElementById('inst-send-seq-btn');
        const actionsDiv = document.getElementById('cold-status-actions');
        if (actionsDiv) {
            if (coldStatus.toLowerCase() === 'processing' || coldStatus.toLowerCase() === 'scheduled') {
                if (sendBtn) sendBtn.style.display = 'none';
                actionsDiv.style.display = 'inline-flex';
                actionsDiv.innerHTML = `<button class="btn" style="padding:12px 24px;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;font-weight:600;display:flex;align-items:center;" onclick="pauseCampaign('${c.id}')"><i class="fa-solid fa-pause" style="color:#d97706;margin-right:8px;"></i>Pause Campaign</button>`;
            } else if (['paused', 'failed', 'completed'].includes(coldStatus.toLowerCase())) {
                if (sendBtn) sendBtn.style.display = 'none';
                actionsDiv.style.display = 'inline-flex';
                actionsDiv.innerHTML = `<button class="btn" style="padding:12px 24px;background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;font-weight:600;display:flex;align-items:center;" onclick="resumeCampaign('${c.id}')"><i class="fa-solid fa-play" style="color:#059669;margin-right:8px;"></i>Resume Campaign</button>`;
            } else {
                if (sendBtn) sendBtn.style.display = 'inline-block';
                actionsDiv.style.display = 'none';
                actionsDiv.innerHTML = '';
            }
        }
        
        window.switchColdTab('sequences');
        showToast('Cold Mail sequence loaded for editing');
"""
if cold_injection_target in text:
    text = text.replace(cold_injection_target, cold_status_logic)
else:
    print("Cold injection target not found.")


# 2. Visual Builder block injection
vb_injection_target = "window.switchVBTab('design');"
vb_status_logic = """
        const vbStatus = c.status || 'draft';
        const vbSendBtn = document.getElementById('send-btn');
        const vbActionsDiv = document.getElementById('vb-status-actions');
        if (vbActionsDiv) {
            if (vbStatus.toLowerCase() === 'processing' || vbStatus.toLowerCase() === 'scheduled') {
                if (vbSendBtn) vbSendBtn.style.display = 'none';
                vbActionsDiv.style.display = 'inline-flex';
                vbActionsDiv.innerHTML = `<button class="btn" style="padding:16px 32px;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;font-weight:600;display:flex;align-items:center;" onclick="pauseCampaign('${c.id}')"><i class="fa-solid fa-pause" style="color:#d97706;margin-right:8px;"></i>Pause Campaign</button>`;
            } else if (['paused', 'failed', 'completed'].includes(vbStatus.toLowerCase())) {
                if (vbSendBtn) vbSendBtn.style.display = 'none';
                vbActionsDiv.style.display = 'inline-flex';
                vbActionsDiv.innerHTML = `<button class="btn" style="padding:16px 32px;background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;font-weight:600;display:flex;align-items:center;" onclick="resumeCampaign('${c.id}')"><i class="fa-solid fa-play" style="color:#059669;margin-right:8px;"></i>Resume Campaign</button>`;
            } else {
                if (vbSendBtn) vbSendBtn.style.display = 'inline-block';
                vbActionsDiv.style.display = 'none';
                vbActionsDiv.innerHTML = '';
            }
        }
        
        window.switchVBTab('design');
"""
if vb_injection_target in text:
    text = text.replace(vb_injection_target, vb_status_logic)
else:
    print("VB injection target not found.")

with open('frontend/assets/app.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('app.js updated successfully!')
