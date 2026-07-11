const ACCOUNTS = {
    list: [],
    
    init: function() {
        this.fetchAccounts();
    },
    
    fetchAccounts: async function() {
        try {
            const res = await fetch(API_URL + '/sending-accounts', {
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
            });
            if(res.ok) {
                this.list = await res.json();
                this.render();
            }
        } catch(e) {
            console.error("Failed to fetch accounts", e);
        }
    },
    
    render: function() {
        const tbody = document.getElementById('accounts-table-body');
        tbody.innerHTML = '';
        if(this.list.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" style="padding:32px;text-align:center;color:var(--text-muted);">No accounts connected yet. Setup your first sending account to start delivering campaigns.</td></tr>`;
            return;
        }
        
        this.list.forEach(acc => {
            const statusBadge = acc.is_active 
                ? `<span style="background:#dcfce7;color:#059669;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:700;">Active</span>`
                : `<span style="background:#f1f5f9;color:#475569;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:700;">Paused</span>`;
                
            const toggleAction = acc.is_active
                ? `<button onclick="ACCOUNTS.toggleStatus('${acc.id}', false)" class="btn" style="padding:6px 12px;font-size:13px;margin-right:8px;"><i class="fa-solid fa-pause"></i> Pause</button>`
                : `<button onclick="ACCOUNTS.toggleStatus('${acc.id}', true)" class="btn" style="padding:6px 12px;font-size:13px;margin-right:8px;"><i class="fa-solid fa-play"></i> Resume</button>`;

            const healthScore = acc.health_score ?? 100;
            let healthBadge = '';
            if (healthScore >= 90) {
                healthBadge = `<span style="color:#059669; font-weight:600;"><i class="fa-solid fa-heart-pulse"></i> ${healthScore}%</span>`;
            } else if (healthScore >= 70) {
                healthBadge = `<span style="color:#f59e0b; font-weight:600;"><i class="fa-solid fa-heart-pulse"></i> ${healthScore}%</span>`;
            } else {
                healthBadge = `<span style="color:#ef4444; font-weight:600;"><i class="fa-solid fa-heart-crack"></i> ${healthScore}%</span>`;
            }

            const tr = document.createElement('tr');
            tr.style.borderBottom = "1px solid var(--border)";
            tr.innerHTML = `
                <td style="padding:16px 24px;font-weight:600;">${acc.name || '-'}</td>
                <td style="padding:16px 24px;">${acc.email}</td>
                <td style="padding:16px 24px;">${acc.daily_limit}</td>
                <td style="padding:16px 24px;">${acc.sent_today}</td>
                <td style="padding:16px 24px;">${healthBadge}</td>
                <td style="padding:16px 24px;">${statusBadge}</td>
                <td style="padding:16px 24px;text-align:right;">
                    ${toggleAction}
                    <button onclick="ACCOUNTS.editAccount('${acc.id}')" class="btn" style="padding:6px 12px;font-size:13px;margin-right:8px;"><i class="fa-solid fa-pen"></i></button>
                    <button onclick="ACCOUNTS.deleteAccount('${acc.id}')" class="btn" style="padding:6px 12px;font-size:13px;color:#ef4444;border-color:#fecaca;"><i class="fa-solid fa-trash"></i></button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    },
    
    showAddModal: function() {
        document.getElementById('acc-id').value = '';
        document.getElementById('acc-modal-title').textContent = 'Add Sending Account';
        document.getElementById('save-account-btn').textContent = 'Connect Account';
        ['acc-name','acc-email','acc-password'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = '';
        });
        document.getElementById('acc-daily-limit').value = '500';
        document.getElementById('acc-warmup-enabled').checked = false;
        document.getElementById('acc-warmup-limit').value = '5';
        document.getElementById('acc-warmup-increment').value = '2';
        document.getElementById('add-account-modal').style.display = 'flex';
    },

    editAccount: function(id) {
        const acc = this.list.find(a => a.id === id);
        if(!acc) return;
        document.getElementById('acc-id').value = acc.id;
        document.getElementById('acc-modal-title').textContent = 'Edit Sending Account';
        document.getElementById('save-account-btn').textContent = 'Save Changes';
        
        document.getElementById('acc-name').value = acc.name || '';
        document.getElementById('acc-email').value = acc.email || '';
        document.getElementById('acc-password').value = acc.smtp_password || '';
        document.getElementById('acc-daily-limit').value = acc.daily_limit || 500;
        document.getElementById('acc-warmup-enabled').checked = acc.warmup_enabled || false;
        document.getElementById('acc-warmup-limit').value = acc.warmup_daily_limit || 5;
        document.getElementById('acc-warmup-increment').value = acc.warmup_increment_per_day || 2;
        
        document.getElementById('add-account-modal').style.display = 'flex';
    },
    
    saveAccount: async function() {
        const email = document.getElementById('acc-email').value;
        const password = document.getElementById('acc-password').value.replace(/\s+/g, '');
        
        const payload = {
            name: document.getElementById('acc-name').value,
            email: email,
            smtp_server: 'smtp.gmail.com',
            smtp_port: 587,
            smtp_username: email,
            smtp_password: password,
            daily_limit: parseInt(document.getElementById('acc-daily-limit').value) || 500,
            imap_server: 'imap.gmail.com',
            imap_port: 993,
            imap_password: password,
            warmup_enabled: document.getElementById('acc-warmup-enabled')?.checked || false,
            warmup_daily_limit: parseInt(document.getElementById('acc-warmup-limit')?.value) || 5,
            warmup_increment_per_day: parseInt(document.getElementById('acc-warmup-increment')?.value) || 2
        };
        
        if(!payload.email || !payload.smtp_password) {
            alert("Email and App Password are required!");
            return;
        }

        const btn = document.getElementById('save-account-btn');
        if (btn) { btn.disabled = true; btn.textContent = 'Saving...'; }
        
        try {
            const token = localStorage.getItem('token');
            const accId = document.getElementById('acc-id').value;
            const url = accId ? API_URL + '/sending-accounts/' + accId : API_URL + '/sending-accounts';
            const method = accId ? 'PUT' : 'POST';
            
            const res = await fetch(url, {
                method: method,
                headers: { 
                    'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            if(res.ok) {
                document.getElementById('add-account-modal').style.display = 'none';
                // Reset form
                ['acc-name','acc-email','acc-password'].forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.value = '';
                });
                this.fetchAccounts();
            } else {
                const errData = await res.json().catch(() => ({ detail: 'Unknown error' }));
                const msg = errData.detail || JSON.stringify(errData);
                alert('Error: ' + msg);
            }
        } catch(e) {
            console.error("Add account error", e);
            alert('Network error: ' + e.message);
        } finally {
            if (btn) { btn.disabled = false; btn.textContent = 'Save Account'; }
        }
    },
    
    toggleStatus: async function(id, isActive) {
        try {
            const res = await fetch(API_URL + '/sending-accounts/' + id, {
                method: 'PATCH',
                headers: { 
                    'Authorization': 'Bearer ' + localStorage.getItem('token'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ is_active: isActive })
            });
            if(res.ok) {
                this.fetchAccounts();
            }
        } catch(e) {
            console.error("Toggle status error", e);
        }
    },
    
    deleteAccount: async function(id) {
        if(!confirm("Are you sure you want to delete this account?")) return;
        try {
            const res = await fetch(API_URL + '/sending-accounts/' + id, {
                method: 'DELETE',
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
            });
            if(res.ok) {
                this.fetchAccounts();
            }
        } catch(e) {
            console.error("Delete account error", e);
        }
    }
};

// Initialize accounts list when nav is clicked or app loads
document.addEventListener('DOMContentLoaded', () => {
    // Attach to existing nav click listener if possible, or just init here.
    // It's safe to init here if they are logged in, but token might not be ready.
});