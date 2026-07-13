window.renderSendingAccountsSelector = async function(containerId, selectedIdsStr) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = '<div style="padding:10px;text-align:center;"><i class="fa-solid fa-spinner fa-spin"></i> Loading accounts...</div>';
    
    try {
        const res = await apiCall('/sending-accounts');
        if (!res.ok) {
            container.innerHTML = '<div style="color:var(--danger); font-size:13px;">Failed to load accounts.</div>';
            return;
        }
        const accounts = await res.json();
        
        let selectedIds = [];
        try {
            if (selectedIdsStr) selectedIds = JSON.parse(selectedIdsStr);
        } catch(e) {}
        
        if (!accounts || accounts.length === 0) {
            container.innerHTML = '<div style="font-size:13px; color:var(--text-muted);">No active sending accounts found. Auto-rotation will fail.</div>';
            return;
        }
        
        let html = '';
        accounts.forEach(acc => {
            const isChecked = selectedIds.includes(acc.id) ? 'checked' : '';
            html += 
                <label style="display:flex; align-items:center; gap:8px; cursor:pointer; font-size:13px; padding:4px 0;">
                    <input type="checkbox" class="sender-acc-checkbox" value=" + acc.id + "  + isChecked + >
                    <div>
                        <div style="font-weight:600; color:var(--p);"> + (acc.name || 'No Name') + </div>
                        <div style="color:var(--text-muted); font-size:11px;"> + acc.email + </div>
                    </div>
                </label>
            ;
        });
        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = '<div style="color:var(--danger); font-size:13px;">Error loading accounts.</div>';
    }
};

window.getSelectedSenderIds = function(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return null;
    const checked = Array.from(container.querySelectorAll('.sender-acc-checkbox:checked')).map(cb => cb.value);
    return checked.length > 0 ? JSON.stringify(checked) : null;
};
