import sys

with open('frontend/assets/app.js', encoding='utf-8') as f:
    text = f.read()

vb_injection_target = "window.switchVbTab('design');"
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
        
        window.switchVbTab('design');
"""
if vb_injection_target in text:
    text = text.replace(vb_injection_target, vb_status_logic)
    with open('frontend/assets/app.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print('app.js updated successfully!')
else:
    print("VB injection target not found.")
