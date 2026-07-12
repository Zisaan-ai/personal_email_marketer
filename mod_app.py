import re

with open('frontend/assets/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

populate_vb_func = """
window.populateVbAnalytics = function(id) {
    if (!window.lastFetchedCampaigns) return;
    const c = window.lastFetchedCampaigns.find(x => x.id === id);
    if (!c) return;

    const statusEl = document.getElementById('vb-analytics-status');
    const cStatus = c.status || 'Draft';
    if (statusEl) {
        statusEl.textContent = cStatus;
        statusEl.style.background = cStatus.toLowerCase() === 'completed' ? '#ecfdf5' : (cStatus.toLowerCase() === 'failed' ? '#fef2f2' : '#e0e7ff');
        statusEl.style.color = cStatus.toLowerCase() === 'completed' ? '#059669' : (cStatus.toLowerCase() === 'failed' ? '#dc2626' : '#4f46e5');
    }

    const started = c.sent_count || 0;
    const opens = c.opens || 0;
    const clicks = c.clicks || 0;
    const openRate = started > 0 ? Math.round((opens / started) * 100) : 0;
    const clickRate = started > 0 ? Math.round((clicks / started) * 100) : 0;

    const setEl = (eid, val) => { const el = document.getElementById(eid); if (el) el.textContent = val; };
    setEl('vb-analytics-seq-started', started.toLocaleString());
    setEl('vb-analytics-open-rate', `${openRate}%`);
    setEl('vb-analytics-open-count', `(${opens.toLocaleString()} opens)`);
    setEl('vb-analytics-click-rate', `${clickRate}%`);
    setEl('vb-analytics-click-count', `(${clicks.toLocaleString()} clicks)`);
    
    // Fetch and render analytics leads table
    const tbody = document.getElementById('vb-analytics-leads-tbody');
    if (tbody) {
        tbody.innerHTML = '<tr><td colspan="3" style="text-align:center;padding:24px;color:var(--text-muted);">Loading leads...</td></tr>';
        apiCall('/campaigns/' + id + '/leads')
            .then(res => res.json())
            .then(leads => {
                tbody.innerHTML = '';
                if (!leads || leads.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="3" style="text-align:center;padding:24px;color:var(--text-muted);">No leads found for this campaign.</td></tr>';
                    return;
                }
                leads.forEach(l => {
                    const tr = document.createElement('tr');
                    const statusColor = (l.status === 'sent' || l.status === 'opened' || l.status === 'clicked') ? '#059669' : (l.status === 'bounced' ? '#dc2626' : (l.status === 'unsubscribed' ? '#ea580c' : '#64748b'));
                    tr.innerHTML = `
                        <td style="font-weight:600;color:var(--text);">${l.email || ''}</td>
                        <td>${l.name || '-'}</td>
                        <td><span style="font-size:12px; font-weight:600; color:${statusColor}; text-transform:capitalize;">${l.status || 'pending'}</span></td>
                    `;
                    tbody.appendChild(tr);
                });
            })
            .catch(err => {
                console.error('Error fetching leads:', err);
                tbody.innerHTML = '<tr><td colspan="3" style="text-align:center;padding:24px;color:var(--text-muted);">Error loading leads.</td></tr>';
            });
    }
}
"""

if 'window.populateVbAnalytics =' not in text:
    idx = text.find('window.populateColdAnalytics = function(id)')
    text = text[:idx] + populate_vb_func + '\n' + text[idx:]

# Now modify window.switchVbTab to call populateVbAnalytics
switch_logic = """
    // Show content
    if (targetContent) {
        targetContent.style.display = 'block';
    }
    
    if (tabName === 'analytics' && window.currentCampaignId) {
        window.populateVbAnalytics(window.currentCampaignId);
    }
};"""

if "window.populateVbAnalytics(window.currentCampaignId);" not in text:
    text = text.replace("""    // Show content\n    if (targetContent) {\n        targetContent.style.display = 'block';\n    }\n};""", switch_logic)

with open('frontend/assets/app.js', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated app.js with populateVbAnalytics')
