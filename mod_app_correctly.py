with open('frontend/assets/app.js', encoding='utf-8') as f:
    text = f.read()

vb_orig = '''    const statusEl = document.getElementById('vb-analytics-status');
    const cStatus = c.status || 'Draft';
    if (statusEl) {
        statusEl.textContent = cStatus;
        statusEl.style.background = cStatus.toLowerCase() === 'completed' ? '#ecfdf5' : (cStatus.toLowerCase() === 'failed' ? '#fef2f2' : '#e0e7ff');
        statusEl.style.color = cStatus.toLowerCase() === 'completed' ? '#059669' : (cStatus.toLowerCase() === 'failed' ? '#dc2626' : '#4f46e5');
    }'''

vb_new = '''    const statusEl = document.getElementById('vb-analytics-status');
    const actionsEl = document.getElementById('vb-analytics-actions');
    const cStatus = c.status || 'Draft';
    if (statusEl) {
        statusEl.textContent = cStatus;
        statusEl.style.background = cStatus.toLowerCase() === 'completed' ? '#ecfdf5' : (cStatus.toLowerCase() === 'failed' ? '#fef2f2' : '#e0e7ff');
        statusEl.style.color = cStatus.toLowerCase() === 'completed' ? '#059669' : (cStatus.toLowerCase() === 'failed' ? '#dc2626' : '#4f46e5');
    }
    if (actionsEl) {
        const st = cStatus.toLowerCase();
        let html = '';
        if (st === 'processing' || st === 'scheduled') {
            html = `<button class="btn" style="padding:6px 24px;border-radius:24px;background:#ecfdf5;border:1px solid #a7f3d0;display:flex;align-items:center;justify-content:center;opacity:0.7;margin-right:8px;" onclick="pauseCampaign('${c.id}')" title="Pause Campaign"><i class="fa-solid fa-pause" style="color:#059669;font-size:16px;"></i></button>`;
        } else if (['paused', 'completed', 'failed', 'draft', 'pending'].includes(st)) {
            html = `<button class="btn" style="padding:6px 24px;border-radius:24px;background:#ecfdf5;border:1px solid #a7f3d0;display:flex;align-items:center;justify-content:center;" onclick="resumeCampaign('${c.id}')" title="Resume/Restart"><i class="fa-solid fa-play" style="color:#059669;font-size:16px;"></i></button>`;
        }
        actionsEl.innerHTML = html;
    }'''

cold_orig = '''    const statusEl = document.getElementById('cold-analytics-status');
    const cStatus = c.status || 'Draft';
    if (statusEl) {
        statusEl.textContent = cStatus;
        statusEl.style.background = cStatus.toLowerCase() === 'completed' ? '#ecfdf5' : (cStatus.toLowerCase() === 'failed' ? '#fef2f2' : '#e0e7ff');
        statusEl.style.color = cStatus.toLowerCase() === 'completed' ? '#059669' : (cStatus.toLowerCase() === 'failed' ? '#dc2626' : '#4f46e5');
    }'''

cold_new = '''    const statusEl = document.getElementById('cold-analytics-status');
    const actionsEl = document.getElementById('cold-analytics-actions');
    const cStatus = c.status || 'Draft';
    if (statusEl) {
        statusEl.textContent = cStatus;
        statusEl.style.background = cStatus.toLowerCase() === 'completed' ? '#ecfdf5' : (cStatus.toLowerCase() === 'failed' ? '#fef2f2' : '#e0e7ff');
        statusEl.style.color = cStatus.toLowerCase() === 'completed' ? '#059669' : (cStatus.toLowerCase() === 'failed' ? '#dc2626' : '#4f46e5');
    }
    if (actionsEl) {
        const st = cStatus.toLowerCase();
        let html = '';
        if (st === 'processing' || st === 'scheduled') {
            html = `<button class="btn" style="padding:6px 24px;border-radius:24px;background:#ecfdf5;border:1px solid #a7f3d0;display:flex;align-items:center;justify-content:center;opacity:0.7;margin-right:8px;" onclick="pauseCampaign('${c.id}')" title="Pause Campaign"><i class="fa-solid fa-pause" style="color:#059669;font-size:16px;"></i></button>`;
        } else if (['paused', 'completed', 'failed', 'draft', 'pending'].includes(st)) {
            html = `<button class="btn" style="padding:6px 24px;border-radius:24px;background:#ecfdf5;border:1px solid #a7f3d0;display:flex;align-items:center;justify-content:center;" onclick="resumeCampaign('${c.id}')" title="Resume/Restart"><i class="fa-solid fa-play" style="color:#059669;font-size:16px;"></i></button>`;
        }
        actionsEl.innerHTML = html;
    }'''

text = text.replace(vb_orig, vb_new)
text = text.replace(cold_orig, cold_new)

with open('frontend/assets/app.js', 'w', encoding='utf-8') as f:
    f.write(text)

with open('frontend/index.html', encoding='utf-8') as f:
    idx_text = f.read()

idx_text = idx_text.replace('app.js?v=3005', 'app.js?v=3006')

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(idx_text)

print('Updated properly')
