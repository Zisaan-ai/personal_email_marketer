with open('frontend/assets/app.js', encoding='utf-8') as f:
    text = f.read()

# Update pauseCampaign
pause_orig = '''            renderColdMailList();
            renderNewsletterList();
        } else {'''
pause_new = '''            renderColdMailList();
            renderNewsletterList();
            if (window.currentCampaignId === id) {
                if (document.getElementById('vb-tab-analytics') && document.getElementById('vb-tab-analytics').style.display !== 'none') {
                    if (typeof window.populateVbAnalytics === 'function') window.populateVbAnalytics(id);
                } else if (document.getElementById('cold-tab-analytics') && document.getElementById('cold-tab-analytics').style.display !== 'none') {
                    if (typeof window.populateColdAnalytics === 'function') window.populateColdAnalytics(id);
                }
            }
        } else {'''
text = text.replace(pause_orig, pause_new)

# Update populateVbAnalytics
vb_orig = '''        const statusEl = document.getElementById('vb-analytics-status');
        if (statusEl) {
            statusEl.textContent = c.status.toUpperCase();
            if (c.status === 'processing') {
                statusEl.style.background = '#e0e7ff';
                statusEl.style.color = '#4338ca';
            } else if (c.status === 'completed') {
                statusEl.style.background = '#dcfce7';
                statusEl.style.color = '#15803d';
            } else {
                statusEl.style.background = '#f1f5f9';
                statusEl.style.color = '#475569';
            }
        }'''
vb_new = '''        const statusEl = document.getElementById('vb-analytics-status');
        const actionsEl = document.getElementById('vb-analytics-actions');
        if (statusEl) {
            statusEl.textContent = c.status.toUpperCase();
            if (c.status === 'processing') {
                statusEl.style.background = '#e0e7ff';
                statusEl.style.color = '#4338ca';
            } else if (c.status === 'completed') {
                statusEl.style.background = '#dcfce7';
                statusEl.style.color = '#15803d';
            } else {
                statusEl.style.background = '#f1f5f9';
                statusEl.style.color = '#475569';
            }
        }
        if (actionsEl) {
            const st = c.status.toLowerCase();
            let html = '';
            if (st === 'processing' || st === 'scheduled') {
                html = `<button class="btn" style="padding:6px 24px;border-radius:24px;background:#ecfdf5;border:1px solid #a7f3d0;display:flex;align-items:center;justify-content:center;opacity:0.7;margin-right:8px;" onclick="pauseCampaign('${c.id}')" title="Pause Campaign"><i class="fa-solid fa-pause" style="color:#059669;font-size:16px;"></i></button>`;
            } else if (['paused', 'completed', 'failed'].includes(st)) {
                html = `<button class="btn" style="padding:6px 24px;border-radius:24px;background:#ecfdf5;border:1px solid #a7f3d0;display:flex;align-items:center;justify-content:center;" onclick="resumeCampaign('${c.id}')" title="Resume/Restart"><i class="fa-solid fa-play" style="color:#059669;font-size:16px;"></i></button>`;
            }
            actionsEl.innerHTML = html;
        }'''
text = text.replace(vb_orig, vb_new)

# Update populateColdAnalytics
cold_orig = '''        const statusEl = document.getElementById('cold-analytics-status');
        if (statusEl) {
            statusEl.textContent = c.status.toUpperCase();
            if (c.status === 'processing') {
                statusEl.style.background = '#e0e7ff';
                statusEl.style.color = '#4338ca';
            } else if (c.status === 'completed') {
                statusEl.style.background = '#dcfce7';
                statusEl.style.color = '#15803d';
            } else {
                statusEl.style.background = '#f1f5f9';
                statusEl.style.color = '#475569';
            }
        }'''
cold_new = '''        const statusEl = document.getElementById('cold-analytics-status');
        const actionsEl = document.getElementById('cold-analytics-actions');
        if (statusEl) {
            statusEl.textContent = c.status.toUpperCase();
            if (c.status === 'processing') {
                statusEl.style.background = '#e0e7ff';
                statusEl.style.color = '#4338ca';
            } else if (c.status === 'completed') {
                statusEl.style.background = '#dcfce7';
                statusEl.style.color = '#15803d';
            } else {
                statusEl.style.background = '#f1f5f9';
                statusEl.style.color = '#475569';
            }
        }
        if (actionsEl) {
            const st = c.status.toLowerCase();
            let html = '';
            if (st === 'processing' || st === 'scheduled') {
                html = `<button class="btn" style="padding:6px 24px;border-radius:24px;background:#ecfdf5;border:1px solid #a7f3d0;display:flex;align-items:center;justify-content:center;opacity:0.7;margin-right:8px;" onclick="pauseCampaign('${c.id}')" title="Pause Campaign"><i class="fa-solid fa-pause" style="color:#059669;font-size:16px;"></i></button>`;
            } else if (['paused', 'completed', 'failed'].includes(st)) {
                html = `<button class="btn" style="padding:6px 24px;border-radius:24px;background:#ecfdf5;border:1px solid #a7f3d0;display:flex;align-items:center;justify-content:center;" onclick="resumeCampaign('${c.id}')" title="Resume/Restart"><i class="fa-solid fa-play" style="color:#059669;font-size:16px;"></i></button>`;
            }
            actionsEl.innerHTML = html;
        }'''
text = text.replace(cold_orig, cold_new)

with open('frontend/assets/app.js', 'w', encoding='utf-8') as f:
    f.write(text)
