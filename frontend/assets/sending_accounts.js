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
            // Status badge with auto-pause detection
            let statusBadge;
            if (acc.auto_paused) {
                statusBadge = `<span style="background:#fef2f2;color:#dc2626;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:700;">⚠️ Auto-Paused</span>`;
            } else if (acc.is_active) {
                statusBadge = `<span style="background:#dcfce7;color:#059669;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:700;">Active</span>`;
            } else {
                statusBadge = `<span style="background:#f1f5f9;color:#475569;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:700;">Paused</span>`;
            }
                
            // Toggle action with reactivate for auto-paused
            let toggleAction;
            if (acc.auto_paused) {
                toggleAction = `<button onclick="ACCOUNTS.reactivateAccount('${acc.id}')" class="btn" style="padding:6px 12px;font-size:13px;margin-right:8px;background:#059669;color:white;border:none;"><i class="fa-solid fa-rotate-right"></i> Reactivate</button>`;
            } else if (acc.is_active) {
                toggleAction = `<button onclick="ACCOUNTS.toggleStatus('${acc.id}', false)" class="btn" style="padding:6px 12px;font-size:13px;margin-right:8px;"><i class="fa-solid fa-pause"></i> Pause</button>`;
            } else {
                toggleAction = `<button onclick="ACCOUNTS.toggleStatus('${acc.id}', true)" class="btn" style="padding:6px 12px;font-size:13px;margin-right:8px;"><i class="fa-solid fa-play"></i> Resume</button>`;
            }

            // Health score with animated bar
            const healthScore = acc.health_score ?? 100;
            let healthColor, healthIcon;
            if (healthScore >= 90) {
                healthColor = '#059669';
                healthIcon = 'fa-heart-pulse';
            } else if (healthScore >= 70) {
                healthColor = '#f59e0b';
                healthIcon = 'fa-heart-pulse';
            } else if (healthScore >= 50) {
                healthColor = '#f97316';
                healthIcon = 'fa-heart-crack';
            } else {
                healthColor = '#ef4444';
                healthIcon = 'fa-heart-crack';
            }

            const healthBar = `
                <div style="display:flex;align-items:center;gap:8px;">
                    <div style="width:80px;height:6px;background:#e2e8f0;border-radius:3px;overflow:hidden;">
                        <div style="width:${healthScore}%;height:100%;background:${healthColor};border-radius:3px;transition:width 0.5s ease;"></div>
                    </div>
                    <span style="color:${healthColor};font-weight:600;font-size:13px;"><i class="fa-solid ${healthIcon}"></i> ${healthScore}%</span>
                </div>
            `;

            // Suggested limit badge - only show when smart limit is ON
            const suggestedLimit = acc.suggested_daily_limit || acc.daily_limit;
            const limitBadge = acc.smart_limit_enabled && suggestedLimit < acc.daily_limit
                ? `<span style="font-size:11px;color:#f59e0b;display:block;margin-top:2px;">📊 Suggested: ${suggestedLimit}/day</span>`
                : '';

            // Domain health badges
            let domainBadges = '';
            if (acc.domain_health) {
                const dh = acc.domain_health;
                domainBadges = `<div style="display:flex;gap:4px;margin-top:4px;flex-wrap:wrap;">
                    <span style="font-size:10px;padding:2px 6px;border-radius:4px;background:${dh.has_spf ? '#dcfce7' : '#fef2f2'};color:${dh.has_spf ? '#059669' : '#dc2626'};">SPF ${dh.has_spf ? '✓' : '✗'}</span>
                    <span style="font-size:10px;padding:2px 6px;border-radius:4px;background:${dh.has_dkim ? '#dcfce7' : '#fef2f2'};color:${dh.has_dkim ? '#059669' : '#dc2626'};">DKIM ${dh.has_dkim ? '✓' : '✗'}</span>
                    <span style="font-size:10px;padding:2px 6px;border-radius:4px;background:${dh.has_dmarc ? '#dcfce7' : '#fef2f2'};color:${dh.has_dmarc ? '#059669' : '#dc2626'};">DMARC ${dh.has_dmarc ? '✓' : '✗'}</span>
                    ${dh.is_blacklisted ? '<span style="font-size:10px;padding:2px 6px;border-radius:4px;background:#fef2f2;color:#dc2626;">⛔ Blacklisted</span>' : ''}
                </div>`;
            }

            // Auto-pause reason tooltip
            const pauseReason = acc.auto_paused_reason 
                ? `<div style="font-size:11px;color:#dc2626;margin-top:4px;">${acc.auto_paused_reason}</div>` 
                : '';

            // Stats summary
            const totalSent = acc.total_sent || 0;
            const totalBounced = acc.total_bounced || 0;
            const bounceRate = totalSent > 0 ? ((totalBounced / totalSent) * 100).toFixed(1) : '0.0';
            const statsLine = totalSent > 0 
                ? `<div style="font-size:11px;color:var(--text-muted);margin-top:2px;">📧 ${totalSent} sent · 💥 ${bounceRate}% bounce</div>` 
                : '';

            const tr = document.createElement('tr');
            tr.style.borderBottom = "1px solid var(--border)";
            tr.innerHTML = `
                <td style="padding:16px 24px;">
                    <div style="font-weight:600;">${acc.name || '-'}</div>
                    ${statsLine}
                </td>
                <td style="padding:16px 24px;">
                    <div>${acc.email}</div>
                    ${domainBadges}
                </td>
                <td style="padding:16px 24px;">
                    <div>${acc.daily_limit}</div>
                    ${limitBadge}
                    <div style="margin-top:6px;display:flex;flex-direction:column;gap:4px;">
                        <label style="display:flex;align-items:center;gap:5px;cursor:pointer;font-size:11px;color:var(--text-muted);" title="Smart Limit: System automatically reduces daily limit based on account age & health to protect deliverability">
                            <div onclick="ACCOUNTS.toggleSmartLimit('${acc.id}', ${!acc.smart_limit_enabled})" style="width:32px;height:18px;border-radius:9px;background:${acc.smart_limit_enabled ? '#6366f1' : 'var(--border)'};position:relative;cursor:pointer;transition:background 0.2s;">
                                <div style="width:14px;height:14px;background:#fff;border-radius:50%;position:absolute;top:2px;left:${acc.smart_limit_enabled ? '16px' : '2px'};transition:left 0.2s;"></div>
                            </div>
                            Smart Limit
                        </label>
                        <label style="display:flex;align-items:center;gap:5px;cursor:pointer;font-size:11px;color:var(--text-muted);" title="Warmup: Automatically exchange emails with the warmup network to build sender reputation">
                            <div onclick="ACCOUNTS.toggleWarmup('${acc.id}', ${!acc.warmup_enabled})" style="width:32px;height:18px;border-radius:9px;background:${acc.warmup_enabled ? '#f59e0b' : 'var(--border)'};position:relative;cursor:pointer;transition:background 0.2s;">
                                <div style="width:14px;height:14px;background:#fff;border-radius:50%;position:absolute;top:2px;left:${acc.warmup_enabled ? '16px' : '2px'};transition:left 0.2s;"></div>
                            </div>
                            Warmup ${acc.warmup_enabled ? `(${acc.warmup_sent_today || 0}/${acc.warmup_daily_limit || 5})` : ''}
                        </label>
                    </div>
                </td>
                <td style="padding:16px 24px;">${acc.sent_today}</td>
                <td style="padding:16px 24px;">${healthBar}</td>
                <td style="padding:16px 24px;">
                    ${statusBadge}
                    ${pauseReason}
                </td>
                <td style="padding:16px 24px;text-align:right;">
                    <div style="display:flex;gap:4px;justify-content:flex-end;flex-wrap:wrap;">
                        ${toggleAction}
                        <button onclick="ACCOUNTS.showHealthDetail('${acc.id}')" class="btn" style="padding:6px 12px;font-size:13px;" title="Health Details"><i class="fa-solid fa-chart-line"></i></button>
                        <button onclick="ACCOUNTS.editAccount('${acc.id}')" class="btn" style="padding:6px 12px;font-size:13px;"><i class="fa-solid fa-pen"></i></button>
                        <button onclick="ACCOUNTS.deleteAccount('${acc.id}')" class="btn" style="padding:6px 12px;font-size:13px;color:#ef4444;border-color:#fecaca;"><i class="fa-solid fa-trash"></i></button>
                    </div>
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
        document.getElementById('acc-warmup-limit').value = '5';
        document.getElementById('acc-warmup-increment').value = '2';
        document.getElementById('acc-smart-warmup-enabled').checked = false;
        document.getElementById('manual-warmup-settings').style.display = 'grid';
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
        document.getElementById('acc-password').value = ''; // Don't prefill password for security
        document.getElementById('acc-password').placeholder = '(Leave blank to keep existing password)';
        document.getElementById('acc-daily-limit').value = acc.daily_limit || 500;
        document.getElementById('acc-warmup-limit').value = acc.warmup_daily_limit || 5;
        document.getElementById('acc-warmup-increment').value = acc.warmup_increment_per_day || 2;
        document.getElementById('acc-smart-warmup-enabled').checked = acc.smart_warmup_enabled || false;
        document.getElementById('manual-warmup-settings').style.display = (acc.smart_warmup_enabled || false) ? 'none' : 'grid';
        
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
            warmup_daily_limit: parseInt(document.getElementById('acc-warmup-limit')?.value) || 5,
            warmup_increment_per_day: parseInt(document.getElementById('acc-warmup-increment')?.value) || 2,
            smart_warmup_enabled: document.getElementById('acc-smart-warmup-enabled')?.checked || false
        };
        
        if(!payload.email || (!payload.smtp_password && !document.getElementById('acc-id').value)) {
            alert("Email and App Password are required for new accounts!");
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

    toggleSmartLimit: async function(id, enable) {
        try {
            const res = await fetch(API_URL + '/sending-accounts/' + id, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                },
                body: JSON.stringify({ smart_limit_enabled: enable })
            });
            if (res.ok) {
                this.fetchAccounts();
                if (window.showToast) showToast(enable ? 'Smart Limit enabled ✅' : 'Smart Limit disabled ✅', 'success');
            } else {
                const err = await res.json();
                alert('Error updating Smart Limit: ' + (err.detail || 'Unknown error'));
            }
        } catch(e) {
            console.error('toggleSmartLimit error', e);
            alert('Failed to update smart limit');
        }
    },

    toggleWarmup: async function(id, enable) {
        try {
            const res = await fetch(API_URL + '/sending-accounts/' + id, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                },
                body: JSON.stringify({ warmup_enabled: enable })
            });
            if (res.ok) {
                this.fetchAccounts();
                if (window.showToast) showToast(enable ? 'Warmup enabled ✅' : 'Warmup disabled ✅', 'success');
            } else {
                const err = await res.json();
                alert('Error updating Warmup: ' + (err.detail || 'Unknown error'));
            }
        } catch(e) {
            console.error('toggleWarmup error', e);
            alert('Failed to update warmup status');
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
    },

    // ============================================================
    // NEW: Reactivate auto-paused account
    // ============================================================
    reactivateAccount: async function(id) {
        if(!confirm("Reactivate this account? It was auto-paused due to poor health. Make sure to fix the underlying issue first.")) return;
        try {
            const res = await fetch(API_URL + '/sending-accounts/' + id + '/reactivate', {
                method: 'POST',
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
            });
            if(res.ok) {
                this.fetchAccounts();
            } else {
                const err = await res.json().catch(() => ({}));
                alert(err.detail || 'Failed to reactivate');
            }
        } catch(e) {
            console.error("Reactivate error", e);
        }
    },

    // ============================================================
    // NEW: Show detailed health modal with analytics
    // ============================================================
    showHealthDetail: async function(id) {
        const acc = this.list.find(a => a.id === id);
        if (!acc) return;

        // Fetch detailed health report
        let healthData = null;
        let statsData = null;
        try {
            const [healthRes, statsRes] = await Promise.all([
                fetch(API_URL + '/account-health/' + id, {
                    headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
                }),
                fetch(API_URL + '/account-stats/' + id + '?days=30', {
                    headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
                })
            ]);
            if (healthRes.ok) healthData = await healthRes.json();
            if (statsRes.ok) statsData = await statsRes.json();
        } catch(e) {
            console.error("Health fetch error", e);
        }

        // Build modal content
        const h = healthData || {};
        const metrics = h.metrics || {};
        const recs = h.recommendations || [];

        // Health color
        let healthColor = '#059669';
        const score = h.health_score || 100;
        if (score < 50) healthColor = '#ef4444';
        else if (score < 70) healthColor = '#f97316';
        else if (score < 90) healthColor = '#f59e0b';

        let recsHtml = recs.map(r => `<li style="margin-bottom:6px;font-size:13px;color:var(--text-muted);">💡 ${r}</li>`).join('');

        let domainCheckBtn = '';
        if (acc.email && acc.email.includes('@')) {
            const domain = acc.email.split('@')[1];
            domainCheckBtn = `<button onclick="ACCOUNTS.checkDomainHealth('${domain}')" class="btn" style="margin-top:12px;padding:8px 16px;font-size:13px;"><i class="fa-solid fa-globe"></i> Check Domain Health (${domain})</button>`;
        }

        const modalHtml = `
            <div style="position:fixed;inset:0;background:rgba(15,23,42,0.6);z-index:9999;backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;" id="health-detail-modal" onclick="if(event.target===this)this.remove()">
                <div style="background:var(--bg);padding:32px;border-radius:16px;width:100%;max-width:650px;max-height:90vh;overflow-y:auto;box-shadow:0 20px 25px -5px rgba(0,0,0,0.1);border:1px solid rgba(255,255,255,0.2);">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;">
                        <h2 style="font-size:20px;font-weight:700;"><i class="fa-solid fa-heart-pulse" style="color:${healthColor};margin-right:8px;"></i>Account Health: ${acc.email}</h2>
                        <button onclick="document.getElementById('health-detail-modal').remove()" style="background:transparent;border:none;color:var(--text-muted);font-size:20px;cursor:pointer;"><i class="fa-solid fa-xmark"></i></button>
                    </div>

                    <!-- Health Score Ring -->
                    <div style="display:flex;align-items:center;gap:24px;margin-bottom:24px;padding:20px;background:var(--surface);border-radius:12px;border:1px solid var(--border);">
                        <div style="position:relative;width:100px;height:100px;">
                            <svg viewBox="0 0 36 36" style="width:100%;height:100%;transform:rotate(-90deg);">
                                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#e2e8f0" stroke-width="3"/>
                                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="${healthColor}" stroke-width="3" stroke-dasharray="${score}, 100" style="transition:stroke-dasharray 1s ease;"/>
                            </svg>
                            <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:800;color:${healthColor};">${score}</div>
                        </div>
                        <div>
                            <div style="font-size:18px;font-weight:700;margin-bottom:4px;">${h.status_label || 'Unknown'}</div>
                            <div style="font-size:13px;color:var(--text-muted);">Suggested daily limit: <strong>${h.suggested_daily_limit || '-'}/day</strong></div>
                            ${h.auto_paused ? `<div style="color:#dc2626;font-size:13px;margin-top:4px;">⚠️ ${h.auto_paused_reason || 'Auto-paused'}</div>` : ''}
                        </div>
                    </div>

                    <!-- Metrics Grid -->
                    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:24px;">
                        <div style="background:var(--surface);padding:16px;border-radius:10px;text-align:center;border:1px solid var(--border);">
                            <div style="font-size:22px;font-weight:800;color:var(--p);">${metrics.total_sent || 0}</div>
                            <div style="font-size:12px;color:var(--text-muted);margin-top:4px;">Total Sent</div>
                        </div>
                        <div style="background:var(--surface);padding:16px;border-radius:10px;text-align:center;border:1px solid var(--border);">
                            <div style="font-size:22px;font-weight:800;color:#ef4444;">${metrics.total_bounced || 0}</div>
                            <div style="font-size:12px;color:var(--text-muted);margin-top:4px;">Bounced (${metrics.bounce_rate || 0}%)</div>
                        </div>
                        <div style="background:var(--surface);padding:16px;border-radius:10px;text-align:center;border:1px solid var(--border);">
                            <div style="font-size:22px;font-weight:800;color:#059669;">${metrics.total_opened || 0}</div>
                            <div style="font-size:12px;color:var(--text-muted);margin-top:4px;">Opened (${metrics.open_rate || 0}%)</div>
                        </div>
                        <div style="background:var(--surface);padding:16px;border-radius:10px;text-align:center;border:1px solid var(--border);">
                            <div style="font-size:22px;font-weight:800;color:#8b5cf6;">${metrics.total_replied || 0}</div>
                            <div style="font-size:12px;color:var(--text-muted);margin-top:4px;">Replied (${metrics.reply_rate || 0}%)</div>
                        </div>
                    </div>

                    <!-- Analytics Chart -->
                    <div style="background:var(--surface);padding:20px;border-radius:12px;border:1px solid var(--border);margin-bottom:24px;">
                        <h3 style="font-size:15px;font-weight:600;margin-bottom:16px;"><i class="fa-solid fa-chart-area" style="color:var(--p);margin-right:6px;"></i>30-Day Activity</h3>
                        <canvas id="health-chart-canvas" height="200"></canvas>
                    </div>

                    <!-- Recommendations -->
                    <div style="background:var(--surface);padding:20px;border-radius:12px;border:1px solid var(--border);margin-bottom:16px;">
                        <h3 style="font-size:15px;font-weight:600;margin-bottom:12px;"><i class="fa-solid fa-lightbulb" style="color:#f59e0b;margin-right:6px;"></i>Recommendations</h3>
                        <ul style="list-style:none;padding:0;margin:0;">${recsHtml}</ul>
                    </div>

                    ${domainCheckBtn}
                </div>
            </div>
        `;

        // Remove existing modal if any
        const existing = document.getElementById('health-detail-modal');
        if (existing) existing.remove();

        document.body.insertAdjacentHTML('beforeend', modalHtml);

        // Render chart if stats available
        if (statsData && statsData.stats && statsData.stats.length > 0) {
            const ctx = document.getElementById('health-chart-canvas').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: statsData.stats.map(s => s.date.slice(5)), // MM-DD
                    datasets: [
                        {
                            label: 'Sent',
                            data: statsData.stats.map(s => s.sent),
                            borderColor: '#4f46e5',
                            backgroundColor: 'rgba(79,70,229,0.1)',
                            fill: true,
                            tension: 0.4
                        },
                        {
                            label: 'Bounced',
                            data: statsData.stats.map(s => s.bounced),
                            borderColor: '#ef4444',
                            backgroundColor: 'rgba(239,68,68,0.1)',
                            fill: true,
                            tension: 0.4
                        },
                        {
                            label: 'Opened',
                            data: statsData.stats.map(s => s.opened),
                            borderColor: '#059669',
                            backgroundColor: 'rgba(5,150,105,0.1)',
                            fill: true,
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: 'bottom', labels: { usePointStyle: true } } },
                    scales: {
                        y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.05)' } },
                        x: { grid: { display: false } }
                    }
                }
            });
        }
    },

    // ============================================================
    // NEW: Check domain health
    // ============================================================
    checkDomainHealth: async function(domain) {
        try {
            const modal = document.getElementById('health-detail-modal');
            if (modal) {
                // Show loading in existing modal
                const btn = modal.querySelector('button[onclick*="checkDomainHealth"]');
                if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Checking...'; }
            }

            const res = await fetch(API_URL + '/domain-health/' + domain, {
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
            });
            
            if (res.ok) {
                const data = await res.json();
                const resultHtml = `
                    <div style="margin-top:16px;background:var(--surface);padding:20px;border-radius:12px;border:1px solid var(--border);">
                        <h3 style="font-size:15px;font-weight:600;margin-bottom:16px;"><i class="fa-solid fa-globe" style="color:var(--p);margin-right:6px;"></i>Domain Health: ${domain} (${data.score_label})</h3>
                        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:12px;">
                            <div style="text-align:center;padding:12px 8px;border-radius:8px;background:${data.spf.has_spf ? '#dcfce7' : '#fef2f2'};">
                                <div style="font-size:20px;margin-bottom:4px;">${data.spf.has_spf ? '✅' : '❌'}</div>
                                <div style="font-size:12px;font-weight:600;">SPF</div>
                            </div>
                            <div style="text-align:center;padding:12px 8px;border-radius:8px;background:${data.dkim.has_dkim ? '#dcfce7' : '#fef2f2'};">
                                <div style="font-size:20px;margin-bottom:4px;">${data.dkim.has_dkim ? '✅' : '❌'}</div>
                                <div style="font-size:12px;font-weight:600;">DKIM</div>
                            </div>
                            <div style="text-align:center;padding:12px 8px;border-radius:8px;background:${data.dmarc.has_dmarc ? '#dcfce7' : '#fef2f2'};">
                                <div style="font-size:20px;margin-bottom:4px;">${data.dmarc.has_dmarc ? '✅' : '❌'}</div>
                                <div style="font-size:12px;font-weight:600;">DMARC</div>
                            </div>
                            <div style="text-align:center;padding:12px 8px;border-radius:8px;background:${!data.blacklist.is_blacklisted ? '#dcfce7' : '#fef2f2'};">
                                <div style="font-size:20px;margin-bottom:4px;">${!data.blacklist.is_blacklisted ? '✅' : '⛔'}</div>
                                <div style="font-size:12px;font-weight:600;">Blacklist</div>
                            </div>
                            <div style="text-align:center;padding:12px 8px;border-radius:8px;background:${!data.catch_all.is_catch_all ? '#dcfce7' : '#fef2f2'};">
                                <div style="font-size:20px;margin-bottom:4px;">${!data.catch_all.is_catch_all ? '✅' : '⚠️'}</div>
                                <div style="font-size:12px;font-weight:600;">Catch-All</div>
                            </div>
                        </div>
                        ${data.recommendations && data.recommendations.length > 0 ? 
                            `<ul style="list-style:none;padding:0;margin:0;">${data.recommendations.map(r => `<li style="margin-bottom:4px;font-size:12px;color:var(--text-muted);">⚠️ ${r}</li>`).join('')}</ul>` 
                            : '<p style="font-size:13px;color:#059669;">✅ All domain checks passed!</p>'
                        }
                    </div>
                `;

                // Insert after the domain check button
                if (modal) {
                    const btn = modal.querySelector('button[onclick*="checkDomainHealth"]');
                    if (btn) {
                        btn.insertAdjacentHTML('afterend', resultHtml);
                        btn.remove(); // Remove the button after showing results
                    }
                }

                // Refresh accounts to update domain health cache
                this.fetchAccounts();
            }
        } catch(e) {
            console.error("Domain health check error", e);
            alert("Failed to check domain health");
        }
    }
};

// Initialize accounts list when nav is clicked or app loads
document.addEventListener('DOMContentLoaded', () => {
    // Attach to existing nav click listener if possible, or just init here.
    // It's safe to init here if they are logged in, but token might not be ready.
});