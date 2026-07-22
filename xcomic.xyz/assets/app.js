
window.updateInputState = (id, hasKey) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.value = ''; // Never show the key in the input box
    if (hasKey) {
        el.placeholder = 'Key is active! Enter a new key to replace...';
        el.style.backgroundColor = 'var(--bg-light)';
        el.style.borderStyle = 'dashed';
    } else {
        el.placeholder = id === 'gemini-api-key' ? 'AIzaSy...' : 'sk-...';
        el.style.backgroundColor = 'var(--bg)';
        el.style.borderStyle = 'solid';
    }
};

// ============================================================



// app.js - Main Application Logic



// Auth is handled in index.html (inline) - NOT here



// ============================================================







const API_URL = '/api';



function escapeHtml(unsafe) {

    if (!unsafe) return '';

    return unsafe.toString().replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");

}







// ============================================================



// MOBILE MENU



// ============================================================



window.toggleMobileMenu = function() {



    var sidebar = document.querySelector('.sidebar');



    var overlay = document.getElementById('sidebar-overlay');



    if (!sidebar) return;



    var isOpen = sidebar.classList.contains('open');



    if (isOpen) {



        sidebar.classList.remove('open');



        if (overlay) overlay.classList.remove('show');



    } else {



        sidebar.classList.add('open');



        if (overlay) overlay.classList.add('show');



    }



};







// Close mobile menu when nav item clicked



document.addEventListener('DOMContentLoaded', function() {



    document.querySelectorAll('.nav-item').forEach(function(item) {



        item.addEventListener('click', function() {



            var sidebar = document.querySelector('.sidebar');



            var overlay = document.getElementById('sidebar-overlay');



            if (window.innerWidth <= 768) {



                if (sidebar) sidebar.classList.remove('open');



                if (overlay) overlay.classList.remove('show');



            }



        });



    });



});







// ============================================================



// BUTTON LOADING STATE HELPERS



// ============================================================



function btnLoading(btn, loading) {



    if (!btn) return;



    if (loading) {



        btn.dataset.originalText = btn.innerHTML;



        btn.classList.add('loading');



        btn.disabled = true;



    } else {



        if (btn.dataset.originalText) btn.innerHTML = btn.dataset.originalText;



        btn.classList.remove('loading');



        btn.disabled = false;



    }



}







// ============================================================



// THEME TOGGLE



// ============================================================



window.toggleTheme = function() {



    var isDark = document.documentElement.getAttribute('data-theme') === 'dark';



    var newTheme = isDark ? 'light' : 'dark';



    document.documentElement.setAttribute('data-theme', newTheme);



    localStorage.setItem('theme', newTheme);



    var icon = document.getElementById('theme-icon');



    var sw = document.getElementById('theme-switch');



    if (icon) icon.className = newTheme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';



    if (sw) sw.style.left = newTheme === 'dark' ? '16px' : '2px';



};







// Init theme from localStorage



(function() {



    var saved = localStorage.getItem('theme') || 'light';



    document.documentElement.setAttribute('data-theme', saved);



    document.addEventListener('DOMContentLoaded', function() {



        var icon = document.getElementById('theme-icon');



        var sw = document.getElementById('theme-switch');



        if (icon) icon.className = saved === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';



        if (sw) sw.style.left = saved === 'dark' ? '16px' : '2px';



    });



})();











// Get token from localStorage



function getToken() {



    try { return localStorage.getItem('token'); } catch(e) { return null; }



}







// API helper



async function apiCall(endpoint, method = 'GET', body = null) {



    const token = getToken();



    const headers = { 'Authorization': `Bearer ${token}` };



    if (body) headers['Content-Type'] = 'application/json';



    if (method === 'GET') {

        endpoint += (endpoint.includes('?') ? '&' : '?') + 't=' + new Date().getTime();

    }

    const res = await fetch(`${API_URL}${endpoint}`, {

        method,

        headers,

        body: body ? JSON.stringify(body) : null,

        cache: 'no-store'

    });



    const ct = res.headers.get('content-type');
    if (res.status === 401) {



        try { localStorage.removeItem('token'); localStorage.removeItem('is_admin'); } catch(e) {}



        



        var authPage = document.getElementById('auth-page');



        if (authPage && authPage.classList.contains('hidden')) {



            // User was in the app, but token expired -> reload to kick them out



            location.reload();



        } else {



            // Already on auth page, don't reload! Just throw error.



            throw new Error('Unauthorized');



        }



    }



    return res;



}







// Toast notification



function showToast(message, type) {



    var toast = document.getElementById('toast');



    var msg = document.getElementById('toast-msg');



    if (!toast || !msg) return;



    // clear any existing timeout



    if (window._toastTimer) clearTimeout(window._toastTimer);



    var icon = type === 'error' ? '&#10006;' : type === 'warning' ? '&#9888;' : '&#10003;';



    var bg = type === 'error' ? 'linear-gradient(135deg,#dc2626,#b91c1c)' 



           : type === 'warning' ? 'linear-gradient(135deg,#d97706,#b45309)'



           : 'linear-gradient(135deg,#059669,#047857)';



    toast.style.background = bg;



    toast.style.boxShadow = '0 8px 32px rgba(0,0,0,0.25)';



    toast.style.borderRadius = '12px';



    toast.style.padding = '14px 20px';



    toast.style.display = 'flex';



    toast.style.alignItems = 'center';



    toast.style.gap = '10px';



    toast.style.minWidth = '260px';



    toast.style.maxWidth = '420px';



    msg.innerHTML = '<span style="font-size:16px;">' + icon + '</span><span style="font-size:14px;font-weight:500;">' + message + '</span>';



    toast.style.bottom = '24px';



    toast.style.opacity = '1';



    toast.style.transform = 'translateY(0)';



    toast.style.transition = 'all 0.3s cubic-bezier(0.34,1.56,0.64,1)';



    window._toastTimer = setTimeout(function() {



        toast.style.opacity = '0';



        toast.style.transform = 'translateY(20px)';



        setTimeout(function() { toast.style.bottom = '-200px'; }, 300);



    }, 3500);



}







// ============================================================



// APP INIT - called after successful login



// ============================================================



window.APP_INIT = function() {



    var _fns = [



        function() { fetchDashboard(); },



        function() { setupNavigation(); },



        function() { setupLogout(); },



        function() { setupSettings(); },



        function() { populateTimezones(); },



        function() { setupColdMailTabs(); },



        function() { setupVisualBuilderTabs(); },



        function() { setupCampaignBuilder(); },



        function() { setupCampaignTabs(); },



        function() { setupSequenceBuilder(); },



        function() { setupABTest(); },



        function() { setupAdmin(); },



        function() { setupAIChat(); },



        function() { if (typeof window.setupAICopilot === 'function') window.setupAICopilot(); },



        function() {



            var aiBtn = document.getElementById('ai-chat-btn');



            if (aiBtn) aiBtn.style.display = 'flex';



        },



        function() { checkPendingApprovals(); setInterval(checkPendingApprovals, 60000); }



    ];



    _fns.forEach(function(fn, idx) {



        try { fn(); }



        catch(e) { console.error('APP_INIT step ' + idx + ' failed:', e); }



    });



};







// ============================================================



// NAVIGATION



// ============================================================







// Global navigation function - called directly from onclick



// This is the primary navigation handler (reliable, no event listener needed)



window.navTo = function(targetId) {



    document.querySelectorAll('.nav-item').forEach(function(n) { n.classList.remove('active'); });



    var clicked = document.querySelector('.nav-item[data-target="' + targetId + '"]');



    if (clicked) clicked.classList.add('active');



    document.querySelectorAll('#app-page .view').forEach(function(v) { v.classList.remove('active'); });



    var target = document.getElementById(targetId);



    if (target) target.classList.add('active');



    // Trigger data loading



    try {



        if (targetId === 'admin-view') loadAdminUsers();



        if (targetId === 'dashboard') fetchDashboard();



        if (targetId === 'cold-mail-list') renderColdMailList();



        if (targetId === 'campaigns-list') renderNewsletterList();



        if (targetId === 'sending-accounts-view' && typeof ACCOUNTS !== 'undefined') ACCOUNTS.init();



        if (targetId === 'unsubscribes-view') loadUnsubscribes();

        if (targetId === 'replies-view') loadReplies();
if (targetId === 'support-view') { SUPPORT.loadSupportTickets(); SUPPORT.checkUnreadTickets(); }

        if (targetId === 'settings') loadSmtpStatus();



    } catch(e) { console.error('navTo data load error:', e); }



};







function setupNavigation() {



    document.querySelectorAll('.nav-item').forEach(item => {



        item.addEventListener('click', e => {



            e.preventDefault();



            const targetId = item.getAttribute('data-target');



            if (targetId) window.navTo(targetId);



        });



    });



}







function populateAnalytics(campaignId) {



    if (!window.lastFetchedCampaigns) return;



    const c = window.lastFetchedCampaigns.find(x => x.id === campaignId);



    if (!c) return;







    document.getElementById('analytics-title').textContent = c.subject || 'Untitled Campaign';



    const statusEl = document.getElementById('analytics-status');



    const cStatus = c.status || 'Draft';



    statusEl.textContent = cStatus;



    statusEl.style.background = cStatus.toLowerCase() === 'completed' ? '#059669' : (cStatus.toLowerCase() === 'failed' ? '#dc2626' : '#333');







    // Stats calculations



    const started = c.sent_count; // sequence started = leads sent to



    const opens = c.opens;



    const clicks = c.clicks;



    const openRate = started > 0 ? ((opens / started) * 100).toFixed(1) : '0';



    const clickRate = started > 0 ? ((clicks / started) * 100).toFixed(1) : '0';



    let progress = started > 0 ? 100 : 0; // Simple progress mock based on having sent something







    document.getElementById('analytics-progress-text').textContent = progress + '%';



    document.getElementById('analytics-progress-bar').style.width = progress + '%';







    document.getElementById('analytics-seq-started').textContent = started;



    document.getElementById('analytics-open-rate').textContent = openRate + '%';



    document.getElementById('analytics-open-count').textContent = opens;



    document.getElementById('analytics-click-rate').textContent = clickRate + '%';



    document.getElementById('analytics-click-count').textContent = clicks;



}









window.renderAnalyticsInfo = async function(c, prefix) {

    // Schedule info

    const schedEl = document.getElementById(`${prefix}-analytics-schedule-info`);

    if (schedEl) {

        let schedText = '';

        if (c.sending_days) {

            schedText += `<strong>Days:</strong> ${c.sending_days}<br>`;

        } else {

            schedText += `<strong>Days:</strong> Mon-Sun<br>`;

        }

        

        let startTime = c.start_hour !== undefined ? c.start_hour + ':00' : '00:00';

        let endTime = c.end_hour !== undefined ? c.end_hour + ':00' : '23:59';

        schedText += `<strong>Time:</strong> ${startTime} - ${endTime} (${c.timezone || 'UTC'})<br>`;

        

        if (c.delay_min !== undefined) {

            schedText += `<strong>Delay:</strong> ${c.delay_min} to ${c.delay_max || c.delay_min} minutes`;

        }

        

        schedEl.innerHTML = schedText;

    }

    

    // Accounts info

    const accEl = document.getElementById(`${prefix}-analytics-accounts-info`);

    if (accEl) {

        accEl.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Loading accounts...';

        try {

            const res = await apiCall('/sending-accounts');

            if (res.ok) {

                const accounts = await res.json();

                const selectedIds = c.selected_sender_ids ? c.selected_sender_ids.split(',').map(s => s.trim()) : [];

                if (selectedIds.length === 0) {

                    accEl.innerHTML = '<span style="color:var(--text-muted);">All active accounts</span>';

                } else {

                    const matched = accounts.filter(a => selectedIds.includes(a.id.toString()) || selectedIds.includes(a.id));

                    if (matched.length > 0) {

                        accEl.innerHTML = matched.map(a => `<div style="padding:4px 0;border-bottom:1px solid var(--border);">${escapeHtml(a.email || a.name || a.id)}</div>`).join('');

                    } else {

                        accEl.innerHTML = '<span style="color:var(--text-muted);">No specific accounts found</span>';

                    }

                }

            } else {

                accEl.innerHTML = '<span style="color:var(--danger);">Failed to load accounts</span>';

            }

        } catch(e) {

            accEl.innerHTML = '<span style="color:var(--danger);">Failed to load accounts</span>';

        }

    }

};



window.populateVbAnalytics = function(id) {

    if (!window.lastFetchedCampaigns) return;

    const c = window.lastFetchedCampaigns.find(x => x.id === id);

    if (!c) return;

    

    window.renderAnalyticsInfo(c, 'vb');



    const statusEl = document.getElementById('vb-analytics-status');

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

                        <td style="font-weight:600;color:var(--text);">${escapeHtml(l.email) || ''}</td>

                        <td>${escapeHtml(l.name) || '-'}</td>

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



window.populateColdAnalytics = function(id) {



    if (!window.lastFetchedCampaigns) return;



    const c = window.lastFetchedCampaigns.find(x => x.id === id);



    if (!c) return;

    

    window.renderAnalyticsInfo(c, 'cold');



    if (c.type !== 'cold_mail') return;







    const statusEl = document.getElementById('cold-analytics-status');



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



    setEl('cold-analytics-seq-started', started.toLocaleString());



    setEl('cold-analytics-open-rate', `${openRate}%`);



    setEl('cold-analytics-open-count', `(${opens.toLocaleString()} opens)`);



    setEl('cold-analytics-click-rate', `${clickRate}%`);



    setEl('cold-analytics-click-count', `(${clicks.toLocaleString()} clicks)`);



    



    // Fetch and render analytics leads table



    const tbody = document.getElementById('cold-analytics-leads-tbody');



    if (tbody) {



        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:24px;color:var(--text-muted);">Loading leads...</td></tr>';



        apiCall('/campaigns/' + id + '/leads')



            .then(res => res.json())



            .then(leads => {



                tbody.innerHTML = '';



                if (!leads || leads.length === 0) {



                    tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:24px;color:var(--text-muted);">No leads found for this campaign.</td></tr>';



                    return;



                }



                leads.forEach(l => {



                    const tr = document.createElement('tr');



                    const statusColor = (l.status === 'sent' || l.status === 'opened' || l.status === 'clicked') ? '#059669' : (l.status === 'bounced' ? '#dc2626' : (l.status === 'unsubscribed' ? '#ea580c' : '#64748b'));



                    tr.innerHTML = `



                        <td style="font-weight:600;color:var(--text);">${escapeHtml(l.email) || ''}</td>



                        <td>${escapeHtml(l.name) || '-'}</td>



                        <td><span style="font-size:12px; font-weight:600; color:${statusColor}; text-transform:capitalize;">${l.status || 'pending'}</span></td>



                        <td><span style="font-size:12px; font-weight:600; color:var(--text-muted);">${l.variant || '-'}</span></td>



                    `;



                    tbody.appendChild(tr);



                });



            })



            .catch(err => {



                tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:24px;color:#dc2626;">Error loading leads.</td></tr>';



            });



    }



};







window.viewAnalytics = function(id) {



    if (!window.lastFetchedCampaigns) return;



    const c = window.lastFetchedCampaigns.find(x => x.id === id);



    if (!c) return;







    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));



    document.querySelectorAll('#app-page .view').forEach(v => v.classList.remove('active'));



    



    if (c.type === 'cold_mail') {



        const navCamp = document.querySelector('.nav-item[data-target="cold-mail-list"]');



        if (navCamp) navCamp.classList.add('active');



        // BUG-2 FIX: was 'cold-mail' which doesn't exist — correct ID is 'cold-mail-builder'



        const target = document.getElementById('cold-mail-builder');



        if (target) target.classList.add('active');



        



        window.currentCampaignId = id;



        switchColdTab('analytics');



        



    } else {



        const target = document.getElementById('view-campaign-details');



        if (target) target.classList.add('active');



        populateAnalytics(id);



    }



};







// ============================================================



// LOGOUT



// ============================================================



function setupLogout() {



    var btn = document.getElementById('logout-btn');



    if (!btn) return;



    btn.addEventListener('click', () => {



        try { localStorage.removeItem('token'); localStorage.removeItem('is_admin'); } catch(e) {}



        location.reload();



    });



}







// ============================================================



// DASHBOARD



// ============================================================



let activityChartInstance = null;







async function fetchDashboard() {



    // Show loading skeleton on stat cards only



    var statEls = document.querySelectorAll('[id^="stat-"]');



    statEls.forEach(function(el) {



        el.innerHTML = '<span class="shimmer-bar" style="display:inline-block;width:40px;height:18px;background:linear-gradient(90deg,#f1f5f9 25%,#e2e8f0 50%,#f1f5f9 75%);border-radius:4px;animation:shimmer 1.2s infinite;background-size:200% 100%;"></span>';



    });



    var tbody = document.querySelector('#dashboard-unified-table tbody');



    if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:32px;color:#94a3b8;"><i class="fa-solid fa-spinner fa-spin" style="margin-right:8px;"></i>Loading campaigns...</td></tr>';







    // --- Helper to safely set text into stat elements ---



    const setEl = function(id, val) {



        var el = document.getElementById(id);



        if (el) {



            // Remove shimmer and set value



            el.innerHTML = '';



            el.textContent = val;



        }



    };







    let coldSent = 0, coldOpens = 0, coldClicks = 0;



    let newsSent = 0, newsOpens = 0, newsClicks = 0;



    let totalReplies = 0;



    let totalBounces = 0;



    let campaigns = [];







    // --- Fetch campaigns (critical) ---



    try {



        const cRes = await apiCall('/campaigns');
        const bulkRes = await apiCall('/bulk-campaigns');
        if (cRes && cRes.ok) {
            campaigns = await cRes.json();
            window.lastFetchedCampaigns = campaigns;
        }
        if (bulkRes && bulkRes.ok) {
            window.lastFetchedBulkCampaigns = await bulkRes.json();
        }
        if (!Array.isArray(campaigns)) campaigns = [];



    } catch(e) {



        console.error('Campaigns fetch error:', e);



        campaigns = [];



    }



    window.lastFetchedCampaigns = campaigns;







    // --- Fetch bounces (non-critical, don't block) ---



    try {



        const bRes = await apiCall('/bounces');



        if (bRes && bRes.ok) {



            const bounces = await bRes.json();



            totalBounces = Array.isArray(bounces) ? bounces.length : 0;



        }



    } catch(e) {



        console.warn('Bounces fetch error:', e);



    }







    

    // --- Fetch replies ---

    try {

        const rRes = await apiCall('/replies');

        if (rRes && rRes.ok) {

            const replies = await rRes.json();

            totalReplies = Array.isArray(replies) ? replies.length : 0;

        }

    } catch(e) {

        console.warn('Replies fetch error:', e);

    }



    // --- Build campaign table ---



    const unifiedTbody = document.querySelector('#dashboard-unified-table tbody');



    if (unifiedTbody) unifiedTbody.innerHTML = '';







    if (!campaigns || campaigns.length === 0) {



        if (unifiedTbody) unifiedTbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:48px 24px;"><div style="display:flex;flex-direction:column;align-items:center;gap:12px;"><div style="width:56px;height:56px;background:#f1f5f9;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:24px;">&#128231;</div><p style="font-weight:600;color:#374151;margin:0;font-size:15px;">No campaigns yet</p><p style="color:#9ca3af;margin:0;font-size:13px;">Create your first Cold Mail or Newsletter campaign</p></div></td></tr>';



    } else {



        campaigns.forEach(function(c) {



            if (c.type === 'cold_mail') {



                coldSent += c.sent_count || 0;



                coldOpens += c.opens || 0;



                coldClicks += c.clicks || 0;



            } else {



                newsSent += c.sent_count || 0;



                newsOpens += c.opens || 0;



                newsClicks += c.clicks || 0;



            }







            const tr = document.createElement('tr');



            tr.setAttribute('data-type', c.type === 'cold_mail' ? 'cold_mail' : 'newsletter');







            const cStatus = c.status ? c.status.toLowerCase() : 'draft';



            let statusColor = '#64748b';



            if (cStatus === 'completed' || cStatus === 'sent') statusColor = '#059669';



            if (cStatus === 'active' || cStatus === 'processing') statusColor = '#3b82f6';



            if (cStatus === 'failed') statusColor = '#dc2626';







            const typeBadge = c.type === 'cold_mail'



                ? '<span style="background:#e0e7ff;color:#4f46e5;font-size:12px;padding:4px 8px;border-radius:6px;font-weight:600;"><i class="fa-solid fa-bolt" style="margin-right:4px;"></i> Cold</span>'



                : '<span style="background:#f1f5f9;color:#475569;font-size:12px;padding:4px 8px;border-radius:6px;font-weight:600;"><i class="fa-solid fa-newspaper" style="margin-right:4px;"></i> Newsletter</span>';







            let progressHtml = '-';



            if (c.type === 'cold_mail') {



                const openRate = c.sent_count > 0 ? Math.round((c.opens / c.sent_count) * 100) : 0;



                progressHtml = '<div style="display:flex;align-items:center;gap:8px;"><div style="flex:1;background:#f1f5f9;height:6px;border-radius:3px;overflow:hidden;"><div style="background:var(--p);height:100%;width:' + openRate + '%"></div></div><span style="font-size:12px;color:var(--text-muted);font-weight:600;">' + openRate + '%</span></div>';



            } else {



                progressHtml = '<span style="font-size:13px;font-weight:600;">' + (c.sent_count || 0) + ' sent</span>';



            }







            let dateStr = '';



            if (c.created_at && c.created_at !== 'None' && c.created_at !== 'null') {



                try {



                    const dt = new Date(c.created_at);



                    if (!isNaN(dt.getTime())) {



                        dateStr = dt.getDate() + ' ' + dt.toLocaleString('default', {month:'short'}) + ' ' + dt.getFullYear();



                    }



                } catch(e) {}



            }







            const abBadge = c.is_ab_test ? '<span style="background:#f3e8ff;color:#a855f7;font-size:10px;padding:2px 6px;border-radius:10px;margin-left:4px;font-weight:700;">A/B</span>' : '';



            tr.innerHTML =



                '<td style="font-weight:600;color:var(--text);">' +



                    '<div style="margin-bottom:2px;">' + (c.subject || 'Untitled') + abBadge + '</div>' +



                    (dateStr ? '<div style="font-size:12px;color:var(--text-muted);">' + dateStr + '</div>' : '') +



                '</td>' +



                '<td>' + typeBadge + '</td>' +



                '<td style="min-width:120px;">' + progressHtml + '</td>' +



                '<td><div style="display:flex;align-items:center;gap:6px;"><div style="width:8px;height:8px;border-radius:50%;background:' + statusColor + ';"></div><span style="font-size:13px;font-weight:600;color:' + statusColor + ';text-transform:capitalize;">' + (c.status || 'Draft') + '</span></div></td>' +



                '<td><div style="display:flex;gap:6px;">' +



                    (c.type === 'cold_mail' ? '<button class="btn" style="padding:6px 12px;font-size:13px;background:#f8fafc;border:1px solid var(--border);" onclick="viewAnalytics(\'' + c.id + '\')" title="View Analytics"><i class="fa-solid fa-chart-pie" style="color:var(--p);"></i></button>' : '') +



                    '<button class="btn" style="padding:6px 12px;font-size:13px;background:#f8fafc;border:1px solid var(--border);" onclick="editCampaign(\'' + c.id + '\')" title="Edit"><i class="fa-solid fa-pen-to-square" style="color:#64748b;"></i></button>' +



                    '<button class="btn" style="padding:6px 12px;font-size:13px;background:#fef2f2;border:1px solid #fca5a5;" onclick="deleteCampaign(\'' + c.id + '\')" title="Delete"><i class="fa-solid fa-trash" style="color:#ef4444;"></i></button>' +



                '</div></td>';







            if (unifiedTbody) unifiedTbody.appendChild(tr);



        });



    }







    // --- Always update stat cards (even if campaigns = []) ---



    const coldOpenRate = coldSent > 0 ? Math.round((coldOpens / coldSent) * 100) : 0;



    const coldClickRate = coldSent > 0 ? Math.round((coldClicks / coldSent) * 100) : 0;



    setEl('stat-cold-sent', coldSent.toLocaleString());



    setEl('stat-cold-opens', coldOpenRate + '%');



    setEl('stat-cold-clicks', coldClickRate + '%');



    setEl('stat-cold-replies', totalReplies.toLocaleString());



    setEl('stat-cold-bounces', totalBounces.toLocaleString());







    const newsOpenRate = newsSent > 0 ? Math.round((newsOpens / newsSent) * 100) : 0;



    const newsClickRate = newsSent > 0 ? Math.round((newsClicks / newsSent) * 100) : 0;



    setEl('stat-news-sent', newsSent.toLocaleString());



    setEl('stat-news-opens', newsOpenRate + '%');



    setEl('stat-news-clicks', newsClickRate + '%');



    setEl('stat-news-replies', '0');



    setEl('stat-news-bounces', '0');







    // --- Draw chart ---



    try { initOrUpdateChart(campaigns); } catch(e) { console.error('Chart error:', e); }



}











async function initOrUpdateChart(campaigns) {



    const ctx = document.getElementById('activityChart');



    if (!ctx) return;



    



    const labels = [];



    const data = [];



    



    for (let i = 6; i >= 0; i--) {



        const d = new Date();



        d.setDate(d.getDate() - i);



        labels.push(d.toLocaleDateString('en-US', { weekday: 'short' }));



        



        let dailyTotal = 0;



        if (campaigns && campaigns.length > 0) {



            campaigns.forEach(c => {



                if (c.created_at && c.created_at !== "None") {



                    const cDate = new Date(c.created_at);



                    if (!isNaN(cDate.getTime())) {



                        if (cDate.getDate() === d.getDate() && 



                            cDate.getMonth() === d.getMonth() && 



                            cDate.getFullYear() === d.getFullYear()) {



                            dailyTotal += (c.sent_count || 0);



                        }



                    }



                }



            });



        }



        data.push(dailyTotal);



    }



    



    if (activityChartInstance) {



        activityChartInstance.destroy();



    }



    



    if (typeof Chart !== 'undefined') {



        Chart.defaults.font.family = "'Inter', sans-serif";



        Chart.defaults.color = '#64748b';



        



        activityChartInstance = new Chart(ctx, {



            type: 'line',



            data: {



                labels: labels,



                datasets: [{



                    label: 'Emails Sent',



                    data: data,



                    borderColor: '#4f46e5',



                    backgroundColor: 'rgba(79, 70, 229, 0.1)',



                    borderWidth: 3,



                    pointBackgroundColor: '#fff',



                    pointBorderColor: '#4f46e5',



                    pointBorderWidth: 2,



                    pointRadius: 4,



                    pointHoverRadius: 6,



                    fill: true,



                    tension: 0.4



                }]



            },



            options: {



                responsive: true,



                maintainAspectRatio: false,



                plugins: {



                    legend: { display: false },



                    tooltip: {



                        backgroundColor: '#1e293b',



                        padding: 12,



                        titleFont: { size: 13, weight: 'bold' },



                        bodyFont: { size: 13 },



                        displayColors: false,



                        callbacks: {



                            label: function(context) { return context.parsed.y + ' emails'; }



                        }



                    }



                },



                scales: {



                    x: { grid: { display: false, drawBorder: false } },



                    y: { 



                        beginAtZero: true,



                        grid: { color: '#f1f5f9', borderDash: [4, 4], drawBorder: false },



                        border: { display: false }



                    }



                },



                interaction: { intersect: false, mode: 'index' }



            }



        });



    }







    // --- Account Health Summary ---



    try {



        const healthRes = await apiCall('/account-health-all');



        if (healthRes && healthRes.ok) {



            const healthData = await healthRes.json();



            const container = document.getElementById('dashboard-health-cards');



            const wrapper = document.getElementById('dashboard-health-summary');



            if (container && wrapper && healthData.length > 0) {



                wrapper.style.display = 'block';



                container.innerHTML = '';



                healthData.forEach(h => {



                    let color = '#059669';



                    const score = h.health_score || 100;



                    if (score < 50) color = '#ef4444';



                    else if (score < 70) color = '#f97316';



                    else if (score < 90) color = '#f59e0b';







                    const autoPauseBanner = h.auto_paused 



                        ? `<div style="background:#fef2f2;color:#dc2626;padding:6px 10px;border-radius:6px;font-size:11px;margin-top:8px;">⚠️ Auto-paused: ${h.auto_paused_reason || 'Poor health'}</div>` 



                        : '';







                    container.innerHTML += `



                        <div style="background:#fff;padding:20px;border-radius:12px;border:1px solid rgba(0,0,0,0.06);box-shadow:0 2px 8px rgba(0,0,0,0.02);transition:transform 0.2s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">



                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">



                                <div style="font-weight:600;font-size:14px;color:var(--text);">${h.email || 'Unknown'}</div>



                                <div style="font-size:20px;font-weight:800;color:${color};">${score}%</div>



                            </div>



                            <div style="width:100%;height:6px;background:#e2e8f0;border-radius:3px;overflow:hidden;margin-bottom:8px;">



                                <div style="width:${score}%;height:100%;background:${color};border-radius:3px;transition:width 0.8s ease;"></div>



                            </div>



                            <div style="display:flex;gap:12px;font-size:12px;color:var(--text-muted);">



                                <span>📧 ${(h.metrics || {}).total_sent || 0} sent</span>



                                <span>💥 ${(h.metrics || {}).bounce_rate || 0}% bounce</span>



                                <span>📊 ${h.suggested_daily_limit || '-'}/day</span>



                            </div>



                            ${autoPauseBanner}



                        </div>



                    `;



                });



            }



        }



    } catch(e) {



        console.warn('Health summary fetch error:', e);



    }



}







// Add event listener for dashboard tabs filtering



document.addEventListener('DOMContentLoaded', () => {



    document.addEventListener('click', e => {



        if (e.target.classList.contains('dash-tab')) {



            document.querySelectorAll('.dash-tab').forEach(t => t.classList.remove('active'));



            e.target.classList.add('active');



            



            const filter = e.target.getAttribute('data-filter');



            const rows = document.querySelectorAll('#dashboard-unified-table tbody tr');



            



            rows.forEach(row => {



                if (filter === 'all' || row.getAttribute('data-type') === filter) {



                    row.style.display = '';



                } else {



                    row.style.display = 'none';



                }



            });



        }



    });



});













window.openCampaignAnalytics = function(id) {

    if (!window.lastFetchedCampaigns) return;

    const c = window.lastFetchedCampaigns.find(x => x.id === id);

    if (!c) return;

    if (c.type === 'cold_mail') {

        openColdMailBuilder(id);

        setTimeout(() => {

            const tab = document.querySelector('.clean-tab[data-coldtab="analytics"]');

            if (tab) tab.click();

        }, 100);

    } else {

        editCampaign(id);

        setTimeout(() => {

            const tab = document.querySelector('.clean-tab[data-vbtab="analytics"]');

            if (tab) tab.click();

        }, 100);

    }

};



window.editCampaign = function(id) {



    if (!window.lastFetchedCampaigns) return;



    const c = window.lastFetchedCampaigns.find(x => x.id === id);



    if (!c) return;



    



    window.currentCampaignId = id;







    if (c.type === 'cold_mail') {



        const target = document.getElementById('cold-mail-builder');



        if (target) {



            document.querySelectorAll('#app-page .view').forEach(v => v.classList.remove('active'));



            target.classList.add('active');



        }



        



        // Parse body back into steps



        const bodyParts = (c.body || '').split(/<hr[^>]*>/i);



        const parsedSteps = bodyParts.map((part, i) => {



            // Remove the <div> wrapper that was added during save without stripping user HTML



            const textContent = part.replace(/^<div>/, '').replace(/<\/div>$/, '').trim();



            return { step: i + 1, wait: 0, subject: i === 0 ? (c.subject || '') : '', body: textContent, is_ab: false, subject_b: '', body_b: '' };



        });



        if (parsedSteps.length === 0) {



            parsedSteps.push({ step: 1, wait: 0, subject: c.subject || '', body: '', is_ab: false, subject_b: '', body_b: '' });



        } else {



            parsedSteps[0].subject = c.subject || '';



        }



        



        // Update global steps array



        if (window._coldMailSteps) {



            window._coldMailSteps.length = 0;



            parsedSteps.forEach(s => window._coldMailSteps.push(s));



        }



        if (typeof window._coldMailCurrentStep !== 'undefined') {



            window._coldMailCurrentStep = 1;



        }



        



        const subjectEl = document.getElementById('inst-subject');



        if (subjectEl) subjectEl.value = parsedSteps[0].subject;



        const bodyEl = document.getElementById('inst-body');



        if (bodyEl) bodyEl.value = parsedSteps[0].body;



        



        // Trigger renderSteps and loadStep if available



        if (typeof window._coldMailRenderSteps === 'function') window._coldMailRenderSteps();



        if (typeof window._coldMailLoadStep === 'function') window._coldMailLoadStep();



        



        

        const coldStatus = c.status || 'draft';

        const sendBtn = document.getElementById('inst-send-seq-btn');

        const actionsDiv = document.getElementById('cold-status-actions');

        if (actionsDiv) {

            if (coldStatus.toLowerCase() === 'processing' || coldStatus.toLowerCase() === 'scheduled') {

                if (sendBtn) sendBtn.style.display = 'none';

                actionsDiv.style.display = 'inline-flex';

                actionsDiv.innerHTML = `<button class="btn" style="padding:12px 24px;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;font-weight:600;display:flex;align-items:center;flex:1;justify-content:center;" onclick="pauseCampaign('${c.id}')"><i class="fa-solid fa-pause" style="color:#d97706;margin-right:8px;"></i>Pause Campaign</button>`;

            } else if (['paused', 'failed', 'completed'].includes(coldStatus.toLowerCase())) {

                if (sendBtn) sendBtn.style.display = 'none';

                actionsDiv.style.display = 'inline-flex';

                actionsDiv.innerHTML = `<button class="btn" style="padding:12px 24px;background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;font-weight:600;display:flex;align-items:center;flex:1;justify-content:center;" onclick="resumeCampaign('${c.id}')"><i class="fa-solid fa-play" style="color:#059669;margin-right:8px;"></i>Resume Campaign</button>`;

            } else {

                if (sendBtn) sendBtn.style.display = 'inline-block';

                actionsDiv.style.display = 'none';

                actionsDiv.innerHTML = '';

            }

        }

        

        // Populate Schedule

        if (c.timezone) {

            const tzEl = document.getElementById('sch-timezone');

            if (tzEl) tzEl.value = c.timezone;

        }

        const coldDayMap = {Mon:'sch-day-mon', Tue:'sch-day-tue', Wed:'sch-day-wed', Thu:'sch-day-thu', Fri:'sch-day-fri', Sat:'sch-day-sat', Sun:'sch-day-sun'};

        Object.values(coldDayMap).forEach(id => { const el = document.getElementById(id); if (el) el.checked = false; });

        if (c.sending_days) {

            try {

                JSON.parse(c.sending_days).forEach(d => {

                    const el = document.getElementById(coldDayMap[d]);

                    if (el) el.checked = true;

                });

            } catch(e) {}

        } else {

            ['sch-day-mon','sch-day-tue','sch-day-wed','sch-day-thu','sch-day-fri'].forEach(id => {

                const el = document.getElementById(id);

                if (el) el.checked = true;

            });

        }

        const coldStartEl = document.getElementById('sch-start-time');

        const coldEndEl = document.getElementById('sch-end-time');

        if (coldStartEl) coldStartEl.value = String(c.start_hour !== null ? c.start_hour : 0).padStart(2,'0') + ':00';

        if (coldEndEl) {

            let eh = c.end_hour !== null ? c.end_hour : 0;

            if (eh === 24) eh = 0;

            coldEndEl.value = String(eh).padStart(2,'0') + ':00';

        }

        

        const cDelayMinEl = document.getElementById('sch-delay-min');

        const cDelayMaxEl = document.getElementById('sch-delay-max');

        if (cDelayMinEl) cDelayMinEl.value = (c.delay_min !== null && c.delay_min !== undefined) ? c.delay_min : 30;

        if (cDelayMaxEl) cDelayMaxEl.value = (c.delay_max !== null && c.delay_max !== undefined) ? c.delay_max : 90;



        const trackOpensEl = document.getElementById('cold-track-opens');

        const trackClicksEl = document.getElementById('cold-track-clicks');

        const unsubscribeEl = document.getElementById('cold-use-unsubscribe');

        const maxEmailsEl = document.getElementById('cold-max-emails');

        const rampUpEl = document.getElementById('cold-ramp-up');

        if (trackOpensEl) trackOpensEl.value = (c.track_opens === false) ? '0' : '1';

        if (trackClicksEl) trackClicksEl.value = (c.track_clicks === false) ? '0' : '1';

        if (unsubscribeEl) unsubscribeEl.value = (c.use_unsubscribe === false) ? '0' : '1';

        if (maxEmailsEl) maxEmailsEl.value = (c.max_emails_per_day !== null && c.max_emails_per_day !== undefined) ? c.max_emails_per_day : 50;

        if (rampUpEl) rampUpEl.value = (c.daily_ramp_up !== null && c.daily_ramp_up !== undefined) ? c.daily_ramp_up : 5;

        

        if (window.renderSendingAccountsSelector) {

            window.renderSendingAccountsSelector('cold-sender-accounts-list', c.selected_sender_ids);

        }



        window.switchColdTab('sequences');

        showToast('Cold Mail sequence loaded for editing');





    } else {



        const target = document.getElementById('campaigns-builder');



        if (target) {



            document.querySelectorAll('#app-page .view').forEach(v => v.classList.remove('active'));



            target.classList.add('active');



        }



        const subjectEl = document.getElementById('campaign-subject');



        if (subjectEl) subjectEl.value = c.subject;



        const vbTrackOpensEl = document.getElementById('vb-track-opens');

        const vbTrackClicksEl = document.getElementById('vb-track-clicks');

        const vbUnsubscribeEl = document.getElementById('vb-use-unsubscribe');

        const vbMaxEmailsEl = document.getElementById('vb-max-emails');

        const vbRampUpEl = document.getElementById('vb-ramp-up');

        if (vbTrackOpensEl) vbTrackOpensEl.value = (c.track_opens === false) ? '0' : '1';

        if (vbTrackClicksEl) vbTrackClicksEl.value = (c.track_clicks === false) ? '0' : '1';

        if (vbUnsubscribeEl) vbUnsubscribeEl.value = (c.use_unsubscribe === false) ? '0' : '1';

        if (vbMaxEmailsEl) vbMaxEmailsEl.value = (c.max_emails_per_day !== null && c.max_emails_per_day !== undefined) ? c.max_emails_per_day : 50;

        if (vbRampUpEl) vbRampUpEl.value = (c.daily_ramp_up !== null && c.daily_ramp_up !== undefined) ? c.daily_ramp_up : 5;

        

        if (window.renderSendingAccountsSelector) {

            window.renderSendingAccountsSelector('vb-sender-accounts-list', c.selected_sender_ids);

        }



        const canvas = document.getElementById('builder-canvas');



        if (canvas) {



            canvas.innerHTML = '';



            if (c.body) {



                const parser = new DOMParser();



                const doc = parser.parseFromString(c.body, 'text/html');



                const tds = doc.querySelectorAll('td[style="padding:0;"]');



                if (tds.length > 0) {



                    tds.forEach(td => {



                        const innerHTML = td.innerHTML;



                        let type = 'text';



                        if (innerHTML.includes('<img')) type = 'image';



                        else if (innerHTML.includes('<a ') && innerHTML.includes('Click Me')) type = 'button'; // basic heuristic



                        else if (innerHTML.includes('text-decoration:none;display:inline-block')) type = 'button';



                        else if (innerHTML.includes('<hr')) type = 'divider';



                        



                        window.addBlockToCanvas(type, null, innerHTML);



                    });



                } else {



                    window.addBlockToCanvas('text', null, c.body);



                }



            } else {



                canvas.innerHTML = '<div class="canvas-placeholder">Drag blocks here to build your email</div>';



            }



        }



        



        // Populate Schedule



        if (c.timezone) {



            const tzEl = document.getElementById('vb-sch-timezone');



            if (tzEl) tzEl.value = c.timezone;



        }



        const dayMap = {Mon:'vb-sch-day-mon', Tue:'vb-sch-day-tue', Wed:'vb-sch-day-wed', Thu:'vb-sch-day-thu', Fri:'vb-sch-day-fri', Sat:'vb-sch-day-sat', Sun:'vb-sch-day-sun'};



        Object.values(dayMap).forEach(id => { const el = document.getElementById(id); if (el) el.checked = false; });



        if (c.sending_days) {



            try {



                JSON.parse(c.sending_days).forEach(d => {



                    const el = document.getElementById(dayMap[d]);



                    if (el) el.checked = true;



                });



            } catch(e) {}



        } else {



            ['vb-sch-day-mon','vb-sch-day-tue','vb-sch-day-wed','vb-sch-day-thu','vb-sch-day-fri'].forEach(id => {



                const el = document.getElementById(id);



                if (el) el.checked = true;



            });



        }



        const startEl = document.getElementById('vb-sch-start-time');



        const endEl = document.getElementById('vb-sch-end-time');



        if (startEl) startEl.value = String(c.start_hour !== null ? c.start_hour : 0).padStart(2,'0') + ':00';



        if (endEl) {



            let eh = c.end_hour !== null ? c.end_hour : 0;



            if (eh === 24) eh = 0;



            endEl.value = String(eh).padStart(2,'0') + ':00';



        }



        const vbDelayMinEl = document.getElementById('vb-sch-delay-min');

        const vbDelayMaxEl = document.getElementById('vb-sch-delay-max');

        if (vbDelayMinEl) vbDelayMinEl.value = (c.delay_min !== null && c.delay_min !== undefined) ? c.delay_min : 30;

        if (vbDelayMaxEl) vbDelayMaxEl.value = (c.delay_max !== null && c.delay_max !== undefined) ? c.delay_max : 90;







        

        const vbStatus = c.status || 'draft';

        const vbSendBtn = document.getElementById('send-btn');

        const vbActionsDiv = document.getElementById('vb-status-actions');

        if (vbActionsDiv) {

            if (vbStatus.toLowerCase() === 'processing' || vbStatus.toLowerCase() === 'scheduled') {

                if (vbSendBtn) vbSendBtn.style.display = 'none';

                vbActionsDiv.style.display = 'inline-flex';

                vbActionsDiv.innerHTML = `<button class="btn" style="padding:16px 32px;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;font-weight:600;display:flex;align-items:center;flex:1;justify-content:center;" onclick="pauseCampaign('${c.id}')"><i class="fa-solid fa-pause" style="color:#d97706;margin-right:8px;"></i>Pause Campaign</button>`;

            } else if (['paused', 'failed', 'completed'].includes(vbStatus.toLowerCase())) {

                if (vbSendBtn) vbSendBtn.style.display = 'none';

                vbActionsDiv.style.display = 'inline-flex';

                vbActionsDiv.innerHTML = `<button class="btn" style="padding:16px 32px;background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;font-weight:600;display:flex;align-items:center;flex:1;justify-content:center;" onclick="resumeCampaign('${c.id}')"><i class="fa-solid fa-play" style="color:#059669;margin-right:8px;"></i>Resume Campaign</button>`;

            } else {

                if (vbSendBtn) vbSendBtn.style.display = 'inline-block';

                vbActionsDiv.style.display = 'none';

                vbActionsDiv.innerHTML = '';

            }

        }

        

        window.switchVbTab('design');





        showToast('Newsletter loaded for editing');



    }



    



    // Fetch leads and populate the leads textarea so that leads are isolated per campaign



    const leadsInputId = c.type === 'cold_mail' ? 'seq-leads' : 'newsletter-leads';



    const leadsInput = document.getElementById(leadsInputId);



    if (leadsInput) {



        leadsInput.value = 'Loading leads...';



        apiCall('/campaigns/' + id + '/leads')



            .then(res => res.json())



            .then(leads => {



                if (leads && leads.length > 0) {



                    const leadsText = leads.map(l => `${l.email}${l.name ? ', ' + l.name : ''}${l.company ? ', ' + l.company : ''}`).join('\n');



                    leadsInput.value = leadsText;



                } else {



                    leadsInput.value = '';



                }



                if (typeof window.renderLeadsList === 'function') window.renderLeadsList(leadsInputId);



            })



            .catch(err => {



                leadsInput.value = '';



                if (typeof window.renderLeadsList === 'function') window.renderLeadsList(leadsInputId);



                showToast('Failed to load campaign leads', 'error');



            });



    }



};







window.pauseCampaign = async function(id) {



    if (!confirm('Are you sure you want to pause this campaign?')) return;



    try {



        const res = await apiCall(`/campaigns/${id}/pause`, 'POST');



        if (res && res.ok) {



            showToast('Campaign paused successfully');



            await fetchDashboard();

            renderColdMailList();

            renderNewsletterList();

            const c = (window.lastFetchedCampaigns || []).find(x => x.id === id);

            if (c) {

                window.navTo(c.type === 'cold_mail' ? 'cold-mail-list' : 'campaigns-list');

            }



        } else {



            showToast('Failed to pause campaign');



        }



    } catch (e) {



        console.error(e);



        showToast('Error pausing campaign');



    }



};







window.resumeCampaign = async function(id) {



    if (!confirm('Are you sure you want to resume this campaign?')) return;



    try {



        const res = await apiCall(`/campaigns/${id}/resume`, 'POST');



        if (res && res.ok) {



            showToast('Campaign resumed successfully');



            await fetchDashboard();

            renderColdMailList();

            renderNewsletterList();

            const c = (window.lastFetchedCampaigns || []).find(x => x.id === id);

            if (c) {

                window.navTo(c.type === 'cold_mail' ? 'cold-mail-list' : 'campaigns-list');

            }



        } else {



            showToast('Failed to resume campaign');



        }



    } catch (e) {



        console.error(e);



        showToast('Error resuming campaign');



    }



};







window.deleteCampaign = async function(id) {



    if (!confirm('Are you sure you want to delete this campaign? This action cannot be undone.')) return;



    



    try {



        const res = await apiCall('/campaigns/' + id, 'DELETE');



        if (res.ok) {



            showToast('Campaign deleted successfully', 'success');



            fetchDashboard();



            if (document.getElementById('cold-mail-list') && document.getElementById('cold-mail-list').classList.contains('active')) {



                renderColdMailList();



            }



            if (document.getElementById('campaigns-list') && document.getElementById('campaigns-list').classList.contains('active')) {



                renderNewsletterList();



            }



        } else {



            const err = await res.json().catch(() => ({}));



            showToast(err.detail || 'Failed to delete campaign', 'error');



        }



    } catch(e) {



        showToast('Error deleting campaign', 'error');



    }



};







// ============================================================



// COLD MAIL TABS



// ============================================================



function setupColdMailTabs() {



    const tabs = document.querySelectorAll('.clean-tab[data-coldtab]');



    const contents = document.querySelectorAll('.cold-tab-content');







    tabs.forEach(tab => {



        tab.addEventListener('click', () => {



            // Remove active classes



            tabs.forEach(t => {



                t.classList.remove('active');



                t.style.fontWeight = '600';



                t.style.color = 'var(--text-muted)';



                t.style.borderBottom = 'none';



            });



            // Hide contents



            contents.forEach(c => c.style.display = 'none');







            // Add active to clicked



            tab.classList.add('active');



            tab.style.fontWeight = '700';



            tab.style.color = 'var(--p)';



            tab.style.borderBottom = '3px solid var(--p)';







            // Show matching content



            const tabName = tab.getAttribute('data-coldtab');



            const targetId = 'cold-tab-' + tabName;



            const targetEl = document.getElementById(targetId);



            if (targetEl) targetEl.style.display = 'block';



            



            if (tabName === 'analytics' && window.currentCampaignId) {



                window.populateColdAnalytics(window.currentCampaignId);



            }



        });



    });



}







// BUG-1 FIX: switchColdTab was called in multiple places but never defined



window.switchColdTab = function(tabName) {



    const tabs = document.querySelectorAll('.clean-tab[data-coldtab]');



    const contents = document.querySelectorAll('.cold-tab-content');



    tabs.forEach(t => {



        t.classList.remove('active');



        t.style.fontWeight = '600';



        t.style.color = 'var(--text-muted)';



        t.style.borderBottom = 'none';



    });



    contents.forEach(c => c.style.display = 'none');



    const activeTab = document.querySelector(`.clean-tab[data-coldtab="${tabName}"]`);



    if (activeTab) {



        activeTab.classList.add('active');



        activeTab.style.fontWeight = '700';



        activeTab.style.color = 'var(--p)';



        activeTab.style.borderBottom = '3px solid var(--p)';



    }



    const targetEl = document.getElementById('cold-tab-' + tabName);



    if (targetEl) targetEl.style.display = 'block';



    



    if (tabName === 'analytics' && window.currentCampaignId) {



        window.populateColdAnalytics(window.currentCampaignId);



    }



    if (tabName === 'schedule' && window.currentCampaignId) {



        loadScheduleTab(window.currentCampaignId);



    }



};







// Load campaign schedule settings into the Schedule tab



function loadScheduleTab(campaignId) {



    if (!window.lastFetchedCampaigns) return;



    const c = window.lastFetchedCampaigns.find(x => x.id === campaignId);



    if (!c) return;







    // Timezone



    const tzEl = document.getElementById('sch-timezone');



    if (tzEl && c.timezone) {



        tzEl.value = c.timezone;



    }







    // Sending days



    const dayMap = {Mon:'sch-day-mon', Tue:'sch-day-tue', Wed:'sch-day-wed', Thu:'sch-day-thu', Fri:'sch-day-fri', Sat:'sch-day-sat', Sun:'sch-day-sun'};



    // Reset all first



    Object.values(dayMap).forEach(id => {



        const el = document.getElementById(id);



        if (el) el.checked = false;



    });



    if (c.sending_days) {



        try {



            const days = JSON.parse(c.sending_days);



            days.forEach(d => {



                const el = document.getElementById(dayMap[d]);



                if (el) el.checked = true;



            });



        } catch(e) {}



    } else {



        // Default: Mon-Fri



        ['sch-day-mon','sch-day-tue','sch-day-wed','sch-day-thu','sch-day-fri'].forEach(id => {



            const el = document.getElementById(id);



            if (el) el.checked = true;



        });



    }







    // Start / End time



    const startEl = document.getElementById('sch-start-time');



    const endEl = document.getElementById('sch-end-time');



    if (startEl) {



        const h = c.start_hour !== null && c.start_hour !== undefined ? c.start_hour : 0;



        startEl.value = String(h).padStart(2,'0') + ':00';



    }



    if (endEl) {

        let h = c.end_hour !== null && c.end_hour !== undefined ? c.end_hour : 0;

        if (h === 24) h = 0;

        endEl.value = String(h).padStart(2,'0') + ':00';

    }



    const cDelayMinEl = document.getElementById('campaign-delay-min');

    const cDelayMaxEl = document.getElementById('campaign-delay-max');

    if (cDelayMinEl) cDelayMinEl.value = (c.delay_min !== null && c.delay_min !== undefined) ? c.delay_min : 30;

    if (cDelayMaxEl) cDelayMaxEl.value = (c.delay_max !== null && c.delay_max !== undefined) ? c.delay_max : 90;

}







// Save Campaign Options (track_opens, track_clicks, use_unsubscribe, max_emails, ramp_up)

window.saveCampaignOptions = async function(prefix = 'cold') {

    if (!window.currentCampaignId) { showToast('No campaign selected', 'error'); return; }

    const btn = document.getElementById(`${prefix}-save-options-btn`);

    if (btn) { btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...'; btn.disabled = true; }



    const trackOpensEl = document.getElementById(`${prefix}-track-opens`);

    const trackClicksEl = document.getElementById(`${prefix}-track-clicks`);

    const unsubscribeEl = document.getElementById(`${prefix}-use-unsubscribe`);

    const maxEmailsEl = document.getElementById(`${prefix}-max-emails`);

    const rampUpEl = document.getElementById(`${prefix}-ramp-up`);



    const payload = {};

    if (trackOpensEl) payload.track_opens = trackOpensEl.value === '1';

    if (trackClicksEl) payload.track_clicks = trackClicksEl.value === '1';

    if (unsubscribeEl) payload.use_unsubscribe = unsubscribeEl.value === '1';

    if (maxEmailsEl) payload.max_emails_per_day = parseInt(maxEmailsEl.value) || 50;

    if (rampUpEl) payload.daily_ramp_up = parseInt(rampUpEl.value) || 0;

    

    if (window.getSelectedSenderIds) {

        payload.selected_sender_ids = window.getSelectedSenderIds(`${prefix}-sender-accounts-list`);

    }



    try {

        const res = await apiCall(`/campaigns/${window.currentCampaignId}/save-options`, 'POST', payload);

        if (res && res.ok) {

            showToast('✅ Options saved!', 'success');

            // Update local cache

            if (window.lastFetchedCampaigns) {

                const idx = window.lastFetchedCampaigns.findIndex(x => x.id === window.currentCampaignId);

                if (idx !== -1) {

                    if (payload.track_opens !== undefined) window.lastFetchedCampaigns[idx].track_opens = payload.track_opens;

                    if (payload.track_clicks !== undefined) window.lastFetchedCampaigns[idx].track_clicks = payload.track_clicks;

                    if (payload.use_unsubscribe !== undefined) window.lastFetchedCampaigns[idx].use_unsubscribe = payload.use_unsubscribe;

                    if (payload.max_emails_per_day !== undefined) window.lastFetchedCampaigns[idx].max_emails_per_day = payload.max_emails_per_day;

                    if (payload.daily_ramp_up !== undefined) window.lastFetchedCampaigns[idx].daily_ramp_up = payload.daily_ramp_up;

                }

            }

        } else {

            const d = res ? await res.json().catch(() => ({})) : {};

            showToast(d.detail || 'Failed to save options', 'error');

        }

    } catch(e) {

        showToast('Error saving options', 'error');

    }

    if (btn) { btn.innerHTML = 'Save Options'; btn.disabled = false; }

};



// Save the Schedule tab settings



window.saveSchedule = async function() {



    const btn = document.getElementById('sch-save-btn');



    if (btn) { btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...'; btn.disabled = true; }







    const dayMap = {Mon:'sch-day-mon', Tue:'sch-day-tue', Wed:'sch-day-wed', Thu:'sch-day-thu', Fri:'sch-day-fri', Sat:'sch-day-sat', Sun:'sch-day-sun'};



    const selectedDays = Object.entries(dayMap)



        .filter(([day, id]) => document.getElementById(id)?.checked)



        .map(([day]) => day);







    const startVal = document.getElementById('sch-start-time')?.value || '00:00';



    const endVal = document.getElementById('sch-end-time')?.value || '00:00';



    const startHour = parseInt(startVal.split(':')[0], 10) || 0;



    const endHour = parseInt(endVal.split(':')[0], 10) || 0;



    const tz = document.getElementById('sch-timezone')?.value || 'UTC';







    const delayMin = parseInt(document.getElementById('sch-delay-min')?.value) || 30;

    const delayMax = parseInt(document.getElementById('sch-delay-max')?.value) || 90;



    const payload = {

        sending_days: JSON.stringify(selectedDays),

        start_hour: startHour,

        end_hour: endHour === 0 ? 24 : endHour,  // 00:00 end = midnight = 24 (all day)

        timezone: tz,

        delay_min: delayMin,

        delay_max: delayMax

    };







    if (!window.currentCampaignId) {

        // Auto-save as draft so schedule persists

        try {

            const subEl = document.getElementById('inst-subject');

            const bodyEl = document.getElementById('inst-body');

            const draftPayload = {

                subject: (subEl ? subEl.value : '') || 'Untitled Campaign',

                body: bodyEl ? bodyEl.value : '',

                type: 'cold_mail',

                leads: [],

                is_draft: true,

                sending_days: payload.sending_days,

                start_hour: payload.start_hour,

                end_hour: payload.end_hour,

                timezone: payload.timezone,

                delay_min: payload.delay_min,

                delay_max: payload.delay_max

            };

            if (window.getSelectedSenderIds) {

                draftPayload.selected_sender_ids = window.getSelectedSenderIds('cold-sender-accounts-list');

            }

            const draftRes = await apiCall('/campaigns/send', 'POST', draftPayload);

            if (draftRes && draftRes.ok) {

                const draftData = await draftRes.json();

                window.currentCampaignId = draftData.campaign_id;

                if (!window.lastFetchedCampaigns) window.lastFetchedCampaigns = [];

                window.lastFetchedCampaigns.push({

                    id: draftData.campaign_id, subject: draftPayload.subject, body: draftPayload.body,

                    type: 'cold_mail', status: 'draft',

                    sending_days: payload.sending_days, start_hour: payload.start_hour,

                    end_hour: payload.end_hour, timezone: payload.timezone,

                    delay_min: payload.delay_min, delay_max: payload.delay_max

                });

                showToast('Schedule saved! Draft created.', 'success');

            } else {

                const d = await draftRes.json().catch(() => ({}));

                showToast(d.detail || 'Failed to save schedule', 'error');

            }

        } catch(e) {

            showToast('Error saving schedule', 'error');

        }

        if (btn) { btn.innerHTML = '<i class="fa-solid fa-floppy-disk" style="margin-right:6px;"></i>Save Schedule'; btn.disabled = false; }

        return;

    }







    try {



        const res = await apiCall(`/campaigns/${window.currentCampaignId}/save-schedule`, 'POST', payload);



        if (res && res.ok) {



            showToast('✅ Schedule saved successfully!', 'success');



            // Update local cache



            if (window.lastFetchedCampaigns) {



                const idx = window.lastFetchedCampaigns.findIndex(x => x.id === window.currentCampaignId);



                if (idx !== -1) {



                    window.lastFetchedCampaigns[idx].sending_days = payload.sending_days;



                    window.lastFetchedCampaigns[idx].start_hour = payload.start_hour;



                    window.lastFetchedCampaigns[idx].end_hour = payload.end_hour;



                    window.lastFetchedCampaigns[idx].timezone = payload.timezone;



                    window.lastFetchedCampaigns[idx].delay_min = payload.delay_min;



                    window.lastFetchedCampaigns[idx].delay_max = payload.delay_max;



                }



            }



        } else {



            const d = await res.json().catch(() => ({}));



            showToast(d.detail || 'Failed to save schedule', 'error');



        }



    } catch(e) {



        showToast('Error saving schedule', 'error');



    }







    if (btn) { btn.innerHTML = '<i class="fa-solid fa-floppy-disk" style="margin-right:6px;"></i>Save Schedule'; btn.disabled = false; }



};







// ============================================================



// POPULATE WORLD TIMEZONES



// ============================================================



function populateTimezones() {



    const schTimezone = document.getElementById('sch-timezone');



    const vbSchTimezone = document.getElementById('vb-sch-timezone');



    



    try {



        let timezones = [];

        try {

            timezones = Intl.supportedValuesOf('timeZone');

        } catch (e) {

            timezones = ['UTC', 'America/New_York', 'America/Los_Angeles', 'Europe/London', 'Asia/Kolkata', 'Asia/Dhaka', 'Australia/Sydney'];

        }



        const userTz = Intl.DateTimeFormat().resolvedOptions().timeZone;



        



        let html = '';



        timezones.forEach(tz => {



            const selected = (tz === userTz) ? 'selected' : '';



            html += `<option value="${tz}" ${selected}>${tz.replace('_', ' ')}</option>`;



        });



        



        if (schTimezone) schTimezone.innerHTML = html;



        if (vbSchTimezone) vbSchTimezone.innerHTML = html;



        



        if (typeof Choices !== 'undefined') {

            if (schTimezone) {

                new Choices(schTimezone, {

                    searchEnabled: true,

                    itemSelectText: '',

                    shouldSort: false

                });

            }

            if (vbSchTimezone) {

                new Choices(vbSchTimezone, {

                    searchEnabled: true,

                    itemSelectText: '',

                    shouldSort: false

                });

            }

        }



    } catch (e) {



        console.warn("Timezone API not supported by browser", e);



    }



}







// ============================================================



// VISUAL BUILDER TABS



// ============================================================



window.switchVbTab = function(tabName) {



    const tabs = document.querySelectorAll('.vb-tab[data-vbtab]');



    const contents = document.querySelectorAll('.vb-tab-content');







    // Remove active styling from all tabs



    tabs.forEach(t => {



        t.classList.remove('active');



        t.style.fontWeight = '600';



        t.style.color = 'var(--text-muted)';



        t.style.borderBottom = 'none';



    });







    // Hide all contents



    contents.forEach(c => c.style.display = 'none');







    // Find the clicked tab and corresponding content



    const targetTab = document.querySelector(`.vb-tab[data-vbtab="${tabName}"]`);



    const targetContent = document.getElementById('vb-tab-' + tabName);







    // Apply active styling



    if (targetTab) {



        targetTab.classList.add('active');



        targetTab.style.fontWeight = '700';



        targetTab.style.color = 'var(--p)';



        targetTab.style.borderBottom = '3px solid var(--p)';



    }







    // Show content

    if (targetContent) {

        targetContent.style.display = 'block';

    }



    // Load analytics if needed

    if (tabName === 'analytics' && window.currentCampaignId) {

        window.populateVbAnalytics(window.currentCampaignId);

    }

};







function setupVisualBuilderTabs() {



    const tabs = document.querySelectorAll('.vb-tab[data-vbtab]');



    tabs.forEach(tab => {



        tab.addEventListener('click', () => {



            window.switchVbTab(tab.getAttribute('data-vbtab'));



        });



    });



}



// SETTINGS



// ============================================================



window.loadedAIKeys = {};

async function loadSmtpStatus() {
    const statusEl = document.getElementById('smtp-status');
    if (!statusEl) return;
    try {
        const res = await apiCall('/settings/smtp', 'GET');
        if (res.ok) {
            const data = await res.json();
            if (data.has_account) {
                statusEl.innerHTML = `✅ <strong>Saved Account:</strong> ${data.email} &nbsp;|&nbsp; Host: ${data.smtp_host}:${data.smtp_port} &nbsp;|&nbsp; Name: ${data.from_name || '-'}`;
                statusEl.style.cssText = 'display:block; margin-top:20px; padding:14px 18px; border-radius:10px; background:#f0fdf4; color:#16a34a; border:1px solid #bbf7d0; font-size:14px;';
            } else {
                statusEl.textContent = '⚠️ No email account saved yet. Fill the form below and click Save Changes.';
                statusEl.style.cssText = 'display:block; margin-top:20px; padding:14px 18px; border-radius:10px; background:#fffbeb; color:#b45309; border:1px solid #fcd34d; font-size:14px;';
            }
        }
    } catch(e) {}
}

function setupSettings() {

    // --- Load existing SMTP account status on page open ---
    (async () => {
        const statusEl = document.getElementById('smtp-status');
        if (!statusEl) return;
        try {
            const res = await apiCall('/settings/smtp', 'GET');
            if (res.ok) {
                const data = await res.json();
                if (data.has_account) {
                    statusEl.innerHTML = `✅ <strong>Saved Account:</strong> ${data.email} &nbsp;|&nbsp; Host: ${data.smtp_host}:${data.smtp_port} &nbsp;|&nbsp; Name: ${data.from_name || '-'}`;
                    statusEl.className = 'alert success';
                    statusEl.style.display = 'block';
                } else {
                    statusEl.textContent = '⚠️ No email account saved yet. Fill the form below and click Save Changes.';
                    statusEl.className = 'alert warning';
                    statusEl.style.display = 'block';
                }
            }
        } catch(e) {}
    })();

    const providerSelect = document.getElementById('smtp-provider');

    if (providerSelect) {

        providerSelect.addEventListener('change', () => {

            const smtpFields = document.getElementById('smtp-fields');

            if (smtpFields) smtpFields.style.display = 'block';

        });

    }







    const saveSmtpBtn = document.getElementById('save-smtp-btn');



    if (saveSmtpBtn) {



        saveSmtpBtn.addEventListener('click', async () => {



            const provider = document.getElementById('smtp-provider').value;



            let body = { provider };



            if (provider === 'smtp') {

                body.smtp_host = document.getElementById('smtp-host').value;

                body.smtp_user = document.getElementById('smtp-user').value;

                body.smtp_pass = document.getElementById('smtp-pass').value;

                body.smtp_port = parseInt(document.getElementById('smtp-port').value);

                body.from_name = document.getElementById('smtp-from-name').value;

            }



            try {



                const res = await apiCall('/settings/smtp', 'POST', body);



                const data = await res.json();



                const statusEl = document.getElementById('smtp-status');



                if (statusEl) {



                    statusEl.textContent = res.ok ? 'Settings saved!' : (data.detail || 'Error');



                    statusEl.className = res.ok ? 'alert success' : 'alert error';



                    statusEl.style.display = 'block';



                }



            } catch(e) { showToast('Error saving settings', 'error'); }



        });



    }







    const testBtn = document.getElementById('test-smtp-btn');



    if (testBtn) {



        testBtn.addEventListener('click', async () => {



            testBtn.textContent = 'Testing...';



            testBtn.disabled = true;



            try {

                const res = await apiCall('/settings/test-smtp', 'POST');
                const data = await res.json();

                if (res.ok) {
                    showToast(data.message || 'SMTP Connection Successful!', 'success');
                } else {
                    const errMsg = data.detail || data.message || 'Connection failed';
                    showToast(errMsg, 'error');
                }

            } catch(e) { showToast('Error testing connection: ' + (e.message || e), 'error'); }



            testBtn.textContent = 'Test Connection';



            testBtn.disabled = false;



        });



    }







    const saveGeminiBtn = document.getElementById('save-gemini-btn');



    if (saveGeminiBtn) {



        saveGeminiBtn.addEventListener('click', async () => {



            const geminiKey = document.getElementById('gemini-api-key').value;



            const groqKeyEl = document.getElementById('groq-api-key');

            const groqKey = groqKeyEl ? groqKeyEl.value : '';

            

            const openaiKeyEl = document.getElementById('openai-api-key');

            const openaiKey = openaiKeyEl ? openaiKeyEl.value : '';

            

            const anthropicKeyEl = document.getElementById('anthropic-api-key');

            const anthropicKey = anthropicKeyEl ? anthropicKeyEl.value : '';

            

            const deepseekKeyEl = document.getElementById('deepseek-api-key');

            const deepseekKey = deepseekKeyEl ? deepseekKeyEl.value : '';



            try {



                if (geminiKey) {
                    try { const r = await apiCall('/settings/gemini', 'POST', { gemini_api_key: geminiKey }); window.loadedAIKeys['gemini'] = geminiKey; document.getElementById('gemini-api-key').value = ''; window.updateInputState('gemini-api-key', true); alert('Gemini key saved!'); } catch(e) { alert('Failed to save Gemini key: ' + e.message); }
                }
                if (groqKey) {
                    try { const r = await apiCall('/settings/groq', 'POST', { groq_api_key: groqKey }); window.loadedAIKeys['groq'] = groqKey; document.getElementById('groq-api-key').value = ''; window.updateInputState('groq-api-key', true); alert('Groq key saved!'); } catch(e) { alert('Failed to save Groq key: ' + e.message); }
                }
                if (openaiKey) {
                    try { const r = await apiCall('/settings/openai', 'POST', { openai_api_key: openaiKey }); window.loadedAIKeys['openai'] = openaiKey; document.getElementById('openai-api-key').value = ''; window.updateInputState('openai-api-key', true); alert('OpenAI key saved!'); } catch(e) { alert('Failed to save OpenAI key: ' + e.message); }
                }
                if (anthropicKey) {
                    try { const r = await apiCall('/settings/anthropic', 'POST', { anthropic_api_key: anthropicKey }); window.loadedAIKeys['anthropic'] = anthropicKey; document.getElementById('anthropic-api-key').value = ''; window.updateInputState('anthropic-api-key', true); alert('Anthropic key saved!'); } catch(e) { alert('Failed to save Anthropic key: ' + e.message); }
                }
                if (deepseekKey) {
                    try { const r = await apiCall('/settings/deepseek', 'POST', { deepseek_api_key: deepseekKey }); window.loadedAIKeys['deepseek'] = deepseekKey; document.getElementById('deepseek-api-key').value = ''; window.updateInputState('deepseek-api-key', true); alert('DeepSeek key saved!'); } catch(e) { alert('Failed to save DeepSeek key: ' + e.message); }
                }
                verifyAllAIKeys();

            } catch(e) { showToast('Error saving keys', 'error'); }



        });



    }







    

    async function verifyAllAIKeys() {
        const providers = ['gemini', 'groq', 'openai', 'anthropic', 'deepseek'];
        const verifyPromises = providers.map(async (provider) => {
            const keyEl = document.getElementById(provider + '-api-key');
            let key = (keyEl && keyEl.value) ? keyEl.value : window.loadedAIKeys[provider];
            const badge = document.getElementById('badge-' + provider);
            if (!badge) return;

            if (!key) {
                badge.innerHTML = `<span style="display:inline-block;width:4px;height:4px;background:#ef4444;border-radius:50%;margin-right:4px;vertical-align:middle;margin-bottom:1px;"></span>No Key`;
                badge.style.background = '#fee2e2';
                badge.style.color = '#ef4444';
                return;
            }
            
            badge.innerHTML = `<i class="fa-solid fa-spinner fa-spin" style="margin-right:4px;font-size:9px;"></i>Checking`;
            badge.style.background = '#e0e7ff';
            badge.style.color = '#4338ca';

            try {
                // If key is boolean true from backend, convert to string so backend knows to fetch from DB
                const res = await apiCall('/settings/verify_key', 'POST', { provider, api_key: String(key) });
                const data = await res.json();
                
                if (data.status === 'valid') {
                    badge.innerHTML = `<span style="display:inline-block;width:4px;height:4px;background:#10b981;border-radius:50%;margin-right:4px;vertical-align:middle;margin-bottom:1px;"></span>Key Active`;
                    badge.style.background = '#dcfce7';
                    badge.style.color = '#059669';
                } else if (data.status === 'invalid') {
                    badge.innerHTML = `<span style="display:inline-block;width:4px;height:4px;background:#ca8a04;border-radius:50%;margin-right:4px;vertical-align:middle;margin-bottom:1px;"></span>Invalid Key`;
                    badge.style.background = '#fef08a';
                    badge.style.color = '#ca8a04';
                } else {
                    badge.innerHTML = `<span style="display:inline-block;width:4px;height:4px;background:#ef4444;border-radius:50%;margin-right:4px;vertical-align:middle;margin-bottom:1px;"></span>No Key`;
                    badge.style.background = '#fee2e2';
                    badge.style.color = '#ef4444';
                }
            } catch (e) {
                badge.innerHTML = `<span style="display:inline-block;width:4px;height:4px;background:#ef4444;border-radius:50%;margin-right:4px;vertical-align:middle;margin-bottom:1px;"></span>API Error`;
                badge.style.background = '#fee2e2';
                badge.style.color = '#ef4444';
            }
        });
        await Promise.all(verifyPromises);
    }



    // Load existing settings



    apiCall('/settings/all').then(async res => {



        if (!res.ok) return;



        const s = await res.json();
        window.loadedAIKeys['gemini'] = !!s.has_gemini_api_key;
        window.loadedAIKeys['groq'] = !!s.has_groq_api_key;
        window.loadedAIKeys['openai'] = !!s.has_openai_api_key;
        window.loadedAIKeys['anthropic'] = !!s.has_anthropic_api_key;
        window.loadedAIKeys['deepseek'] = !!s.has_deepseek_api_key;




        window.updateInputState('gemini-api-key', !!s.has_gemini_api_key);

        window.updateInputState('groq-api-key', !!s.has_groq_api_key);

        window.updateInputState('openai-api-key', !!s.has_openai_api_key);

        window.updateInputState('anthropic-api-key', !!s.has_anthropic_api_key);

        window.updateInputState('deepseek-api-key', !!s.has_deepseek_api_key);

        verifyAllAIKeys();



    }).catch((e) => {
        console.error("Settings fetch failed:", e);
        document.querySelectorAll('[id^=badge-]').forEach(b => {
            if(b) {
                b.innerHTML = `<span style="display:inline-block;width:4px;height:4px;background:#ef4444;border-radius:50%;margin-right:4px;vertical-align:middle;margin-bottom:1px;"></span>Server Down`;
                b.style.background = '#fee2e2';
                b.style.color = '#ef4444';
            }
        });
        alert('Server is failing to load API keys! Error: ' + e.message + '\nPlease check cPanel Error Logs!');
    });



}







// ============================================================



// CAMPAIGN BUILDER (Visual Drag & Drop)



// ============================================================



function setupCampaignBuilder() {



    const canvasWrapper = document.querySelector('.builder-canvas-wrapper');



    const canvas = document.getElementById('builder-canvas');



    const defaultSidebar = document.getElementById('builder-sidebar-default');



    const editSidebar = document.getElementById('builder-sidebar-edit');



    const propertyFields = document.getElementById('property-fields');



    const mcEditTitle = document.getElementById('mc-edit-title');



    if (!canvas || !canvasWrapper) return;







    window.switchMcTab = function(tab) {



        document.querySelectorAll('.mc-tab').forEach(t => {



            t.classList.remove('active');



            t.style.borderBottomColor = 'transparent';



            t.style.color = 'var(--text-muted)';



        });



        const selectedTab = document.querySelector(`.mc-tab[data-mctab="${tab}"]`);



        if(selectedTab) {



            selectedTab.classList.add('active');



            selectedTab.style.borderBottomColor = 'var(--p)';



            selectedTab.style.color = 'var(--p)';



        }



        



        document.querySelectorAll('.mc-tab-content').forEach(c => c.style.display = 'none');



        const content = document.getElementById(`mc-tab-${tab}`);



        if (content) content.style.display = 'block';



    };







    window.closeMcEdit = () => {



        if (defaultSidebar && editSidebar) {



            editSidebar.style.display = 'none';



            defaultSidebar.style.display = 'flex';



        }



        document.querySelectorAll('.email-block').forEach(b => b.classList.remove('selected'));



        selectedBlock = null;



    };







    let canvasHistory = [];



    let historyIndex = -1;







    window.saveState = () => {



        const placeholder = canvas.querySelector('.canvas-placeholder');



        if (placeholder) return;



        const state = canvas.innerHTML;



        if (historyIndex >= 0 && canvasHistory[historyIndex] === state) return;



        canvasHistory = canvasHistory.slice(0, historyIndex + 1);



        canvasHistory.push(state);



        historyIndex++;



    };







    const bindCanvasEvents = () => {



        document.querySelectorAll('.email-block').forEach(block => {



            block.draggable = true;



            block.addEventListener('dragstart', (e) => {



                draggedCanvasBlock = block;



                e.dataTransfer.setData('type', 'reorder');



                setTimeout(() => block.style.opacity = '0.5', 0);



            });



            block.addEventListener('dragend', () => {



                draggedCanvasBlock = null;



                block.style.opacity = '1';



            });



        });



    };







    window.undo = () => {



        if (historyIndex > 0) {



            historyIndex--;



            canvas.innerHTML = canvasHistory[historyIndex];



            bindCanvasEvents();



        } else if (historyIndex === 0) {



            // Revert to empty state



            historyIndex = -1;



            canvas.innerHTML = '<div class="canvas-placeholder" style="text-align:center;padding:60px 20px;color:var(--text-muted);border:2px dashed var(--border);border-radius:8px;"><i class="fa-solid fa-layer-group" style="font-size:32px;color:#cbd5e1;margin-bottom:16px;display:block;"></i>Drag blocks here to build your email</div>';



        }



    };







    window.redo = () => {



        if (historyIndex < canvasHistory.length - 1) {



            historyIndex++;



            canvas.innerHTML = canvasHistory[historyIndex];



            bindCanvasEvents();



        }



    };







    window.saveAsTemplate = () => {



        const name = prompt("Enter a name for this template:");



        if (!name) return;



        const html = canvas.innerHTML;



        const templates = JSON.parse(localStorage.getItem('saved_templates') || '{}');



        templates[name] = html;



        localStorage.setItem('saved_templates', JSON.stringify(templates));



        showToast('Template saved successfully!');



    };







    let selectedBlock = null;



    const dropIndicator = document.createElement('div');



    dropIndicator.className = 'drop-indicator';



    let currentDropTarget = null;







    canvasWrapper.addEventListener('dragover', e => {



        e.preventDefault();



        const blocks = Array.from(canvas.querySelectorAll('.email-block'));



        if (blocks.length === 0) return;



        let closestBlock = null, closestOffset = Number.NEGATIVE_INFINITY;



        blocks.forEach(block => {



            const box = block.getBoundingClientRect();



            const offset = e.clientY - box.top - box.height / 2;



            if (offset < 0 && offset > closestOffset) { closestOffset = offset; closestBlock = block; }



        });



        if (closestBlock) { canvas.insertBefore(dropIndicator, closestBlock); currentDropTarget = closestBlock; }



        else { canvas.appendChild(dropIndicator); currentDropTarget = null; }



        dropIndicator.style.display = 'block';



    });







    let draggedCanvasBlock = null;







    canvasWrapper.addEventListener('drop', e => {



        e.preventDefault();



        dropIndicator.style.display = 'none';



        const type = e.dataTransfer.getData('type');



        if (!type) return;



        



        if (type === 'reorder' && draggedCanvasBlock) {



            if (currentDropTarget) {



                canvas.insertBefore(draggedCanvasBlock, currentDropTarget);



            } else {



                canvas.appendChild(draggedCanvasBlock);



            }



        } else {



            window.addBlockToCanvas(type, currentDropTarget);



        }



        window.saveState();



    });







    window.drag = e => {



        const b = e.target.closest('.draggable-block');



        if (b) e.dataTransfer.setData('type', b.getAttribute('data-type'));



    };







    window.addBlockToCanvas = (type, targetBlock = null, customContent = null) => {



        const placeholder = canvas.querySelector('.canvas-placeholder');



        if (placeholder) placeholder.remove();



        const block = document.createElement('div');



        block.className = 'email-block';



        block.setAttribute('data-type', type);



        block.draggable = true;



        



        block.addEventListener('dragstart', (e) => {



            draggedCanvasBlock = block;



            e.dataTransfer.setData('type', 'reorder');



            setTimeout(() => block.style.opacity = '0.5', 0);



        });



        block.addEventListener('dragend', () => {



            draggedCanvasBlock = null;



            block.style.opacity = '1';



        });



        



        const actions = document.createElement('div');



        actions.className = 'block-actions';



        actions.innerHTML = `



            <div class="action-btn" title="Drag to reorder" style="cursor:grab;"><i class="fa-solid fa-arrows-up-down-left-right"></i></div>



            <div class="action-btn edit" title="Edit"><i class="fa-solid fa-pencil"></i></div>



            <div class="action-btn duplicate" title="Duplicate"><i class="fa-solid fa-copy"></i></div>



            <div class="action-btn delete" title="Delete"><i class="fa-solid fa-trash"></i></div>



        `;



        block.appendChild(actions);



        const content = document.createElement('div');



        content.className = 'block-content';



        



        if (customContent) {



            content.innerHTML = customContent;



        } else {



            if (type === 'text') {



                content.innerHTML = `<p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#241C15;line-height:1.5;padding:20px;">New Text Block. Click to edit.</p>`;



            }



            else if (type === 'image') content.innerHTML = `<img src="https://via.placeholder.com/600x200?text=Your+Image" style="max-width:100%;height:auto;display:block;">`;



            else if (type === 'button') content.innerHTML = `<div style="text-align:center;padding:20px;"><a href="#" style="background:#6366f1;color:#fff;padding:12px 28px;text-decoration:none;display:inline-block;border-radius:8px;font-weight:bold;font-family:Helvetica,Arial,sans-serif;">Click Me</a></div>`;



            else if (type === 'divider') content.innerHTML = `<hr style="border:0;border-top:2px solid #E0E0DF;margin:20px 0;">`;



            else if (type === 'spacer') content.innerHTML = `<div style="height:40px;line-height:40px;">&nbsp;</div>`;



            else if (type === 'socials') content.innerHTML = `<div style="text-align:center;padding:20px;">



                <a href="" style="display:none;margin:0 8px;"><img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" width="32" height="32" alt="Facebook"></a>



                <a href="" style="display:none;margin:0 8px;"><img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" width="32" height="32" alt="Twitter"></a>



                <a href="" style="display:none;margin:0 8px;"><img src="https://cdn-icons-png.flaticon.com/512/174/174855.png" width="32" height="32" alt="Instagram"></a>



                <a href="" style="display:none;margin:0 8px;"><img src="https://cdn-icons-png.flaticon.com/512/3536/3536505.png" width="32" height="32" alt="LinkedIn"></a>



                <a href="" style="display:none;margin:0 8px;"><img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" width="32" height="32" alt="YouTube"></a>



                <a href="" style="display:none;margin:0 8px;"><img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" width="32" height="32" alt="WhatsApp"></a>



                <a href="" style="display:none;margin:0 8px;"><img src="https://cdn-icons-png.flaticon.com/512/2111/2111646.png" width="32" height="32" alt="Telegram"></a>



                <a href="" style="display:none;margin:0 8px;"><img src="https://cdn-icons-png.flaticon.com/512/1006/1006771.png" width="32" height="32" alt="Website"></a>



            </div>`;



            else if (type === 'columns2') content.innerHTML = `



                <table width="100%" border="0" cellspacing="0" cellpadding="0">



                    <tr>



                        <td width="50%" valign="top" style="padding:10px;">



                            <p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#241C15;line-height:1.5;">Column 1 Content</p>



                        </td>



                        <td width="50%" valign="top" style="padding:10px;">



                            <p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#241C15;line-height:1.5;">Column 2 Content</p>



                        </td>



                    </tr>



                </table>`;



            else if (type === 'video') content.innerHTML = `



                <div style="text-align:center;padding:20px;">



                    <a href="#" style="display:block;position:relative;text-decoration:none;">



                        <img src="https://via.placeholder.com/600x300?text=Video+Thumbnail" style="max-width:100%;height:auto;display:block;border-radius:8px;">



                    </a>



                </div>`;



            else if (type === 'custom_html') content.innerHTML = `



                <div style="padding:20px;font-family:monospace;background:#f8fafc;color:#64748b;font-size:14px;border:1px dashed #cbd5e1;text-align:center;">



                    &lt;!-- Custom HTML Content --&gt;<br>Click to edit code



                </div>`;



            else if (type === 'header') content.innerHTML = `



                <div style="text-align:center;padding:20px 20px 10px 20px;">



                    <img src="https://via.placeholder.com/200x60?text=Your+Logo" style="max-width:100%;height:auto;display:inline-block;border-radius:0px;">



                </div>`;



            else if (type === 'footer') content.innerHTML = `



                <div style="text-align:center;padding:30px 20px;background:#f1f5f9;">



                    <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#64748b;line-height:1.5;margin-bottom:10px;">



                        Copyright © 2026 Your Company, All rights reserved.<br>



                        Our mailing address is:<br>



                        123 Main Street, Suite 400, City, State 12345



                    </p>



                    <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#64748b;line-height:1.5;margin:0;">



                        Want to change how you receive these emails?<br>



                        You can <a href="#" style="color:#6366f1;text-decoration:underline;">update your preferences</a> or <a href="#" style="color:#6366f1;text-decoration:underline;">unsubscribe from this list</a>.



                    </p>



                </div>`;



            else if (type === 'product') content.innerHTML = `



                <div style="padding:20px;text-align:center;">



                    <img src="https://via.placeholder.com/300x200?text=Product+Image" style="max-width:100%;height:auto;display:block;margin:0 auto 16px auto;border-radius:8px;">



                    <h3 style="font-family:Helvetica,Arial,sans-serif;font-size:20px;color:#1e293b;margin:0 0 8px 0;">Product Name</h3>



                    <p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#64748b;line-height:1.5;margin:0 0 16px 0;">Product description goes here.</p>



                    <a href="#" style="background:#4f46e5;color:#fff;padding:12px 24px;text-decoration:none;display:inline-block;border-radius:8px;font-weight:bold;font-family:Helvetica,Arial,sans-serif;">Buy Now - $99</a>



                </div>`;



            else if (type === 'image_group') content.innerHTML = `



                <table width="100%" border="0" cellspacing="0" cellpadding="0">



                    <tr>



                        <td width="50%" valign="top" style="padding:10px;">



                            <img src="https://via.placeholder.com/300x200?text=Image+1" style="max-width:100%;height:auto;display:block;border-radius:8px;">



                        </td>



                        <td width="50%" valign="top" style="padding:10px;">



                            <img src="https://via.placeholder.com/300x200?text=Image+2" style="max-width:100%;height:auto;display:block;border-radius:8px;">



                        </td>



                    </tr>



                </table>`;



        }



        



        block.appendChild(content);



        if (targetBlock) canvas.insertBefore(block, targetBlock);



        else canvas.appendChild(block);



        bindBlockEvents(block);



        setTimeout(() => selectBlock(null, block), 10);



        showToast('Block added');



    };







    function bindBlockEvents(block) {



        block.addEventListener('click', e => selectBlock(e, block));



        const actions = block.querySelector('.block-actions');



        if (!actions) return;



        actions.querySelector('.edit').addEventListener('click', e => { e.stopPropagation(); selectBlock(e, block); });



        actions.querySelector('.duplicate').addEventListener('click', e => {



            e.stopPropagation();



            const clone = block.cloneNode(true);



            block.parentNode.insertBefore(clone, block.nextSibling);



            bindBlockEvents(clone);



            showToast('Block duplicated');



        });



        actions.querySelector('.delete').addEventListener('click', e => {



            e.stopPropagation();



            if (confirm('Delete this block?')) {



                block.remove();



                if (selectedBlock === block) { window.closeMcEdit(); }



                if (canvas.querySelectorAll('.email-block').length === 0) canvas.innerHTML = '<div class="canvas-placeholder" style="text-align:center;padding:60px 20px;color:var(--text-muted);border:2px dashed var(--border);border-radius:8px;"><i class="fa-solid fa-layer-group" style="font-size:32px;color:#cbd5e1;margin-bottom:16px;display:block;"></i>Drag blocks here to build your email</div>';



                showToast('Block deleted');



            }



        });



    }







    function rgbToHex(rgb) {



        if (!rgb || rgb.indexOf('rgb') !== 0) return rgb;



        const a = rgb.split("(")[1].split(")")[0];



        const b = a.split(",");



        const c = b.map(x => {



            x = parseInt(x).toString(16);



            return (x.length == 1) ? "0" + x : x;



        });



        return "#" + c.join("");



    }







    function selectBlock(event, block) {



        if (event) event.stopPropagation();



        document.querySelectorAll('.email-block').forEach(b => b.classList.remove('selected'));



        selectedBlock = block;



        block.classList.add('selected');



        



        if (defaultSidebar && editSidebar) {



            defaultSidebar.style.display = 'none';



            editSidebar.style.display = 'flex';



        }



        const type = block.getAttribute('data-type');



        const contentDiv = block.querySelector('.block-content');



        propertyFields.innerHTML = '';



        if (mcEditTitle) mcEditTitle.textContent = type.charAt(0).toUpperCase() + type.slice(1);



        



        if (type === 'text') {



            const p = contentDiv.querySelector('p') || contentDiv;



            const currentSize = p.style.fontSize ? p.style.fontSize.replace('px', '') : '16';



            const currentColor = p.style.color ? rgbToHex(p.style.color) : '#241c15';



            const currentAlign = p.style.textAlign || 'left';



            propertyFields.innerHTML = `



                <div class="form-group"><label>Text (HTML allowed)</label><textarea id="prop-text" rows="5" style="width:100%;border:1px solid var(--border);border-radius:6px;padding:10px;font-family:monospace;">${contentDiv.innerHTML}</textarea></div>



                <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">



                    <div class="form-group"><label>Font Size (px)</label><input type="number" id="prop-text-size" value="${currentSize}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;"></div>



                    <div class="form-group"><label>Color</label><input type="color" id="prop-text-color" value="${currentColor}" style="width:100%;height:38px;padding:2px;border:1px solid var(--border);border-radius:6px;cursor:pointer;"></div>



                </div>



                <div class="form-group"><label>Alignment</label>



                    <select id="prop-text-align" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;">



                        <option value="left" ${currentAlign==='left'?'selected':''}>Left</option>



                        <option value="center" ${currentAlign==='center'?'selected':''}>Center</option>



                        <option value="right" ${currentAlign==='right'?'selected':''}>Right</option>



                        <option value="justify" ${currentAlign==='justify'?'selected':''}>Justify</option>



                    </select>



                </div>



            `;



            document.getElementById('prop-text').addEventListener('input', e => contentDiv.innerHTML = e.target.value);



            document.getElementById('prop-text-size').addEventListener('input', e => { if(p) p.style.fontSize = e.target.value + 'px'; });



            document.getElementById('prop-text-color').addEventListener('input', e => { if(p) p.style.color = e.target.value; });



            document.getElementById('prop-text-align').addEventListener('change', e => { if(p) p.style.textAlign = e.target.value; });



        } else if (type === 'image') {



            const img = contentDiv.querySelector('img');



            const currentRadius = img && img.style.borderRadius ? img.style.borderRadius.replace('px', '') : '0';



            propertyFields.innerHTML = `



                <div class="form-group">



                    <label>Image Source</label>



                    <div style="display:flex;gap:8px;margin-bottom:8px;">



                        <button id="btn-upload-image" class="btn primary" style="flex:1;padding:8px;font-size:13px;"><i class="fa-solid fa-upload"></i> Upload Image</button>



                        <input type="file" id="prop-img-file" accept="image/*" style="display:none;">



                    </div>



                    <input type="text" id="prop-img-src" value="${img ? img.src : ''}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;" placeholder="Or paste image URL..."><button type="button" onclick="openGalleryModal('prop-img-src')" class="secondary-btn" style="padding:6px 12px;font-size:12px;margin-top:6px;width:100%;background:#f1f5f9;border:1px solid #cbd5e1;border-radius:6px;color:#475569;cursor:pointer;"><i class="fa-solid fa-images"></i> Browse Gallery</button>



                </div>



                <div class="form-group">



                    <label>Border Radius (px)</label>



                    <input type="number" id="prop-img-radius" value="${currentRadius}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;">



                </div>



            `;



            const fileInput = document.getElementById('prop-img-file');



            document.getElementById('btn-upload-image').addEventListener('click', () => fileInput.click());



            fileInput.addEventListener('change', async e => {



                const file = e.target.files[0];



                if (!file) return;



                const formData = new FormData();



                formData.append('file', file);



                try {



                    const btn = document.getElementById('btn-upload-image');



                    const origText = btn.innerHTML;



                    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Uploading...';



                    btn.disabled = true;



                    const res = await fetch('/api/gallery/upload', { method: 'POST', body: formData, headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') } });



                    const data = await res.json();



                    btn.innerHTML = origText;



                    btn.disabled = false;



                    if (res.ok && data.url) {



                        document.getElementById('prop-img-src').value = data.url;



                        if (img) img.src = data.url;



                        showToast('Image uploaded successfully');



                    } else alert('Upload failed: ' + (data.detail || 'Unknown error'));



                } catch (err) {



                    console.error(err);



                    alert('Error uploading image');



                    document.getElementById('btn-upload-image').disabled = false;



                    document.getElementById('btn-upload-image').innerHTML = '<i class="fa-solid fa-upload"></i> Upload Image';



                }



            });



            document.getElementById('prop-img-src').addEventListener('input', e => {



                if (img) img.src = e.target.value;



            });



            document.getElementById('prop-img-radius').addEventListener('input', e => {



                if (img) img.style.borderRadius = e.target.value + 'px';



            });



        } else if (type === 'button') {



            const a = contentDiv.querySelector('a');



            const currentBg = a && a.style.background ? rgbToHex(a.style.background) : '#4f46e5';



            const currentColor = a && a.style.color ? rgbToHex(a.style.color) : '#ffffff';



            const currentRadius = a && a.style.borderRadius ? a.style.borderRadius.replace('px', '') : '8';



            propertyFields.innerHTML = `



                <div class="form-group"><label>Button Text</label><input type="text" id="prop-btn-text" value="${a ? a.innerText : 'Click Me'}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;"></div>



                <div class="form-group"><label>Button URL</label><input type="text" id="prop-btn-url" value="${a ? a.getAttribute('href') : '#'}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;"></div>



                <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">



                    <div class="form-group"><label>Background</label><input type="color" id="prop-btn-bg" value="${currentBg}" style="width:100%;height:38px;padding:2px;border:1px solid var(--border);border-radius:6px;cursor:pointer;"></div>



                    <div class="form-group"><label>Text Color</label><input type="color" id="prop-btn-color" value="${currentColor}" style="width:100%;height:38px;padding:2px;border:1px solid var(--border);border-radius:6px;cursor:pointer;"></div>



                </div>



                <div class="form-group"><label>Border Radius (px)</label><input type="number" id="prop-btn-radius" value="${currentRadius}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;"></div>



            `;



            document.getElementById('prop-btn-text').addEventListener('input', e => { if (a) a.innerText = e.target.value; });



            document.getElementById('prop-btn-url').addEventListener('input', e => { if (a) a.setAttribute('href', e.target.value); });



            document.getElementById('prop-btn-bg').addEventListener('input', e => { if (a) a.style.background = e.target.value; });



            document.getElementById('prop-btn-color').addEventListener('input', e => { if (a) a.style.color = e.target.value; });



            document.getElementById('prop-btn-radius').addEventListener('input', e => { if (a) a.style.borderRadius = e.target.value + 'px'; });



        } else if (type === 'divider') {



            propertyFields.innerHTML = `<p style="color:var(--text-muted);font-size:13px;text-align:center;padding:20px;">Divider has no properties.</p>`;



        } else if (type === 'spacer') {



            const div = contentDiv.querySelector('div');



            const currentHeight = div ? div.style.height.replace('px', '') : '40';



            propertyFields.innerHTML = `<div class="form-group"><label>Height (px)</label><input type="number" id="prop-spacer-height" value="${currentHeight}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;"></div>`;



            document.getElementById('prop-spacer-height').addEventListener('input', e => {



                if (div) {



                    div.style.height = e.target.value + 'px';



                    div.style.lineHeight = e.target.value + 'px';



                }



            });



        } else if (type === 'socials') {



            const links = contentDiv.querySelectorAll('a');



            let fb = '', tw = '', ig = '', li = '', yt = '', wa = '', tg = '', ws = '';



            links.forEach(a => {



                const img = a.querySelector('img');



                if (img) {



                    const href = a.getAttribute('href');



                    const val = (href === '#' || href === '') ? '' : href;



                    if (img.alt === 'Facebook') fb = val;



                    if (img.alt === 'Twitter') tw = val;



                    if (img.alt === 'Instagram') ig = val;



                    if (img.alt === 'LinkedIn') li = val;



                    if (img.alt === 'YouTube') yt = val;



                    if (img.alt === 'WhatsApp') wa = val;



                    if (img.alt === 'Telegram') tg = val;



                    if (img.alt === 'Website') ws = val;



                }



            });



            propertyFields.innerHTML = `



                <div class="form-group" style="margin-bottom:12px;"><label style="display:flex;align-items:center;gap:8px;"><img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" width="16" height="16"> Facebook URL</label><input type="text" id="prop-social-fb" value="${fb}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;margin-top:4px;"></div>



                <div class="form-group" style="margin-bottom:12px;"><label style="display:flex;align-items:center;gap:8px;"><img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" width="16" height="16"> Twitter URL</label><input type="text" id="prop-social-tw" value="${tw}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;margin-top:4px;"></div>



                <div class="form-group" style="margin-bottom:12px;"><label style="display:flex;align-items:center;gap:8px;"><img src="https://cdn-icons-png.flaticon.com/512/174/174855.png" width="16" height="16"> Instagram URL</label><input type="text" id="prop-social-ig" value="${ig}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;margin-top:4px;"></div>



                <div class="form-group" style="margin-bottom:12px;"><label style="display:flex;align-items:center;gap:8px;"><img src="https://cdn-icons-png.flaticon.com/512/3536/3536505.png" width="16" height="16"> LinkedIn URL</label><input type="text" id="prop-social-li" value="${li}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;margin-top:4px;"></div>



                <div class="form-group" style="margin-bottom:12px;"><label style="display:flex;align-items:center;gap:8px;"><img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" width="16" height="16"> YouTube URL</label><input type="text" id="prop-social-yt" value="${yt}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;margin-top:4px;"></div>



                <div class="form-group" style="margin-bottom:12px;"><label style="display:flex;align-items:center;gap:8px;"><img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" width="16" height="16"> WhatsApp URL</label><input type="text" id="prop-social-wa" value="${wa}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;margin-top:4px;"></div>



                <div class="form-group" style="margin-bottom:12px;"><label style="display:flex;align-items:center;gap:8px;"><img src="https://cdn-icons-png.flaticon.com/512/2111/2111646.png" width="16" height="16"> Telegram URL</label><input type="text" id="prop-social-tg" value="${tg}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;margin-top:4px;"></div>



                <div class="form-group" style="margin-bottom:12px;"><label style="display:flex;align-items:center;gap:8px;"><img src="https://cdn-icons-png.flaticon.com/512/1006/1006771.png" width="16" height="16"> Website URL</label><input type="text" id="prop-social-ws" value="${ws}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;margin-top:4px;"></div>



                <p style="font-size:12px;color:var(--text-muted);margin-top:8px;">* Leave blank to hide the icon</p>



            `;



            const updateSocial = (alt, val) => {



                links.forEach(a => {



                    const img = a.querySelector('img');



                    if (img && img.alt === alt) {



                        a.setAttribute('href', val || '#');



                        a.style.display = val ? 'inline-block' : 'none';



                    }



                });



            };



            document.getElementById('prop-social-fb').addEventListener('input', e => updateSocial('Facebook', e.target.value));



            document.getElementById('prop-social-tw').addEventListener('input', e => updateSocial('Twitter', e.target.value));



            document.getElementById('prop-social-ig').addEventListener('input', e => updateSocial('Instagram', e.target.value));



            document.getElementById('prop-social-li').addEventListener('input', e => updateSocial('LinkedIn', e.target.value));



            document.getElementById('prop-social-yt').addEventListener('input', e => updateSocial('YouTube', e.target.value));



            document.getElementById('prop-social-wa').addEventListener('input', e => updateSocial('WhatsApp', e.target.value));



            document.getElementById('prop-social-tg').addEventListener('input', e => updateSocial('Telegram', e.target.value));



            document.getElementById('prop-social-ws').addEventListener('input', e => updateSocial('Website', e.target.value));



        } else if (type === 'columns2') {



            const tds = contentDiv.querySelectorAll('td');



            propertyFields.innerHTML = `



                <div class="form-group"><label>Column 1 HTML</label><textarea id="prop-col1" rows="4" style="width:100%;border:1px solid var(--border);border-radius:6px;padding:10px;font-family:monospace;">${tds[0] ? tds[0].innerHTML.trim() : ''}</textarea></div>



                <div class="form-group"><label>Column 2 HTML</label><textarea id="prop-col2" rows="4" style="width:100%;border:1px solid var(--border);border-radius:6px;padding:10px;font-family:monospace;">${tds[1] ? tds[1].innerHTML.trim() : ''}</textarea></div>



            `;



            document.getElementById('prop-col1').addEventListener('input', e => { if (tds[0]) tds[0].innerHTML = e.target.value; });



            document.getElementById('prop-col2').addEventListener('input', e => { if (tds[1]) tds[1].innerHTML = e.target.value; });



        } else if (type === 'video') {



            const a = contentDiv.querySelector('a');



            const img = contentDiv.querySelector('img');



            propertyFields.innerHTML = `



                <div class="form-group"><label>Video URL (Link)</label><input type="text" id="prop-video-url" value="${a ? a.getAttribute('href') : '#'}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;"></div>



                <div class="form-group">



                    <label>Thumbnail Image URL</label>



                    <div style="display:flex;gap:8px;margin-bottom:8px;">



                        <button id="btn-upload-thumb" class="btn primary" style="flex:1;padding:8px;font-size:13px;"><i class="fa-solid fa-upload"></i> Upload Thumbnail</button>



                        <input type="file" id="prop-thumb-file" accept="image/*" style="display:none;">



                    </div>



                    <input type="text" id="prop-video-thumb" value="${img ? img.src : ''}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;" placeholder="Or paste image URL..."><button type="button" onclick="openGalleryModal('prop-video-thumb')" class="secondary-btn" style="padding:6px 12px;font-size:12px;margin-top:6px;width:100%;background:#f1f5f9;border:1px solid #cbd5e1;border-radius:6px;color:#475569;cursor:pointer;"><i class="fa-solid fa-images"></i> Browse Gallery</button>



                </div>



            `;



            const fileInput = document.getElementById('prop-thumb-file');



            document.getElementById('btn-upload-thumb').addEventListener('click', () => fileInput.click());



            fileInput.addEventListener('change', async e => {



                const file = e.target.files[0];



                if (!file) return;



                const formData = new FormData();



                formData.append('file', file);



                try {



                    const btn = document.getElementById('btn-upload-thumb');



                    const origText = btn.innerHTML;



                    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Uploading...';



                    btn.disabled = true;



                    const res = await fetch('/api/gallery/upload', { method: 'POST', body: formData, headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') } });



                    const data = await res.json();



                    btn.innerHTML = origText;



                    btn.disabled = false;



                    if (res.ok && data.url) {



                        document.getElementById('prop-video-thumb').value = data.url;



                        if (img) img.src = data.url;



                        showToast('Thumbnail uploaded successfully');



                    } else alert('Upload failed: ' + (data.detail || 'Unknown error'));



                } catch (err) {



                    console.error(err);



                    alert('Error uploading thumbnail');



                    document.getElementById('btn-upload-thumb').disabled = false;



                    document.getElementById('btn-upload-thumb').innerHTML = '<i class="fa-solid fa-upload"></i> Upload Thumbnail';



                }



            });



            document.getElementById('prop-video-url').addEventListener('input', e => { if (a) a.setAttribute('href', e.target.value); });



            document.getElementById('prop-video-thumb').addEventListener('input', e => { if (img) img.src = e.target.value; });



        } else if (type === 'custom_html') {



            propertyFields.innerHTML = `<div class="form-group"><label>Custom HTML</label><textarea id="prop-custom-html" rows="8" style="width:100%;border:1px solid var(--border);border-radius:6px;padding:10px;font-family:monospace;">${contentDiv.innerHTML}</textarea></div>`;



            document.getElementById('prop-custom-html').addEventListener('input', e => {



                contentDiv.innerHTML = e.target.value;



            });



        } else if (type === 'header') {



            const img = contentDiv.querySelector('img');



            propertyFields.innerHTML = `



                <div class="form-group"><label>Logo URL</label><div><input type="text" id="prop-header-img" value="${img ? img.src : ''}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;"><button type="button" onclick="openGalleryModal('prop-header-img')" class="secondary-btn" style="padding:6px 12px;font-size:12px;margin-top:6px;width:100%;background:#f1f5f9;border:1px solid #cbd5e1;border-radius:6px;color:#475569;cursor:pointer;"><i class="fa-solid fa-images"></i> Browse Gallery</button></div></div>



            `;



            document.getElementById('prop-header-img').addEventListener('input', e => { if (img) img.src = e.target.value; });



        } else if (type === 'footer') {



            propertyFields.innerHTML = `<div class="form-group"><label>Footer HTML</label><textarea id="prop-footer-html" rows="8" style="width:100%;border:1px solid var(--border);border-radius:6px;padding:10px;font-family:monospace;">${contentDiv.innerHTML}</textarea></div>`;



            document.getElementById('prop-footer-html').addEventListener('input', e => {



                contentDiv.innerHTML = e.target.value;



            });



        } else if (type === 'product') {



            const img = contentDiv.querySelector('img');



            const h3 = contentDiv.querySelector('h3');



            const p = contentDiv.querySelector('p');



            const a = contentDiv.querySelector('a');



            propertyFields.innerHTML = `



                <div class="form-group"><label>Product Image URL</label><div><input type="text" id="prop-prod-img" value="${img ? img.src : ''}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;"><button type="button" onclick="openGalleryModal('prop-prod-img')" class="secondary-btn" style="padding:6px 12px;font-size:12px;margin-top:6px;width:100%;background:#f1f5f9;border:1px solid #cbd5e1;border-radius:6px;color:#475569;cursor:pointer;"><i class="fa-solid fa-images"></i> Browse Gallery</button></div></div>



                <div class="form-group"><label>Product Name</label><input type="text" id="prop-prod-name" value="${h3 ? h3.innerText : ''}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;"></div>



                <div class="form-group"><label>Description</label><textarea id="prop-prod-desc" rows="3" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;">${p ? p.innerText : ''}</textarea></div>



                <div class="form-group"><label>Button Text</label><input type="text" id="prop-prod-btn-text" value="${a ? a.innerText : ''}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;"></div>



                <div class="form-group"><label>Button URL</label><input type="text" id="prop-prod-btn-url" value="${a ? a.getAttribute('href') : '#'}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;"></div>



            `;



            document.getElementById('prop-prod-img').addEventListener('input', e => { if (img) img.src = e.target.value; });



            document.getElementById('prop-prod-name').addEventListener('input', e => { if (h3) h3.innerText = e.target.value; });



            document.getElementById('prop-prod-desc').addEventListener('input', e => { if (p) p.innerText = e.target.value; });



            document.getElementById('prop-prod-btn-text').addEventListener('input', e => { if (a) a.innerText = e.target.value; });



            document.getElementById('prop-prod-btn-url').addEventListener('input', e => { if (a) a.setAttribute('href', e.target.value); });



        } else if (type === 'image_group') {



            const imgs = contentDiv.querySelectorAll('img');



            propertyFields.innerHTML = `



                <div class="form-group"><label>Image 1 URL</label><div><input type="text" id="prop-img1-src" value="${imgs[0] ? imgs[0].src : ''}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;"><button type="button" onclick="openGalleryModal('prop-img1-src')" class="secondary-btn" style="padding:6px 12px;font-size:12px;margin-top:6px;width:100%;background:#f1f5f9;border:1px solid #cbd5e1;border-radius:6px;color:#475569;cursor:pointer;"><i class="fa-solid fa-images"></i> Browse Gallery</button></div></div>



                <div class="form-group"><label>Image 2 URL</label><div><input type="text" id="prop-img2-src" value="${imgs[1] ? imgs[1].src : ''}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;"><button type="button" onclick="openGalleryModal('prop-img2-src')" class="secondary-btn" style="padding:6px 12px;font-size:12px;margin-top:6px;width:100%;background:#f1f5f9;border:1px solid #cbd5e1;border-radius:6px;color:#475569;cursor:pointer;"><i class="fa-solid fa-images"></i> Browse Gallery</button></div></div>



            `;



            document.getElementById('prop-img1-src').addEventListener('input', e => { if (imgs[0]) imgs[0].src = e.target.value; });



            document.getElementById('prop-img2-src').addEventListener('input', e => { if (imgs[1]) imgs[1].src = e.target.value; });



        }



        



        const topPadding = contentDiv.style.paddingTop.replace('px', '') || '0';



        const bottomPadding = contentDiv.style.paddingBottom.replace('px', '') || '0';



        const spacingDiv = document.createElement('div');



        spacingDiv.innerHTML = `



            <div style="margin-top:24px;padding-top:24px;border-top:1px solid var(--border);">



                <h4 style="font-size:12px;font-weight:700;margin-bottom:12px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;">Spacing Settings</h4>



                <div style="display:flex;gap:12px;">



                    <div class="form-group" style="flex:1;">



                        <label style="font-size:12px;">Top Padding (px)</label>



                        <input type="number" id="prop-pad-top" value="${topPadding}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;">



                    </div>



                    <div class="form-group" style="flex:1;">



                        <label style="font-size:12px;">Bottom Padding (px)</label>



                        <input type="number" id="prop-pad-bottom" value="${bottomPadding}" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:6px;">



                    </div>



                </div>



            </div>



        `;



        propertyFields.appendChild(spacingDiv);



        



        document.getElementById('prop-pad-top').addEventListener('input', e => {



            contentDiv.style.paddingTop = e.target.value ? e.target.value + 'px' : '0px';



        });



        document.getElementById('prop-pad-bottom').addEventListener('input', e => {



            contentDiv.style.paddingBottom = e.target.value ? e.target.value + 'px' : '0px';



        });



    }







    canvasWrapper.addEventListener('click', e => {



        if (e.target === canvas || e.target === canvasWrapper) {



            window.closeMcEdit();



        }



    });







    document.querySelectorAll('.draggable-block').forEach(block => {



        block.addEventListener('click', () => window.addBlockToCanvas(block.getAttribute('data-type')));



    });







    const saveBlockBtn = document.getElementById('save-block-btn');



    if (saveBlockBtn) saveBlockBtn.addEventListener('click', () => {



        if (!selectedBlock) return;



        const type = selectedBlock.getAttribute('data-type');



        const contentDiv = selectedBlock.querySelector('.block-content');



        if (type === 'text') contentDiv.innerHTML = document.getElementById('prop-text').value;



        else if (type === 'image') { const img = contentDiv.querySelector('img'); if (img) img.src = document.getElementById('prop-img-src').value; }



        else if (type === 'button') { const a = contentDiv.querySelector('a'); if (a) { a.innerText = document.getElementById('prop-btn-text').value; a.setAttribute('href', document.getElementById('prop-btn-url').value); } }



        else if (type === 'spacer') { const div = contentDiv.querySelector('div'); if (div) { div.style.height = document.getElementById('prop-spacer-height').value + 'px'; div.style.lineHeight = document.getElementById('prop-spacer-height').value + 'px'; } }



        else if (type === 'columns2') { const tds = contentDiv.querySelectorAll('td'); if (tds[0]) tds[0].innerHTML = document.getElementById('prop-col1').value; if (tds[1]) tds[1].innerHTML = document.getElementById('prop-col2').value; }



        else if (type === 'video') { const a = contentDiv.querySelector('a'); const img = contentDiv.querySelector('img'); if (a) a.setAttribute('href', document.getElementById('prop-video-url').value); if (img) img.src = document.getElementById('prop-video-thumb').value; }



        else if (type === 'socials') {



            const links = contentDiv.querySelectorAll('a');



            const vals = {



                'Facebook': document.getElementById('prop-social-fb').value,



                'Twitter': document.getElementById('prop-social-tw').value,



                'Instagram': document.getElementById('prop-social-ig').value,



                'LinkedIn': document.getElementById('prop-social-li').value,



                'YouTube': document.getElementById('prop-social-yt').value,



                'WhatsApp': document.getElementById('prop-social-wa').value,



                'Telegram': document.getElementById('prop-social-tg').value,



                'Website': document.getElementById('prop-social-ws').value



            };



            links.forEach(a => {



                const img = a.querySelector('img');



                if (img && vals[img.alt] !== undefined) {



                    const val = vals[img.alt];



                    a.setAttribute('href', val || '#');



                    a.style.display = val ? 'inline-block' : 'none';



                }



            });



        }



        else if (type === 'custom_html') { contentDiv.innerHTML = document.getElementById('prop-custom-html').value; }



        else if (type === 'header') { const img = contentDiv.querySelector('img'); if (img) img.src = document.getElementById('prop-header-img').value; }



        else if (type === 'footer') { contentDiv.innerHTML = document.getElementById('prop-footer-html').value; }



        else if (type === 'product') {



            const img = contentDiv.querySelector('img'); const h3 = contentDiv.querySelector('h3'); const p = contentDiv.querySelector('p'); const a = contentDiv.querySelector('a');



            if (img) img.src = document.getElementById('prop-prod-img').value;



            if (h3) h3.innerText = document.getElementById('prop-prod-name').value;



            if (p) p.innerText = document.getElementById('prop-prod-desc').value;



            if (a) { a.innerText = document.getElementById('prop-prod-btn-text').value; a.setAttribute('href', document.getElementById('prop-prod-btn-url').value); }



        }



        else if (type === 'image_group') {



            const imgs = contentDiv.querySelectorAll('img');



            if (imgs[0]) imgs[0].src = document.getElementById('prop-img1-src').value;



            if (imgs[1]) imgs[1].src = document.getElementById('prop-img2-src').value;



        }



        window.saveState();

        window.closeMcEdit();

        showToast('Changes applied');

    });



    const cancelBlockBtn = document.getElementById('cancel-block-btn');

    if (cancelBlockBtn) cancelBlockBtn.addEventListener('click', () => {

        window.closeMcEdit();

    });







    const deleteBlockBtn = document.getElementById('delete-block-btn');



    if (deleteBlockBtn) deleteBlockBtn.addEventListener('click', () => {



        if (!selectedBlock) return;



        selectedBlock.remove();



        window.closeMcEdit();



        if (canvas.querySelectorAll('.email-block').length === 0) canvas.innerHTML = '<div class="canvas-placeholder" style="text-align:center;padding:60px 20px;color:var(--text-muted);border:2px dashed var(--border);border-radius:8px;"><i class="fa-solid fa-layer-group" style="font-size:32px;color:#cbd5e1;margin-bottom:16px;display:block;"></i>Drag blocks here to build your email</div>';



        window.saveState();



    });







    const desktopBtn = document.getElementById('preview-desktop');



    const mobileBtn = document.getElementById('preview-mobile');



    if (desktopBtn) desktopBtn.addEventListener('click', () => { canvas.style.maxWidth = '600px'; });



    if (mobileBtn) mobileBtn.addEventListener('click', () => { canvas.style.maxWidth = '320px'; });







    const bgColor = document.getElementById('global-bg-color');



    if (bgColor) bgColor.addEventListener('input', e => { canvas.style.backgroundColor = e.target.value; });







    // Save Newsletter Draft



    const saveNewsletterDraftBtn = document.getElementById('save-newsletter-draft-btn');



    if (saveNewsletterDraftBtn) saveNewsletterDraftBtn.addEventListener('click', async () => {



        const subject = document.getElementById('campaign-subject').value;



        const blocks = Array.from(canvas.querySelectorAll('.block-content'));



        let rawHTML = '';



        blocks.forEach(b => rawHTML += `<tr><td style="padding:0;">${b.innerHTML}</td></tr>\n`);



        const canvasBg = canvas.style.backgroundColor || '#FFFFFF';



        const finalHTML = `<!DOCTYPE html>



<html>



<head>



    <meta charset="utf-8">



    <meta name="viewport" content="width=device-width, initial-scale=1.0">



</head>



<body style="margin:0;padding:0;background-color:#F6F6F4;font-family:Helvetica,Arial,sans-serif;">



    <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#F6F6F4;">



        <tr>



            <td align="center" style="padding:40px 10px;">



                <table width="100%" max-width="600" border="0" cellspacing="0" cellpadding="0" style="background-color:${canvasBg};border-radius:12px;overflow:hidden;max-width:600px;margin:0 auto;box-shadow:0 4px 24px rgba(0,0,0,0.06);">



                    ${rawHTML}



                </table>



            </td>



        </tr>



    </table>



</body>



</html>`;







        const leadsText = (document.getElementById('newsletter-leads') || {}).value || '';



        const leads = [];



        leadsText.split('\n').map(l => l.trim()).filter(l => l).forEach(line => {



            const parts = line.split(',').map(p => p.trim());



            leads.push({ email: parts[0], name: parts[1] || '', company: parts[2] || '' });



        });







        // Grab Schedule



        const dayMap = {Mon:'vb-sch-day-mon', Tue:'vb-sch-day-tue', Wed:'vb-sch-day-wed', Thu:'vb-sch-day-thu', Fri:'vb-sch-day-fri', Sat:'vb-sch-day-sat', Sun:'vb-sch-day-sun'};



        const selectedDays = Object.entries(dayMap).filter(([day, id]) => document.getElementById(id)?.checked).map(([day]) => day);



        



        const startHour = parseInt((document.getElementById('vb-sch-start-time')?.value || '00:00').split(':')[0]) || 0;



        const endHourVal = parseInt((document.getElementById('vb-sch-end-time')?.value || '00:00').split(':')[0]) || 0;







        const delayMin = parseInt(document.getElementById('vb-sch-delay-min')?.value) || 30;

        const delayMax = parseInt(document.getElementById('vb-sch-delay-max')?.value) || 90;



        const payload = {

            subject: subject || 'Draft Campaign',

            body: finalHTML,

            type: 'newsletter',

            leads: leads,

            is_draft: true,

            campaign_id: window.currentCampaignId || null,

            sending_days: JSON.stringify(selectedDays),

            start_hour: startHour,

            end_hour: endHourVal === 0 ? 24 : endHourVal,

            timezone: document.getElementById('vb-sch-timezone')?.value || 'UTC',

            delay_min: delayMin,

            delay_max: delayMax

        };



        saveNewsletterDraftBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';



        saveNewsletterDraftBtn.disabled = true;



        try {

            if (window.getSelectedSenderIds) {

                payload.selected_sender_ids = window.getSelectedSenderIds('vb-sender-accounts-list');

            }



            const res = await apiCall('/campaigns/send', 'POST', payload);



            if (res.ok) {



                const data = await res.json();



                if (data.campaign_id) window.currentCampaignId = data.campaign_id;



                showToast('Draft saved successfully!', 'success');



            } else { const d = await res.json(); showToast(d.detail || 'Failed to save draft', 'error'); }



        } catch(e) { showToast('Error saving draft', 'error'); }



        saveNewsletterDraftBtn.innerHTML = '<i class="fa-solid fa-save"></i> Save Draft';



        saveNewsletterDraftBtn.disabled = false;



    });







    // Send campaign button



    const sendBtn = document.getElementById('send-btn');



    if (sendBtn) sendBtn.addEventListener('click', async () => {



        const subject = document.getElementById('campaign-subject').value;



        if (!subject) { showToast('Please enter a subject line in the Design tab.', 'error'); return; }



        const blocks = Array.from(canvas.querySelectorAll('.block-content'));



        if (blocks.length === 0) { showToast('Your email is empty! Add blocks first.', 'error'); return; }



        let rawHTML = '';



        blocks.forEach(b => rawHTML += `<tr><td style="padding:0;">${b.innerHTML}</td></tr>\n`);



        const canvasBg = canvas.style.backgroundColor || '#FFFFFF';



        const finalHTML = `<!DOCTYPE html>



<html>



<head>



    <meta charset="utf-8">



    <meta name="viewport" content="width=device-width, initial-scale=1.0">



</head>



<body style="margin:0;padding:0;background-color:#F6F6F4;font-family:Helvetica,Arial,sans-serif;">



    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F6F6F4;padding:20px 0;">



        <tr>



            <td align="center">



                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:${canvasBg};max-width:600px;width:100%;border:1px solid #E0E0DF;">



                    ${rawHTML}



                    <tr>



                        <td align="center" style="background-color:#F6F6F4;padding:20px;font-size:12px;color:#6C6D67;border-top:1px solid #E0E0DF;">



                            <p style="margin:0;">You received this email because you subscribed.</p>



                        </td>



                    </tr>



                </table>



            </td>



        </tr>



    </table>



</body>



</html>`;



        // Launch directly - backend handles account validation

        sendBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';

        sendBtn.disabled = true;



        try {



            const leadsText = document.getElementById('newsletter-leads').value;



            const leads = [];



            leadsText.split('\n').map(l => l.trim()).filter(l => l).forEach(line => {



                const parts = line.split(',').map(p => p.trim());



                leads.push({ email: parts[0], name: parts[1] || '', company: parts[2] || '' });



            });



            const payload = { subject, body: finalHTML, type: 'newsletter', campaign_id: window.currentCampaignId || null };



            



            // Grab Schedule



            const dayMap = {Mon:'vb-sch-day-mon', Tue:'vb-sch-day-tue', Wed:'vb-sch-day-wed', Thu:'vb-sch-day-thu', Fri:'vb-sch-day-fri', Sat:'vb-sch-day-sat', Sun:'vb-sch-day-sun'};



            const selectedDays = Object.entries(dayMap).filter(([day, id]) => document.getElementById(id)?.checked).map(([day]) => day);



            payload.sending_days = JSON.stringify(selectedDays);



            



            const startHour = parseInt((document.getElementById('vb-sch-start-time')?.value || '00:00').split(':')[0]) || 0;



            const endHourVal = parseInt((document.getElementById('vb-sch-end-time')?.value || '00:00').split(':')[0]) || 0;



            payload.start_hour = startHour;



            payload.end_hour = endHourVal === 0 ? 24 : endHourVal;



            payload.timezone = document.getElementById('vb-sch-timezone')?.value || 'UTC';

            payload.track_opens = document.getElementById('vb-track-opens') ? document.getElementById('vb-track-opens').value === '1' : true;

            payload.track_clicks = document.getElementById('vb-track-clicks') ? document.getElementById('vb-track-clicks').value === '1' : true;

            payload.use_unsubscribe = document.getElementById('vb-use-unsubscribe') ? document.getElementById('vb-use-unsubscribe').value === '1' : true;

            payload.max_emails_per_day = document.getElementById('vb-max-emails') ? parseInt(document.getElementById('vb-max-emails').value) || 50 : 50;

            payload.daily_ramp_up = document.getElementById('vb-ramp-up') ? parseInt(document.getElementById('vb-ramp-up').value) || 5 : 5;



            



            if (leads.length === 0) {



                showToast('Please add at least one email in the Audience tab!', 'error');



                sendBtn.innerHTML = '<i class="fa-solid fa-rocket"></i> Launch Newsletter';



                sendBtn.disabled = false;



                return;



            }



            payload.leads = leads;

            if (window.getSelectedSenderIds) {

                payload.selected_sender_ids = window.getSelectedSenderIds('vb-sender-accounts-list');

            }



            const res = await apiCall('/campaigns/send', 'POST', payload);



            if (res.ok) {



                showToast('Campaign sent successfully!', 'success');



                canvas.innerHTML = '<div class="canvas-placeholder">Drag blocks here to build your email</div>';



                var leadsEl = document.getElementById('newsletter-leads');



                if (leadsEl) leadsEl.value = '';



                // Redirect to Newsletters list



                window.navTo('campaigns-list');



            } else {



                const data = await res.json();



                showToast(data.detail || 'Failed to send', 'error');



            }



        } catch(e) { showToast('Error sending campaign', 'error'); }



        sendBtn.innerHTML = '<i class="fa-solid fa-rocket"></i> Send Now';



        sendBtn.disabled = false;



    });







    // ---- TEMPLATE GALLERY ----



    function loadTemplate(templateId) {



        const tmpl = window.EmailTemplates ? window.EmailTemplates.find(t => t.id === templateId) : null;



        if (!tmpl) { showToast('Template not found', 'error'); return; }



        if (canvas.querySelectorAll('.email-block').length > 0) {



            if (!confirm('This will replace your current design. Continue?')) return;



        }



        canvas.innerHTML = '';



        const subjEl = document.getElementById('campaign-subject');



        if (subjEl) subjEl.value = tmpl.subject || '';



        tmpl.blocks.forEach(b => window.addBlockToCanvas(b.type, null, b.content));



        showToast('✨ Template loaded: ' + tmpl.name, 'success');



        // Switch to design area



        window.switchMcTab('blocks');



    }







    const container = document.getElementById('template-accordion-container');

    if (container && window.EmailTemplates) {

        container.innerHTML = '';

        const categories = {};

        window.EmailTemplates.forEach(t => {

            const cat = t.category || 'Other';

            if (!categories[cat]) categories[cat] = [];

            categories[cat].push(t);

        });

        

        for (const cat in categories) {

            const box = document.createElement('div');

            box.style.border = '1px solid var(--border)';

            box.style.borderRadius = '8px';

            box.style.overflow = 'hidden';

            box.style.background = '#fff';

            box.style.boxShadow = '0 1px 2px rgba(0,0,0,0.05)';

            

            const header = document.createElement('div');

            header.style.padding = '12px 16px';

            header.style.background = '#f8fafc';

            header.style.cursor = 'pointer';

            header.style.fontWeight = '600';

            header.style.fontSize = '13px';

            header.style.color = '#334155';

            header.style.display = 'flex';

            header.style.justifyContent = 'space-between';

            header.style.alignItems = 'center';

            header.innerHTML = `<span>${cat} <span style="font-size:11px;color:#94a3b8;font-weight:400;margin-left:4px;">(${categories[cat].length})</span></span><i class="fa-solid fa-chevron-down" style="font-size:10px;transition:transform 0.2s;"></i>`;

            

            const content = document.createElement('div');

            content.style.display = 'none';

            content.style.flexDirection = 'column';

            content.style.maxHeight = '280px';

            content.style.overflowY = 'auto';

            content.style.borderTop = '1px solid var(--border)';

            

            header.addEventListener('click', () => {

                const isOpen = content.style.display === 'flex';

                // Close all others

                Array.from(container.children).forEach(c => {

                    c.children[1].style.display = 'none';

                    c.children[0].querySelector('i').style.transform = 'rotate(0deg)';

                    c.children[0].style.background = '#f8fafc';

                });

                

                if (!isOpen) {

                    content.style.display = 'flex';

                    header.querySelector('i').style.transform = 'rotate(180deg)';

                    header.style.background = '#e2e8f0';

                }

            });

            

            categories[cat].forEach(t => {

                const item = document.createElement('div');

                item.style.padding = '10px 16px';

                item.style.fontSize = '13px';

                item.style.color = '#475569';

                item.style.cursor = 'pointer';

                item.style.borderBottom = '1px solid #f1f5f9';

                item.style.transition = 'background 0.2s, color 0.2s';

                item.innerHTML = `<i class="fa-regular fa-file-lines" style="margin-right:8px;color:#94a3b8;"></i> ${t.name}`;

                

                item.addEventListener('mouseenter', () => {

                    item.style.background = '#f1f5f9';

                    item.style.color = 'var(--p)';

                });

                item.addEventListener('mouseleave', () => {

                    item.style.background = 'transparent';

                    item.style.color = '#475569';

                });

                

                item.addEventListener('click', () => {

                    loadTemplate(t.id);

                });

                content.appendChild(item);

            });

            

            box.appendChild(header);

            box.appendChild(content);

            container.appendChild(box);

        }

    }

}











// ============================================================



// CAMPAIGN TABS



// ============================================================



function setupCampaignTabs() {



    document.querySelectorAll('.tab-btn').forEach(btn => {



        btn.addEventListener('click', () => {



            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));



            btn.classList.add('active');



            document.querySelectorAll('.tab-content').forEach(c => { c.style.display = 'none'; c.classList.remove('active'); });



            const target = document.getElementById(btn.getAttribute('data-tab'));



            if (target) { target.style.display = 'block'; target.classList.add('active'); }



        });



    });



}







// ============================================================



// SEQUENCE BUILDER



// ============================================================



function setupSequenceBuilder() {



    let steps = [{ step: 1, wait: 0, subject: '', body: '', is_ab: false, subject_b: '', body_b: '' }];



    let currentStep = 1;



    



    // Expose steps globally so editCampaign can update them



    window._coldMailSteps = steps;



    window._coldMailCurrentStep = currentStep;







    window.toggleInstAB = function() {



        const s = steps.find(x => x.step === currentStep);



        if (!s) return;



        s.is_ab = !s.is_ab;



        document.getElementById('inst-ab-section').style.display = s.is_ab ? 'block' : 'none';



        const abToggleBtn = document.getElementById('ab-toggle-btn');



        if (abToggleBtn) {



            abToggleBtn.style.color = s.is_ab ? 'var(--p)' : 'var(--text-muted)';



            abToggleBtn.style.borderColor = s.is_ab ? 'var(--p)' : 'var(--border)';



        }



        renderSteps();



    };







    function renderSteps() {



        const bar = document.getElementById('inst-steps-bar');



        if (!bar) return;



        bar.innerHTML = '';



        steps.forEach(s => {



            const btn = document.createElement('div');



            btn.className = 'btn';



            btn.innerHTML = `<div style="display:flex;flex-direction:column;align-items:flex-start;gap:2px;">



                <span style="font-weight:700;">Step ${s.step} ${s.is_ab ? '<i class="fa-solid fa-flask" style="font-size:10px;margin-left:4px;color:var(--p);"></i>' : ''}</span>



                <span style="font-size:12px;opacity:0.8;">Wait: ${s.wait} day(s)</span>



            </div>`;



            btn.style.cssText = 'padding:12px 16px;font-size:14px;width:100%;text-align:left;justify-content:flex-start;background:' + (s.step === currentStep ? 'var(--surface-1)' : 'transparent') + ';color:' + (s.step === currentStep ? 'var(--text)' : 'var(--text-muted)') + ';border:1px solid ' + (s.step === currentStep ? 'var(--border)' : 'transparent') + ';cursor:pointer;border-radius:8px;';



            if (s.step === currentStep) btn.style.boxShadow = 'var(--shadow-sm)';



            btn.onclick = () => { saveStep(); currentStep = s.step; loadStep(); renderSteps(); };



            bar.appendChild(btn);



        });



    }







    function saveStep() {



        const s = steps.find(x => x.step === currentStep);



        if (!s) return;



        s.subject = (document.getElementById('inst-subject') || {}).value || '';



        s.body = (document.getElementById('inst-body') || {}).value || '';



        s.wait = parseInt((document.getElementById('inst-wait') || {}).value) || 0;



        s.subject_b = (document.getElementById('inst-subject-b') || {}).value || '';



        s.body_b = (document.getElementById('inst-body-b') || {}).value || '';



    }







    function loadStep() {



        const s = steps.find(x => x.step === currentStep);



        if (!s) return;



        



        const titleEl = document.getElementById('inst-step-title');



        if (titleEl) titleEl.textContent = 'Step ' + s.step;



        



        const subj = document.getElementById('inst-subject');



        const body = document.getElementById('inst-body');



        const wait = document.getElementById('inst-wait');



        const subjB = document.getElementById('inst-subject-b');



        const bodyB = document.getElementById('inst-body-b');



        



        if (subj) subj.value = s.subject;



        if (body) body.value = s.body;



        if (wait) wait.value = s.wait;



        if (subjB) subjB.value = s.subject_b || '';



        if (bodyB) bodyB.value = s.body_b || '';



        



        document.getElementById('inst-ab-section').style.display = s.is_ab ? 'block' : 'none';



        const abToggleBtn = document.getElementById('ab-toggle-btn');



        if (abToggleBtn) {



            abToggleBtn.style.color = s.is_ab ? 'var(--p)' : 'var(--text-muted)';



            abToggleBtn.style.borderColor = s.is_ab ? 'var(--p)' : 'var(--border)';



        }



    }







    const addStepBtn = document.getElementById('inst-add-step-btn');



    if (addStepBtn) addStepBtn.addEventListener('click', () => {



        saveStep();



        steps.push({ step: steps.length + 1, wait: 2, subject: '', body: '', is_ab: false, subject_b: '', body_b: '' });



        currentStep = steps.length;



        loadStep();



        renderSteps();



    });







    // Expose renderSteps and loadStep globally for editCampaign



    window._coldMailRenderSteps = renderSteps;



    window._coldMailLoadStep = loadStep;







    const saveStepBtn = document.getElementById('inst-save-step-btn');



    if (saveStepBtn) saveStepBtn.addEventListener('click', () => { saveStep(); renderSteps(); showToast('Step saved'); });







    const sendSeqBtn = document.getElementById('inst-send-seq-btn');



    if (sendSeqBtn) sendSeqBtn.addEventListener('click', async () => {



        saveStep();



        renderSteps();



        const emptySteps = steps.filter(s => !s.subject || !s.body.trim());



        if (emptySteps.length > 0) { showToast(`Step ${emptySteps[0].step} is incomplete`, 'error'); return; }







        const leadsText = (document.getElementById('seq-leads') || {}).value || '';



        const leads = [];



        leadsText.split('\n').map(l => l.trim()).filter(l => l).forEach(line => {



            const parts = line.split(',').map(p => p.trim());



            leads.push({ email: parts[0], name: parts[1] || '', company: parts[2] || '' });



        });







        if (leads.length === 0) {



            showToast('Please add at least one lead in the Campaign Audience', 'error');



            return;



        }







        // Convert sequence steps to a single campaign with A/B variants for MVP



        const s1 = steps[0];



        let delayMin = parseInt((document.getElementById('sch-delay-min') || {}).value); if(isNaN(delayMin)) delayMin = 30;



        let delayMax = parseInt((document.getElementById('sch-delay-max') || {}).value); if(isNaN(delayMax)) delayMax = 90;



        const payload = {



            subject: s1.subject,



            body: steps.map(s => '<div>' + s.body + '</div>').join('<hr>'),



            type: 'cold_mail',



            leads: leads,



            is_ab_test: !!s1.is_ab,



            subject_b: s1.subject_b || '',



            body_b: steps.map(s => '<div>' + (s.is_ab ? (s.body_b || s.body) : s.body) + '</div>').join('<hr>'),



            steps_json: JSON.stringify(steps),



            delay_min: delayMin,



            delay_max: delayMax,



            campaign_id: window.currentCampaignId || null



        };



        



        // Grab Schedule from the Schedule Tab if it exists



        const dayMap = {Mon:'sch-day-mon', Tue:'sch-day-tue', Wed:'sch-day-wed', Thu:'sch-day-thu', Fri:'sch-day-fri', Sat:'sch-day-sat', Sun:'sch-day-sun'};



        const selectedDays = Object.entries(dayMap).filter(([day, id]) => document.getElementById(id)?.checked).map(([day]) => day);



        payload.sending_days = JSON.stringify(selectedDays);



        



        const startHour = parseInt((document.getElementById('sch-start-time')?.value || '00:00').split(':')[0], 10) || 0;



        const endHourVal = parseInt((document.getElementById('sch-end-time')?.value || '00:00').split(':')[0], 10) || 0;



        payload.start_hour = startHour;



        payload.end_hour = endHourVal === 0 ? 24 : endHourVal;



        payload.timezone = document.getElementById('sch-timezone')?.value || 'UTC';

        payload.track_opens = document.getElementById('cold-track-opens') ? document.getElementById('cold-track-opens').value === '1' : true;

        payload.track_clicks = document.getElementById('cold-track-clicks') ? document.getElementById('cold-track-clicks').value === '1' : true;

        payload.use_unsubscribe = document.getElementById('cold-use-unsubscribe') ? document.getElementById('cold-use-unsubscribe').value === '1' : true;

          payload.max_emails_per_day = document.getElementById('cold-max-emails') ? parseInt(document.getElementById('cold-max-emails').value) || 50 : 50;

          payload.daily_ramp_up = document.getElementById('cold-ramp-up') ? parseInt(document.getElementById('cold-ramp-up').value) || 0 : 0;



        















        // Launch directly - backend handles account validation

        sendSeqBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Launching...';

        sendSeqBtn.disabled = true;



        try {

            if (window.getSelectedSenderIds) {

                payload.selected_sender_ids = window.getSelectedSenderIds('cold-sender-accounts-list');

            }

            const res = await apiCall('/campaigns/send', 'POST', payload);

            if (res.ok) {

                showToast('Campaign launched successfully!', 'success');

                // Refresh campaigns list and redirect

                apiCall('/campaigns').then(r => r.json()).then(c => { 

                    window.lastFetchedCampaigns = c; 

                    window.navTo('cold-mail-list');

                }).catch(() => {

                    window.navTo('cold-mail-list');

                });

            } else {

                const d = await res.json();

                showToast(d.detail || 'Failed to launch', 'error');

            }

        } catch(e) { showToast('Error launching campaign', 'error'); }



        sendSeqBtn.innerHTML = '<i class="fa-solid fa-rocket"></i> Launch Campaign';



        sendSeqBtn.disabled = false;



    });







    const saveDraftBtn = document.getElementById('inst-save-draft-btn');



    if (saveDraftBtn) saveDraftBtn.addEventListener('click', async () => {



        saveStep();



        renderSteps();



        const emptySteps = steps.filter(s => !s.subject || !s.body.trim());



        if (emptySteps.length > 0) { showToast(`Step ${emptySteps[0].step} is incomplete`, 'error'); return; }







        const leadsText = (document.getElementById('seq-leads') || {}).value || '';



        const leads = [];



        leadsText.split('\n').map(l => l.trim()).filter(l => l).forEach(line => {



            const parts = line.split(',').map(p => p.trim());



            leads.push({ email: parts[0], name: parts[1] || '', company: parts[2] || '' });



        });







        const s1 = steps[0];



        let delayMin = parseInt((document.getElementById('sch-delay-min') || {}).value); if(isNaN(delayMin)) delayMin = 30;



        let delayMax = parseInt((document.getElementById('sch-delay-max') || {}).value); if(isNaN(delayMax)) delayMax = 90;



        const payload = {



            subject: s1.subject,



            body: steps.map(s => '<div>' + s.body + '</div>').join('<hr>'),



            type: 'cold_mail',



            leads: leads,



            is_ab_test: !!s1.is_ab,



            subject_b: s1.subject_b || '',



            body_b: steps.map(s => '<div>' + (s.is_ab ? (s.body_b || s.body) : s.body) + '</div>').join('<hr>'),



            steps_json: JSON.stringify(steps),



            delay_min: delayMin,



            delay_max: delayMax,



            is_draft: true,



            campaign_id: window.currentCampaignId || null



        };







        // BUG FIX: Include schedule in Save Draft so it doesn't get overwritten with null



        const dayMap = {Mon:'sch-day-mon', Tue:'sch-day-tue', Wed:'sch-day-wed', Thu:'sch-day-thu', Fri:'sch-day-fri', Sat:'sch-day-sat', Sun:'sch-day-sun'};



        const selectedDays = Object.entries(dayMap).filter(([day, id]) => document.getElementById(id)?.checked).map(([day]) => day);



        payload.sending_days = JSON.stringify(selectedDays);



        const startHour = parseInt((document.getElementById('sch-start-time')?.value || '00:00').split(':')[0], 10) || 0;



        const endHourVal = parseInt((document.getElementById('sch-end-time')?.value || '00:00').split(':')[0], 10) || 0;



        payload.start_hour = startHour;



        payload.end_hour = endHourVal === 0 ? 24 : endHourVal;



        payload.timezone = document.getElementById('sch-timezone')?.value || 'UTC';

        payload.track_opens = document.getElementById('cold-track-opens') ? document.getElementById('cold-track-opens').value === '1' : true;

        payload.track_clicks = document.getElementById('cold-track-clicks') ? document.getElementById('cold-track-clicks').value === '1' : true;

        payload.use_unsubscribe = document.getElementById('cold-use-unsubscribe') ? document.getElementById('cold-use-unsubscribe').value === '1' : true;

          payload.max_emails_per_day = document.getElementById('cold-max-emails') ? parseInt(document.getElementById('cold-max-emails').value) || 50 : 50;

          payload.daily_ramp_up = document.getElementById('cold-ramp-up') ? parseInt(document.getElementById('cold-ramp-up').value) || 0 : 0;



        



        saveDraftBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';



        saveDraftBtn.disabled = true;



        try {

            if (window.getSelectedSenderIds) {

                payload.selected_sender_ids = window.getSelectedSenderIds('cold-sender-accounts-list');

            }



            const res = await apiCall('/campaigns/send', 'POST', payload);



            if (res.ok) showToast('Draft saved successfully!', 'success');



            else { const d = await res.json(); showToast(d.detail || 'Failed to save draft', 'error'); }



        } catch(e) { showToast('Error saving draft', 'error'); }



        saveDraftBtn.innerHTML = '<i class="fa-solid fa-save"></i> Save Draft';



        saveDraftBtn.disabled = false;



    });







    loadStep();



    renderSteps();



}







// ============================================================



// A/B TEST



// ============================================================



function setupABTest() {



    const sendBtn = document.getElementById('ab-send-btn');



    if (!sendBtn) return;



    sendBtn.addEventListener('click', async () => {



        const subjectA = (document.getElementById('ab-subject-a') || {}).value;



        const bodyA = (document.getElementById('ab-body-a') || {}).value;



        const subjectB = (document.getElementById('ab-subject-b') || {}).value;



        const bodyB = (document.getElementById('ab-body-b') || {}).value;



        const statusDiv = document.getElementById('ab-status');



        if (!subjectA || !bodyA || !subjectB || !bodyB) {



            if (statusDiv) { statusDiv.textContent = 'Please fill all A/B fields.'; statusDiv.className = 'alert error'; statusDiv.style.display = 'block'; }



            return;



        }



        sendBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Running...';



        sendBtn.disabled = true;



        try {



        const delayMin = parseInt(document.getElementById('vb-sch-delay-min')?.value) || 30;



        const delayMax = parseInt(document.getElementById('vb-sch-delay-max')?.value) || 90;



        const payload = { 



            subject: subjectA, 



            body: bodyA, 



            subject_b: subjectB, 



            body_b: bodyB, 



            is_ab_test: true, 



            delay_min: delayMin, 



            delay_max: delayMax, 



            leads: window.campaignLeads || [],



            campaign_id: window.currentCampaignId || null



        };



        const res = await apiCall('/campaigns/send', 'POST', payload);



            if (statusDiv) {



                statusDiv.textContent = res.ok ? 'A/B test launched!' : 'Failed to launch';



                statusDiv.className = res.ok ? 'alert success' : 'alert error';



                statusDiv.style.display = 'block';



            }



        } catch(e) { showToast('Error', 'error'); }



        sendBtn.innerHTML = '<i class="fa-solid fa-flask"></i> Run A/B Test';



        sendBtn.disabled = false;



    });



}







// ============================================================



// ADMIN



// ============================================================



function updateAdminBadge(count) {



    var navAdmin = document.getElementById('nav-admin');



    if (!navAdmin) return;



    var existing = navAdmin.querySelector('.admin-badge');



    if (existing) existing.remove();



    if (count > 0) {



        var badge = document.createElement('span');



        badge.className = 'admin-badge';



        badge.textContent = count;



        badge.style.cssText = 'background:#ef4444;color:#fff;border-radius:50%;width:18px;height:18px;display:inline-flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;margin-left:auto;animation:pulse 1.5s infinite;';



        navAdmin.appendChild(badge);



    }



}







async function checkPendingApprovals() {



    try {



        var isAdmin = localStorage.getItem('is_admin') === 'true';



        if (!isAdmin) return;



        var res = await apiCall('/admin/users');



        if (!res.ok) return;



        var users = await res.json();



        var pending = users.filter(function(u) { return !u.is_approved; }).length;



        updateAdminBadge(pending);



    } catch(e) {}



}







window.SUPPORT = {
    showCreateModal: function() {
        var m = document.getElementById('support-create-modal');
        if (m) m.style.display = 'flex';
    },
    createTicket: async function(btn) {
        var subject = document.getElementById('support-subject');
        var message = document.getElementById('support-message');
        if (!subject.value.trim() || !message.value.trim()) {
            alert('Please enter a subject and message.');
            return;
        }
        var origText = btn.innerHTML;
        btn.innerHTML = 'Submitting...';
        btn.disabled = true;
        
        try {
            let res = await fetch('/api/support/tickets', {
                method: 'POST',
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token'), 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    subject: subject.value.trim(),
                    message: message.value.trim()
                })
            });
            if (res.ok) {
                document.getElementById('support-create-modal').style.display = 'none';
                subject.value = '';
                message.value = '';
                SUPPORT.loadSupportTickets();
                alert('Ticket created successfully.');
            } else {
                let err = await res.json();
                alert('Failed to create ticket: ' + (err.detail || 'Unknown error'));
            }
        } catch (e) {
            console.error(e);
            alert('An error occurred.');
        } finally {
            btn.innerHTML = origText;
            btn.disabled = false;
        }
    },
    
    loadSupportTickets: async function() {
        try {
            let res = await fetch('/api/support/tickets', { headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') } });
            if (res.ok) {
                let data = await res.json();
                let tbody = document.getElementById('user-tickets-body');
                let userHtml = '';
                
                data.tickets.forEach(t => {
                    let statusColor = (t.status.toLowerCase() === 'open' || t.status.toLowerCase() === 'user reply') ? '#3b82f6' : (t.status.toLowerCase() === 'admin reply' ? '#10b981' : '#64748b');
                    let dt = new Date(t.updated_at).toLocaleString();
                    
                    userHtml += `<tr>
                        <td>${t.subject}</td>
                        <td><span style="color:${statusColor}; font-weight:600; text-transform:capitalize;">${t.status}</span></td>
                        <td>${dt}</td>
                        <td><button class="btn" onclick="SUPPORT.viewTicket('${t.id}')">View</button></td>
                    </tr>`;
                });
                if (tbody) tbody.innerHTML = userHtml || '<tr><td colspan="4">No tickets found.</td></tr>';
            }
        } catch (e) {
            console.error('Failed to load user tickets', e);
        }
    },
    loadAdminTickets: async function() {
        try {
            let res = await fetch('/api/admin/tickets', { headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') } });
            if (res.ok) {
                let data = await res.json();
                let adminBody = document.getElementById('admin-all-tickets-body');
                let adminHtml = '';
                
                data.tickets.forEach(t => {
                    let statusColor = (t.status.toLowerCase() === 'open' || t.status.toLowerCase() === 'user reply') ? '#3b82f6' : (t.status.toLowerCase() === 'admin reply' ? '#10b981' : '#64748b');
                    let dt = new Date(t.updated_at).toLocaleString();
                    
                    adminHtml += `<tr>
                        <td>${t.user_email}</td>
                        <td>${t.subject}</td>
                        <td><span style="color:${statusColor}; font-weight:600; text-transform:capitalize;">${t.status}</span></td>
                        <td><button class="btn" onclick="SUPPORT.viewTicket('${t.id}')">View & Reply</button></td>
                    </tr>`;
                });
                if (adminBody) adminBody.innerHTML = adminHtml || '<tr><td colspan="4">No tickets found.</td></tr>';
            }
        } catch (e) {
            console.error('Failed to load admin tickets', e);
        }
    },
viewTicket: async function(ticketId) {
        try {
            let res = await fetch('/api/support/tickets/' + ticketId, { headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') } });
            if (res.ok) {
                let data = await res.json();
                let currentUser = JSON.parse(localStorage.getItem('user') || '{}');
                let isAdmin = currentUser.is_admin === true;
                document.getElementById('support-active-ticket-id').value = ticketId;
                let statusColor = data.status === 'resolved' ? '#10b981' : (data.status === 'Admin Reply' ? '#10b981' : '#3b82f6');
                document.getElementById('support-view-title').innerHTML = '<i class="fa-solid fa-comments"></i> ' + data.subject + ' <span style="font-size:12px;color:' + statusColor + ';margin-left:8px;text-transform:capitalize;font-weight:600;">(' + data.status + ')</span>';
                
                // Show/hide admin action buttons
                let adminActions = document.getElementById('support-admin-actions');
                if (adminActions) {
                    if (isAdmin) {
                        adminActions.style.display = 'flex';
                        let resolveBtn = document.getElementById('support-resolve-btn');
                        if (resolveBtn) {
                            if (data.status === 'resolved') {
                                resolveBtn.innerHTML = '<i class="fa-solid fa-check-circle"></i> Resolved';
                                resolveBtn.style.background = '#10b981';
                                resolveBtn.disabled = true;
                            } else {
                                resolveBtn.innerHTML = '<i class="fa-solid fa-check-circle"></i> Resolve';
                                resolveBtn.style.background = '#3b82f6';
                                resolveBtn.disabled = false;
                            }
                        }
                    } else {
                        adminActions.style.display = 'none';
                    }
                }

                let chatContainer = document.getElementById('support-replies-container');
                let chatHtml = '';
                
                data.messages.forEach(m => {
                    let bg = m.is_admin ? '#e0e7ff' : '#fff';
                    let align = m.is_admin ? 'flex-start' : 'flex-end';
                    let name = m.is_admin ? 'Support Team' : 'You';
                    
                    chatHtml += `
                    <div style="display:flex; flex-direction:column; align-items:${align};">
                        <div style="font-size:11px; color:#64748b; margin-bottom:4px;">${name} &bull; ${new Date(m.created_at).toLocaleString()}</div>
                        <div style="background:${bg}; padding:12px 16px; border-radius:12px; box-shadow:0 1px 2px rgba(0,0,0,0.05); max-width:80%; font-size:14px; color:#1e293b; white-space:pre-wrap;">${m.message}</div>
                    </div>`;
                });
                
                chatContainer.innerHTML = chatHtml;
                document.getElementById('support-view-modal').style.display = 'flex';
                // scroll to bottom
                setTimeout(() => { chatContainer.scrollTop = chatContainer.scrollHeight; }, 100);
            } else {
                alert('Failed to load ticket details.');
            }
        } catch (e) {
            console.error('Error viewing ticket', e);
            alert('An error occurred loading the ticket.');
        }
    },
    replyToTicket: async function(btn) {
        var message = document.getElementById('support-reply-message');
        var ticketId = document.getElementById('support-active-ticket-id').value;
        if (!message.value.trim() || !ticketId) {
            alert('Please enter a reply.');
            return;
        }
        var origText = btn.innerHTML;
        btn.innerHTML = 'Sending...';
        btn.disabled = true;
        
        try {
            let res = await fetch('/api/support/tickets/' + ticketId + '/reply', {
                method: 'POST',
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token'), 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message.value.trim() })
            });
            if (res.ok) {
                message.value = '';
                // Reload ticket chat and ticket list
                SUPPORT.viewTicket(ticketId);
                SUPPORT.loadSupportTickets();
            } else {
                alert('Failed to send reply.');
            }
        } catch(e) {
            console.error(e);
            alert('An error occurred.');
        } finally {
            btn.innerHTML = origText;
            btn.disabled = false;
        }
    },
    resolveTicket: async function() {
        let ticketId = document.getElementById('support-active-ticket-id').value;
        if (!ticketId) return;
        try {
            let res = await fetch('/api/admin/tickets/' + ticketId + '/status', {
                method: 'PUT',
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token'), 'Content-Type': 'application/json' },
                body: JSON.stringify({ status: 'resolved' })
            });
            if (res.ok) {
                SUPPORT.viewTicket(ticketId);
                SUPPORT.loadAdminTickets();
                SUPPORT.checkUnreadTickets();
            } else { alert('Failed to resolve ticket.'); }
        } catch(e) { alert('Error resolving ticket.'); }
    },
    deleteTicket: async function() {
        let ticketId = document.getElementById('support-active-ticket-id').value;
        if (!ticketId) return;
        if (!confirm('Are you sure you want to delete this ticket? This cannot be undone.')) return;
        try {
            let res = await fetch('/api/admin/tickets/' + ticketId, {
                method: 'DELETE',
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
            });
            if (res.ok) {
                document.getElementById('support-view-modal').style.display = 'none';
                SUPPORT.loadAdminTickets();
                SUPPORT.checkUnreadTickets();
            } else { alert('Failed to delete ticket.'); }
        } catch(e) { alert('Error deleting ticket.'); }
    },
    checkUnreadTickets: async function() {
        try {
            let currentUser = JSON.parse(localStorage.getItem('user') || '{}');
            if (!currentUser.is_admin) return;
            let res = await fetch('/api/admin/tickets/unread-count', {
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
            });
            if (res.ok) {
                let data = await res.json();
                let badge = document.getElementById('support-unread-badge');
                if (badge) {
                    if (data.unread > 0) {
                        badge.textContent = data.unread;
                        badge.style.display = 'inline-flex';
                    } else {
                        badge.style.display = 'none';
                    }
                }
            }
        } catch(e) { /* silent */ }
    },
    switchAdminTab: function(tab) {
        document.querySelectorAll('.admin-tab').forEach(t => {
            t.classList.remove('active');
            t.style.color = 'var(--text-muted)';
            t.style.borderBottomColor = 'transparent';
        });
        document.querySelectorAll('.admin-section').forEach(s => s.style.display = 'none');
        var btn = document.getElementById('tab-btn-' + tab);
        if(btn) {
            btn.classList.add('active');
            btn.style.color = 'var(--primary)';
            btn.style.borderBottomColor = 'var(--primary)';
        }
        var sec = document.getElementById('admin-section-' + tab);
        if(sec) {
            sec.style.display = 'block';
            if (tab === 'tickets') SUPPORT.loadAdminTickets();
        }
    }
};

function setupAdmin() {



    // loadAdminUsers is called when admin tab is selected



}







async function loadUnsubscribes() {



    try {



        const res = await apiCall('/unsubscribes');



        if (!res.ok) return;



        const data = await res.json();



        const tbody = document.getElementById('unsubscribes-table-body');



        if (!tbody) return;



        tbody.innerHTML = '';



        if (data.length === 0) {



            tbody.innerHTML = `<tr><td colspan="2" style="padding:20px; text-align:center; color:var(--text-muted);">No unsubscribes yet</td></tr>`;



            return;



        }



        data.forEach(item => {



            const tr = document.createElement('tr');



            tr.innerHTML = `



                <td style="padding:16px 24px; font-weight:600; color:var(--text);">${escapeHtml(item.email)}</td>



                <td style="padding:16px 24px; color:var(--text-muted); font-size:13px;">${new Date(item.unsubscribed_at).toLocaleString()}</td>



            `;



            tbody.appendChild(tr);



        });



    } catch(e) { console.error(e); }



}







async function loadReplies() {



    try {



        const res = await apiCall('/replies');  // BUG-10 FIX: was '/api/replies' causing double /api prefix



        if (!res.ok) return;



        const data = await res.json();



        const tbody = document.getElementById('replies-table-body');



        if (!tbody) return;



        tbody.innerHTML = '';



        if (data.length === 0) {



            tbody.innerHTML = `<tr><td colspan="4" style="padding:20px; text-align:center; color:var(--text-muted);">No replies yet</td></tr>`;



            return;



        }



        data.forEach(item => {



            const tr = document.createElement('tr');



            let color = '#64748b';



            if (item.sentiment === 'Interested') color = '#059669';



            else if (item.sentiment === 'Not Interested') color = '#dc2626';



            else if (item.sentiment === 'Meeting Booked') color = '#2563eb';



            



            tr.innerHTML = `



                <td style="padding:16px 24px; font-weight:600; color:var(--text);">${item.sender_email}</td>



                <td style="padding:16px 24px; color:var(--text-muted);">${item.subject || '(No Subject)'}</td>



                <td style="padding:16px 24px;"><span style="background:${color}20; color:${color}; padding:4px 12px; border-radius:12px; font-size:12px; font-weight:600;">${item.sentiment}</span></td>



                <td style="padding:16px 24px; color:var(--text-muted); font-size:13px;">${new Date(item.received_at).toLocaleString()}</td>

                

                <td style="padding:16px 24px; display: flex; gap: 8px; align-items: center;">

                    <button class="btn secondary" style="padding:6px 12px; font-size:12px;" onclick="openReplyModal(window._replyData['${item.id}'])"><i class="fa-solid fa-eye"></i> View & Reply</button>

                    <button onclick="deleteReply('${item.id}', this)" class="btn" style="padding:6px 12px; font-size:12px; color:#ef4444; border-color:#fecaca; background: transparent;"><i class="fa-solid fa-trash"></i></button>

                </td>



            `;



            window._replyData = window._replyData || {};

            window._replyData[item.id] = item;



            tbody.appendChild(tr);



        });



    } catch(e) { console.error(e); }



}



async function deleteReply(replyId, btn) {

    if (!confirm("Are you sure you want to delete this reply?")) return;

    const oldHtml = btn.innerHTML;

    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

    btn.disabled = true;

    try {

        const res = await apiCall(`/replies/${replyId}`, 'DELETE');

        if (res.ok) {

            showToast("Reply deleted successfully", "success");

            loadReplies();

        } else {

            const data = await res.json();

            showToast(data.detail || "Failed to delete reply", "error");

            btn.innerHTML = oldHtml;

            btn.disabled = false;

        }

    } catch (e) {

        console.error(e);

        showToast("Error deleting reply", "error");

        btn.innerHTML = oldHtml;

        btn.disabled = false;

    }

}



function openReplyModal(item) {

    document.getElementById('active-reply-id').value = item.id;

    document.getElementById('client-original-message').innerText = item.body || '(No message body)';

    document.getElementById('ai-reply-draft').value = '';

    document.getElementById('reply-modal').style.display = 'flex';

}



async function generateAiReplyDraft(btn) {

    const replyId = document.getElementById('active-reply-id').value;

    const oldHtml = btn.innerHTML;

    

    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating...';

    btn.disabled = true;

    

    try {

        const res = await apiCall(`/replies/${replyId}/draft`, 'POST');

        const data = await res.json();

        

        if (res.ok && data.draft) {

            document.getElementById('ai-reply-draft').value = data.draft;

        } else {

            showToast('Failed to generate draft: ' + (data.detail || ''), 'error');

        }

    } catch(e) {

        showToast('Network error generating draft.', 'error');

    } finally {

        btn.innerHTML = oldHtml;

        btn.disabled = false;

    }

}



async function sendAiReply(btn) {

    const replyId = document.getElementById('active-reply-id').value;

    const content = document.getElementById('ai-reply-draft').value.trim();

    

    if (!content) {

        showToast('Reply draft cannot be empty.', 'error');

        return;

    }

    

    const oldHtml = btn.innerHTML;

    

    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';

    btn.disabled = true;

    

    try {

        const res = await apiCall(`/replies/${replyId}/send`, 'POST', { content });

        if (res.ok) {

            showToast('Reply sent successfully!', 'success');

            document.getElementById('reply-modal').style.display = 'none';

        } else {

            const data = await res.json();

            showToast('Failed to send reply: ' + (data.detail || ''), 'error');

        }

    } catch(e) {

        showToast('Network error sending reply.', 'error');

    } finally {

        btn.innerHTML = oldHtml;

        btn.disabled = false;

    }

}







async function loadAdminUsers() {



    try {



        const res = await fetch(`${API_URL}/admin/users`, { headers: { 'Authorization': `Bearer ${getToken()}` } });



        if (!res.ok) return;



        const users = await res.json();



        const tbody = document.getElementById('admin-users-body');



        if (!tbody) return;



        tbody.innerHTML = '';



        users.forEach(u => {



            const tr = document.createElement('tr');



            



            const statusBadge = u.is_approved



                ? `<span style="background:#dcfce7;color:#059669;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">✅ Approved</span>`



                : `<span style="background:#fef9c3;color:#ca8a04;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">⏳ Pending</span>`;



                



            let actionsHTML = '';



            let approveBtn = u.is_approved 



                ? `<button class="btn" disabled style="padding:5px 14px;font-size:12px;opacity:0.5;background:#e2e8f0;color:#64748b;"><i class='fa-solid fa-check' style='margin-right:4px;'></i>Approved</button>`



                : `<button class="btn primary" onclick="approveUser('${u.id}')" style="padding:5px 14px;font-size:12px;background:#059669;color:white;"><i class='fa-solid fa-check' style='margin-right:4px;'></i>Approve</button>`;



                



            let deleteBtn = u.is_admin 



                ? `<button class="btn" disabled style="padding:5px 10px;font-size:12px;background:#e2e8f0;color:#64748b;margin-left:8px;" title="Cannot delete admin"><i class='fa-solid fa-trash'></i> Delete</button>`



                : `<button class="btn danger" onclick="deleteUser('${u.id}')" style="padding:5px 10px;font-size:12px;background:#ef4444;color:white;margin-left:8px;"><i class='fa-solid fa-trash'></i> Delete</button>`;



            



            actionsHTML = approveBtn + deleteBtn;







            tr.innerHTML = `



                <td>${u.id}</td>



                <td>${escapeHtml(u.email)}</td>



                <td>${u.is_admin ? '<span style="color:#6366f1;font-weight:600;">Admin</span>' : `User ${statusBadge}`}</td>



                <td style="display:flex;align-items:center;">



                    ${actionsHTML}



                </td>



            `;



            tbody.appendChild(tr);



        });



    } catch(e) { console.error(e); }



}







window.approveUser = async function(id) {



    try {



        const res = await fetch(`${API_URL}/admin/users/${id}/approve`, { method: 'POST', headers: { 'Authorization': `Bearer ${getToken()}` } });



        if (res.ok) { 



            showToast('User approved successfully! ✅', 'success'); 



            loadAdminUsers(); 



        } else { 



            const d = await res.json();



            showToast(d.detail || 'Error approving user', 'error'); 



        }



    } catch(e) { showToast('Network error', 'error'); }



};







window.deleteUser = async function(id) {



    if (!confirm('Are you sure you want to delete this user completely?')) return;



    try {



        const res = await fetch(`${API_URL}/admin/users/${id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${getToken()}` } });



        if (res.ok) { 



            showToast('User deleted successfully', 'success'); 



            loadAdminUsers(); 



        } else {



            const d = await res.json();



            showToast(d.detail || 'Error deleting user', 'error');



        }



    } catch(e) { showToast('Network error', 'error'); }



};







// ============================================================



// AI CHAT



// ============================================================



function setupAIChat() {



    // Toggling logic has been moved to inline onclick handlers in index.html



}







async function renderColdMailList() {



    await fetchDashboard();



    const tbody = document.getElementById('cold-mail-list-tbody');



    if (!tbody) return;



    tbody.innerHTML = '';



    const campaigns = (window.lastFetchedCampaigns || []).filter(c => c.type === 'cold_mail');



    



    if (campaigns.length === 0) {



        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:32px;color:var(--text-muted);">No Cold Mail campaigns found.</td></tr>';



        return;



    }



    



    campaigns.forEach(c => {



        const tr = document.createElement('tr');



        const openRate = c.sent_count > 0 ? Math.round((c.opens / c.sent_count) * 100) : 0;



        const clickRate = c.sent_count > 0 ? Math.round((c.clicks / c.sent_count) * 100) : 0;



        const cStatus = c.status || 'Draft';



        const statusColor = cStatus.toLowerCase() === 'completed' ? '#059669' : (cStatus.toLowerCase() === 'failed' ? '#dc2626' : '#64748b');



        



        tr.innerHTML = `



            <td><div style="font-weight:600;color:var(--text);">${c.subject || 'Untitled'}</div></td>



            <td>



                <span style="font-size:13px; font-weight:600; color:${statusColor}; text-transform:capitalize;">${cStatus}</span>



                ${c.paused_reason ? `<div style="font-size:11px; color:#ef4444; margin-top:4px;"><i class="fa-solid fa-triangle-exclamation"></i> ${c.paused_reason}</div>` : ''}



            </td>



            <td>${openRate}%</td>



            <td>${clickRate}%</td>



            <td>



                <div style="display:flex; gap:6px; justify-content:flex-end;">



                    ${cStatus.toLowerCase() === 'processing' || cStatus.toLowerCase() === 'scheduled' ? `<button class="btn" style="padding:6px 12px;font-size:13px;background:#fffbeb;border:1px solid #fde68a;" onclick="pauseCampaign('${c.id}')" title="Pause"><i class="fa-solid fa-pause" style="color:#d97706;"></i></button>` : ''}



                    ${['paused', 'completed', 'failed'].includes(cStatus.toLowerCase()) ? `<button class="btn" style="padding:6px 12px;font-size:13px;background:#ecfdf5;border:1px solid #a7f3d0;" onclick="resumeCampaign('${c.id}')" title="Resume/Restart"><i class="fa-solid fa-play" style="color:#059669;"></i></button>` : ''}



                    <button class="btn" style="padding:6px 12px;font-size:13px;background:#eef2ff;border:1px solid #c7d2fe;" onclick="openCampaignAnalytics('${c.id}')" title="Analytics"><i class="fa-solid fa-chart-line" style="color:#4f46e5;"></i></button>

                    <button class="btn" style="padding:6px 12px;font-size:13px;background:#f8fafc;border:1px solid var(--border);" onclick="openColdMailBuilder('${c.id}')" title="Edit"><i class="fa-solid fa-pen-to-square" style="color:#64748b;"></i></button>



                    <button class="btn" style="padding:6px 12px;font-size:13px;background:#fef2f2;border:1px solid #fca5a5;" onclick="deleteCampaign('${c.id}')" title="Delete"><i class="fa-solid fa-trash" style="color:#ef4444;"></i></button>



                </div>



            </td>



        `;



        tbody.appendChild(tr);



    });



}







async function renderNewsletterList() {



    await fetchDashboard();



    const tbody = document.getElementById('newsletters-list-tbody');



    if (!tbody) return;



    tbody.innerHTML = '';



    const campaigns = window.lastFetchedBulkCampaigns || [];



    



    if (campaigns.length === 0) {



        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:32px;color:var(--text-muted);">No Newsletters found.</td></tr>';



        return;



    }



    



    campaigns.forEach(c => {



        const tr = document.createElement('tr');



        const cStatus = c.status || 'Draft';



        const statusColor = cStatus.toLowerCase() === 'completed' ? '#059669' : (cStatus.toLowerCase() === 'failed' ? '#dc2626' : '#64748b');



        



        tr.innerHTML = `



            <td><div style="font-weight:600;color:var(--text);">${c.name || 'Untitled'}</div></td>



            <td>



                <span style="font-size:13px; font-weight:600; color:${statusColor}; text-transform:capitalize;">${cStatus}</span>



                ${c.paused_reason ? `<div style="font-size:11px; color:#ef4444; margin-top:4px;"><i class="fa-solid fa-triangle-exclamation"></i> ${c.paused_reason}</div>` : ''}



            </td>



            <td>${c.sent_count}</td>



            <td>



                <div style="display:flex; gap:6px; justify-content:flex-end;">



                    ${cStatus.toLowerCase() === 'processing' || cStatus.toLowerCase() === 'scheduled' ? `<button class="btn" style="padding:6px 12px;font-size:13px;background:#fffbeb;border:1px solid #fde68a;" onclick="pauseCampaign('${c.id}')" title="Pause"><i class="fa-solid fa-pause" style="color:#d97706;"></i></button>` : ''}



                    ${['paused', 'completed', 'failed'].includes(cStatus.toLowerCase()) ? `<button class="btn" style="padding:6px 12px;font-size:13px;background:#ecfdf5;border:1px solid #a7f3d0;" onclick="resumeCampaign('${c.id}')" title="Resume/Restart"><i class="fa-solid fa-play" style="color:#059669;"></i></button>` : ''}



                    <button class="btn" style="padding:6px 12px;font-size:13px;background:#f8fafc;border:1px solid var(--border);" onclick="openNewsletterBuilder('${c.id}')" title="Edit"><i class="fa-solid fa-pen-to-square" style="color:#64748b;"></i></button>



                    <button class="btn" style="padding:6px 12px;font-size:13px;background:#fef2f2;border:1px solid #fca5a5;" onclick="deleteCampaign('${c.id}')" title="Delete"><i class="fa-solid fa-trash" style="color:#ef4444;"></i></button>



                </div>



            </td>



        `;



        tbody.appendChild(tr);



    });



}







window.openColdMailBuilder = async function(id) {



    document.querySelectorAll('#app-page .view').forEach(v => v.classList.remove('active'));



    const target = document.getElementById('cold-mail-builder');



    if (target) target.classList.add('active');



    



    if (id) {



        window.editCampaign(id);



    } else {



        // Create a blank draft campaign so we can save schedule etc immediately



    window.currentCampaignId = null;





        window.currentCampaignId = null;



        document.getElementById('inst-subject').value = '';

        document.getElementById('inst-body').value = '';

        document.getElementById('seq-leads').value = '';

        if (typeof window.renderLeadsList === 'function') window.renderLeadsList('seq-leads');

        localStorage.removeItem('saved_leads_seq-leads');

        

        if (window.renderSendingAccountsSelector) {

            window.renderSendingAccountsSelector('cold-sender-accounts-list', null);

        }

        

        // Reset schedule UI manually for a fresh start

        ['sch-day-mon','sch-day-tue','sch-day-wed','sch-day-thu','sch-day-fri'].forEach(id => {

        });



        ['sch-day-sat','sch-day-sun'].forEach(id => {



            const el = document.getElementById(id); if (el) el.checked = true;



        });



        const st = document.getElementById('sch-start-time'); if(st) st.value = '00:00';



        const et = document.getElementById('sch-end-time'); if(et) et.value = '00:00';







        window.switchColdTab('sequences');



    }



}







window.openNewsletterBuilder = async function(id) {



    document.querySelectorAll('#app-page .view').forEach(v => v.classList.remove('active'));



    const target = document.getElementById('campaigns-builder');



    if (target) target.classList.add('active');



    



    if (id) {



        window.editCampaign(id);



    } else {



        window.currentCampaignId = null;







        document.getElementById('campaign-subject').value = '';



        document.getElementById('newsletter-leads').value = '';



        if (typeof window.renderLeadsList === 'function') window.renderLeadsList('newsletter-leads');



        localStorage.removeItem('saved_leads_newsletter-leads');

        

        if (window.renderSendingAccountsSelector) {

            window.renderSendingAccountsSelector('vb-sender-accounts-list', null);

        }



        // Reset schedule UI manually for a fresh start



        ['vb-sch-day-mon','vb-sch-day-tue','vb-sch-day-wed','vb-sch-day-thu','vb-sch-day-fri'].forEach(id => {



            const el = document.getElementById(id); if (el) el.checked = true;



        });



        ['vb-sch-day-sat','vb-sch-day-sun'].forEach(id => {



            const el = document.getElementById(id); if (el) el.checked = true;



        });



        const st = document.getElementById('vb-sch-start-time'); if(st) st.value = '00:00';



        const et = document.getElementById('vb-sch-end-time'); if(et) et.value = '00:00';







        window.switchVbTab('audience');



    }



}







window.checkSpamScore = async function() {



    const text = document.getElementById('inst-body').value;



    const subject = document.getElementById('inst-subject').value || '';



    if (!text.trim()) {



        showToast("Please write an email first to check spam score.");



        return;



    }



    



    try {

        const res = await apiCall('/preflight', 'POST', {body: text, subject: subject});

        if (res && res.ok) {

            const data = await res.json();

            let msg = '';

            if (data.score >= 9) {



                msg = `Spam Score: ${data.score}/10 (${data.rating})`;



                showToast(msg, 'success');



            } else if (data.score >= 7) {



                msg = `Spam Score: ${data.score}/10 (${data.rating})`;



                if (data.found_words.length > 0) msg += ` | Spam words: ${data.found_words.join(', ')}`;



                if (data.warnings && data.warnings.length > 0) msg += ` | ${data.warnings[0]}`;



                showToast(msg, 'success');



            } else {



                msg = `Spam Score: ${data.score}/10 (${data.rating})`;



                if (data.found_words.length > 0) msg += ` | Spam words: ${data.found_words.join(', ')}`;



                if (data.warnings && data.warnings.length > 0) msg += ` | ${data.warnings.join('; ')}`;



                showToast(msg, 'error');



            }

        } else {

            const err = await res.json().catch(() => ({}));

            showToast(err.detail || 'Failed to check spam score', 'error');

        }



    } catch(e) {



        console.error(e);



        showToast("Error checking spam score.");



    }



};







const TEMPLATES = {



    saas_outreach: {



        subject: "{Quick question|Thoughts on} your {workflow|current process} at {{company}}?",



        body: "Hey {{firstName}},\n\nI noticed that {{company}} is growing {fast|rapidly}, and I was wondering how you're handling your current workflow.\n\n{Many|Several} companies like yours use our platform to {save time|automate tasks} and {reduce costs|increase efficiency}. \n\nWould you be open to a quick {5-minute|short} chat next week to see if there's a fit?\n\n{Best|Cheers},\nYour Name"



    },



    sales_followup: {



        subject: "{Following up|Checking in} - {{company}} / Our last {chat|email}",



        body: "Hi {{firstName}},\n\nI just wanted to {follow up|check in} on my previous email. {I know you're busy|Things get busy}, so I wanted to bump this to the top of your inbox.\n\nHave you had a chance to {review|look at} the info I sent over? Let me know if you have any questions or if now isn't the right time.\n\n{Thanks|Best regards},\nYour Name"



    },



    link_building: {



        subject: "{Quick question|Collab idea} about your article on {{company}} blog",



        body: "Hey {{firstName}},\n\nI was doing some research on {topic} and came across your excellent article on the {{company}} blog.\n\nI {really enjoyed|loved} your point about [insert point here]. I actually just published a comprehensive guide that {complements|expands on} your piece perfectly.\n\nWould you consider {linking to it|adding it as a resource}? I'd be happy to share your article with my {audience|newsletter} as well.\n\n{Cheers|Best},\nYour Name"



    }



};







window.loadTemplate = function() {



    const selector = document.getElementById('template-selector');



    const val = selector.value;



    



    if (val && TEMPLATES[val]) {



        document.getElementById('inst-subject').value = TEMPLATES[val].subject;



        document.getElementById('inst-body').value = TEMPLATES[val].body;



        showToast("Template loaded successfully!");



    } else {



        document.getElementById('inst-subject').value = "";



        document.getElementById('inst-body').value = "";



    }



};







function setupDragDrop(id) {



    const el = document.getElementById(id);



    if (!el) return;



    



    el.addEventListener('dragover', (e) => {



        e.preventDefault();



        el.style.borderColor = "var(--p)";



        el.style.background = "#eef2ff";



    });



    



    el.addEventListener('dragleave', (e) => {



        e.preventDefault();



        el.style.borderColor = "var(--border)";



        el.style.background = "#fff";



    });



    



    el.addEventListener('drop', (e) => {



        e.preventDefault();



        el.style.borderColor = "var(--border)";



        el.style.background = "#fff";



        



        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {



            const file = e.dataTransfer.files[0];



            if (file.name.endsWith('.csv') || file.name.endsWith('.txt')) {



                const reader = new FileReader();



                reader.onload = async function(evt) {



                    const text = evt.target.result;



                    let lines = text.split('\n').filter(l => l.trim().length > 0);



                    



                    showToast(`Validating ${lines.length} leads... please wait.`, 'success');



                    el.value = text;



                    



                    const emailsToCheck = lines.map(l => l.split(',')[0].trim()).filter(e => e);



                    



                    try {



                        const res = await apiCall('/validate-leads', 'POST', { emails: emailsToCheck });



                        if (res.ok) {



                            const data = await res.json();



                            const invalidEmails = new Set(data.results.filter(r => !r.valid).map(r => r.email.toLowerCase()));



                            



                            const validLines = lines.filter(l => {



                                const e = l.split(',')[0].trim().toLowerCase();



                                return !invalidEmails.has(e);



                            });



                            



                            el.value = validLines.join('\n');



                            



                            const removed = lines.length - validLines.length;



                            if (removed > 0) {



                                showToast(`⚠️ Removed ${removed} invalid/inactive leads. Loaded ${validLines.length} valid leads.`, 'error');



                            } else {



                                showToast(`✅ Successfully loaded ${validLines.length} healthy leads!`, 'success');



                            }



                        }



                    } catch (err) {



                        showToast(`✅ Loaded ${lines.length} leads (validation skipped)`, 'success');



                    }



                };



                reader.readAsText(file);



            } else {



                showToast("⚠️ Please drop a valid .csv or .txt file.");



            }



        }



    });



}







document.addEventListener('DOMContentLoaded', () => {



    setupDragDrop('seq-leads');



    setupDragDrop('newsletter-leads');



    



    // Restore saved leads



    ['seq-leads', 'newsletter-leads'].forEach(id => {



        const el = document.getElementById(id);



        const saved = localStorage.getItem('saved_leads_' + id);



        if (el && saved) el.value = saved;



        if (typeof window.renderLeadsList === 'function') {



            window.renderLeadsList(id);



        }



    });



});















// Inbox Preview Feature



window.previewInbox = function(subjectId, bodyId) {



    const subjectEl = document.getElementById(subjectId);



    const bodyEl = document.getElementById(bodyId);



    



    if (!subjectEl || !bodyEl) return;



    



    const subjectText = subjectEl.value || "(No Subject)";



    const bodyText = bodyEl.value || "(Empty Body)";



    



    document.getElementById('preview-subject').textContent = subjectText;



    



    // Inject into iframe for perfect HTML rendering without CSS leaks



    const frame = document.getElementById('preview-body-frame');



    if (frame) {



        const doc = frame.contentWindow.document;



        doc.open();



        doc.write(bodyText);



        doc.close();



    }



    



    document.getElementById('inbox-preview-modal').style.display = 'flex';



};















document.addEventListener('DOMContentLoaded', async () => {



    // Load Webhook



    const webhookUrlInput = document.getElementById('webhook-url');



    if (webhookUrlInput) {



        try {



            const res = await apiCall('/webhook');  // BUG-11 FIX: was '/api/webhook' causing double /api prefix



            if (res.ok) {



                const data = await res.json();



                if (data.url) webhookUrlInput.value = data.url;



            }



        } catch(e) {}



    }







    // Save Webhook



    const saveWebhookBtn = document.getElementById('save-webhook-btn');



    if (saveWebhookBtn) {



        saveWebhookBtn.addEventListener('click', async () => {



            const url = document.getElementById('webhook-url').value;



            saveWebhookBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';



            try {



            const res = await apiCall('/webhook', 'POST', { url });  // BUG-11 FIX: was '/api/webhook'



                const statusEl = document.getElementById('webhook-status');



                if (res.ok) {



                    statusEl.textContent = 'Webhook URL saved successfully!';



                    statusEl.className = 'alert success';



                } else {



                    statusEl.textContent = 'Failed to save webhook URL.';



                    statusEl.className = 'alert error';



                }



                statusEl.style.display = 'block';



                setTimeout(() => statusEl.style.display = 'none', 3000);



            } catch(e) { console.error(e); }



            saveWebhookBtn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Save Webhook';



        });



    }



});















// ============================================================



// ADMIN PANEL



// ============================================================



window.loadAdminUsers = async function() {



    var tbody = document.getElementById('admin-users-body');



    if (!tbody) return;



    tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:20px;color:#888;">Loading users...</td></tr>';



    try {



        var res = await apiCall('/admin/users');



        if (!res.ok) {



            var errData = await res.json().catch(function() { return {}; });



            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:red;padding:20px;">Error ' + res.status + ': ' + (errData.detail || 'Failed to load') + '</td></tr>';



            return;



        }



        var users = await res.json();



        if (!users || !users.length) {



            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#888;padding:20px;">No users found.</td></tr>';



            return;



        }



        var rows = '';



        for (var i = 0; i < users.length; i++) {



            var u = users[i];



            var shortId = u.id ? u.id.substring(0, 8) + '...' : '-';



            var roleBadge = u.is_admin



                ? '<span style="background:#4f46e5;color:#fff;padding:2px 10px;border-radius:20px;font-size:12px;font-weight:600;">Admin</span>'



                : '<span style="background:#e2e8f0;color:#475569;padding:2px 10px;border-radius:20px;font-size:12px;font-weight:600;">User</span>';



            var statusHtml = u.is_approved



                ? '<span style="color:#059669;font-weight:600;">&#10003; Approved</span>'



                : '<button onclick="window.approveUser(\'' + u.id + '\')" style="background:#059669;color:#fff;border:none;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:13px;font-weight:600;">&#10003; Approve</button>';



            var deleteBtn = (u.email === 'zmonemrahman@gmail.com')



                ? '<span style="color:#94a3b8;font-size:12px;">Protected</span>'



                : '<button onclick="window.deleteUser(\'' + u.id + '\')" style="background:#dc2626;color:#fff;border:none;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:13px;font-weight:600;">&#128465; Delete</button>';



            rows += '<tr>'



                + '<td style="padding:12px 16px;font-size:12px;color:#94a3b8;">' + shortId + '</td>'



                + '<td style="padding:12px 16px;font-weight:500;">' + escapeHtml(u.email) + '</td>'



                + '<td style="padding:12px 16px;">' + roleBadge + '</td>'



                + '<td style="padding:12px 16px;"><div style="display:flex;gap:8px;align-items:center;">' + statusHtml + ' ' + deleteBtn + '</div></td>'



                + '</tr>';



        }



        tbody.innerHTML = rows;



    } catch(e) {



        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:red;padding:20px;">Error: ' + e.message + '</td></tr>';



    }



};







window.approveUser = async function(id) {



    try {



        var res = await apiCall('/admin/users/' + id + '/approve', 'POST');



        if (res.ok) {



            showToast('User approved!', 'success');



            window.loadAdminUsers();



        } else {



            var err = await res.json().catch(function() { return {}; });



            showToast('Failed: ' + (err.detail || res.status), 'error');



        }



    } catch(e) {



        showToast('Error: ' + e.message, 'error');



    }



};







window.deleteUser = async function(id) {



    if (!confirm('Are you sure you want to delete this user?')) return;



    try {



        var res = await apiCall('/admin/users/' + id, 'DELETE');



        if (res.ok) {



            showToast('User deleted!', 'success');



            window.loadAdminUsers();



        } else {



            var err = await res.json().catch(function() { return {}; });



            showToast('Failed: ' + (err.detail || res.status), 'error');



        }



    } catch(e) {



        showToast('Error: ' + e.message, 'error');



    }



};







window.saveLeads = function(id) {



    const el = document.getElementById(id);



    if (!el) return;



    localStorage.setItem('saved_leads_' + id, el.value);



    if (typeof window.renderLeadsList === 'function') {



        window.renderLeadsList(id);



    }



    showToast('Leads saved successfully!', 'success');



};







window.clearLeads = function(id) {



    if(!confirm('Are you sure you want to clear all leads?')) return;



    const el = document.getElementById(id);



    if (!el) return;



    el.value = '';



    localStorage.removeItem('saved_leads_' + id);



    if (typeof window.renderLeadsList === 'function') {



        window.renderLeadsList(id);



    }



    showToast('Leads cleared!', 'info');



};







window.renderLeadsList = function(id) {



    const listEl = document.getElementById(id + '-list');



    const textarea = document.getElementById(id);



    if (!listEl || !textarea) return;



    



    const lines = textarea.value.split('\n').filter(l => l.trim() !== '');



    if (lines.length === 0) {



        listEl.innerHTML = '';



        return;



    }



    



    let html = '';



    const MAX_VISIBLE = 100;



    const visibleLines = lines.slice(0, MAX_VISIBLE);



    



    visibleLines.forEach((line, index) => {



        const parts = line.split(',').map(p => p.trim());



        const email = parts[0] || '';



        const name = parts[1] || 'Unknown';



        const company = parts[2] || '';



        



        html += `



        <div style="display:flex; justify-content:space-between; align-items:center; background:#fff; padding:12px 16px; border-radius:8px; border:1px solid var(--border); box-shadow:0 2px 5px rgba(0,0,0,0.02);">



            <div style="display:flex; flex-direction:column; gap:4px;">



                <div style="font-weight:600; font-size:14px; color:var(--text);">${email}</div>



                <div style="font-size:12px; color:var(--text-muted); display:flex; gap:12px;">



                    <span><i class="fa-regular fa-user" style="margin-right:4px;"></i>${name}</span>



                    ${company ? `<span><i class="fa-regular fa-building" style="margin-right:4px;"></i>${company}</span>` : ''}



                </div>



            </div>



            <button onclick="window.removeLeadItem('${id}', ${index})" style="background:#fef2f2; color:#ef4444; border:none; width:32px; height:32px; border-radius:6px; cursor:pointer; display:flex; align-items:center; justify-content:center; transition:0.2s;"><i class="fa-solid fa-xmark"></i></button>



        </div>`;



    });



    



    if (lines.length > MAX_VISIBLE) {



        html += `



        <div style="text-align:center; padding:16px; color:var(--text-muted); font-size:13px; background:#f8fafc; border-radius:8px; border:1px dashed var(--border);">



            <i class="fa-solid fa-circle-info" style="margin-right:6px; color:#3b82f6;"></i>



            Showing the first ${MAX_VISIBLE} of ${lines.length} total leads. The rest are hidden to maintain browser performance, but will be processed normally.



        </div>



        `;



    }



    



    listEl.innerHTML = html;



};







window.removeLeadItem = function(id, index) {



    const textarea = document.getElementById(id);



    if (!textarea) return;



    



    const lines = textarea.value.split('\n').filter(l => l.trim() !== '');



    lines.splice(index, 1);



    textarea.value = lines.join('\n');



    



    localStorage.setItem('saved_leads_' + id, textarea.value);



    window.renderLeadsList(id);



};



window.saveNewsletterSchedule = async function() {

    const btn = document.getElementById('vb-sch-save-btn');

    if (btn) { btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...'; btn.disabled = true; }



    const dayMap = {Mon:'vb-sch-day-mon', Tue:'vb-sch-day-tue', Wed:'vb-sch-day-wed', Thu:'vb-sch-day-thu', Fri:'vb-sch-day-fri', Sat:'vb-sch-day-sat', Sun:'vb-sch-day-sun'};

    const selectedDays = Object.entries(dayMap)

        .filter(([day, id]) => document.getElementById(id)?.checked)

        .map(([day]) => day);



    const startVal = document.getElementById('vb-sch-start-time')?.value || '00:00';

    const endVal = document.getElementById('vb-sch-end-time')?.value || '00:00';

    const startHour = parseInt(startVal.split(':')[0], 10) || 0;

    const endHour = parseInt(endVal.split(':')[0], 10) || 0;

    const tz = document.getElementById('vb-sch-timezone')?.value || 'UTC';



    const delayMin = parseInt(document.getElementById('vb-sch-delay-min')?.value) || 30;

    const delayMax = parseInt(document.getElementById('vb-sch-delay-max')?.value) || 90;



    const payload = {

        sending_days: JSON.stringify(selectedDays),

        start_hour: startHour,

        end_hour: endHour === 0 ? 24 : endHour,

        timezone: tz,

        delay_min: delayMin,

        delay_max: delayMax,

        track_opens: document.getElementById('vb-track-opens') ? document.getElementById('vb-track-opens').value === '1' : true,

        track_clicks: document.getElementById('vb-track-clicks') ? document.getElementById('vb-track-clicks').value === '1' : true,

        use_unsubscribe: document.getElementById('vb-use-unsubscribe') ? document.getElementById('vb-use-unsubscribe').value === '1' : true,

        max_emails_per_day: document.getElementById('vb-max-emails') ? parseInt(document.getElementById('vb-max-emails').value) || 50 : 50,

        daily_ramp_up: document.getElementById('vb-ramp-up') ? parseInt(document.getElementById('vb-ramp-up').value) || 5 : 5

    };



    if (!window.currentCampaignId) {

        // Auto-save as draft so schedule persists

        try {

            const subEl = document.getElementById('campaign-subject');

            const draftPayload = {

                name: (subEl ? subEl.value : '') || 'Untitled Newsletter',

                html_content: editor ? editor.exportHtml() : '',

                design_json: editor ? JSON.stringify(editor.exportDesign()) : '',

                leads: [],

                is_draft: false

            };



            const leadsText = (document.getElementById('newsletter-leads') || {}).value || '';

            leadsText.split('\n').map(l => l.trim()).filter(l => l).forEach(line => {

                const parts = line.split(',').map(p => p.trim());
                draftPayload.leads.push({ email: parts[0], name: parts[1] || '', company: parts[2] || '' });
            });



            if (window.getSelectedSenderIds) {

                const sendingIds = window.getSelectedSenderIds('vb-sender-accounts-list');

                if (sendingIds) {

                    draftPayload.sending_account_ids = JSON.stringify(sendingIds);

                }

            }



            const draftRes = await apiCall('/bulk-campaigns', 'POST', draftPayload);

            if (draftRes && draftRes.ok) {

                const draftData = await draftRes.json();

                window.currentCampaignId = draftData.campaign_id;

                if (!window.lastFetchedCampaigns) window.lastFetchedCampaigns = [];

                window.lastFetchedCampaigns.push({

                    id: draftData.campaign_id, subject: draftPayload.subject, body: '',

                    type: 'newsletter', status: 'draft',

                    sending_days: payload.sending_days, start_hour: payload.start_hour,

                    end_hour: payload.end_hour, timezone: payload.timezone,

                    delay_min: payload.delay_min, delay_max: payload.delay_max

                });

                showToast('Schedule saved! Draft created.', 'success');

            } else {

                const d = await draftRes.json().catch(() => ({}));

                showToast(d.detail || 'Failed to save schedule', 'error');

            }

        } catch(e) {

            showToast('Error saving schedule', 'error');

        }

        if (btn) { btn.innerHTML = '<i class="fa-solid fa-floppy-disk" style="margin-right:6px;"></i>Save Schedule'; btn.disabled = false; }

        return;

    }



    try {

        const res = await apiCall(`/campaigns/${window.currentCampaignId}/save-schedule`, 'POST', payload);

        if (res && res.ok) {

            showToast(' Schedule saved successfully!', 'success');

            if (window.lastFetchedCampaigns) {

                const idx = window.lastFetchedCampaigns.findIndex(x => x.id === window.currentCampaignId);

                if (idx !== -1) {

                    window.lastFetchedCampaigns[idx].sending_days = payload.sending_days;

                    window.lastFetchedCampaigns[idx].start_hour = payload.start_hour;

                    window.lastFetchedCampaigns[idx].end_hour = payload.end_hour;

                    window.lastFetchedCampaigns[idx].timezone = payload.timezone;

                    window.lastFetchedCampaigns[idx].delay_min = payload.delay_min;

                    window.lastFetchedCampaigns[idx].delay_max = payload.delay_max;

                }

            }

        } else {

            const d = await res.json().catch(() => ({}));

            showToast(d.detail || 'Failed to save schedule', 'error');

        }

    } catch (e) {

        console.error('Schedule save error', e);

        showToast('Error saving schedule', 'error');

    }

    if (btn) { btn.innerHTML = '<i class="fa-solid fa-floppy-disk" style="margin-right:6px;"></i>Save Schedule'; btn.disabled = false; }

};



// ============================================================

// IMAGE GALLERY

// ============================================================

let currentGalleryInputId = null;



window.openGalleryModal = function(inputId) {

    currentGalleryInputId = inputId;

    document.getElementById('gallery-modal').style.display = 'flex';

    fetchGalleryImages();

};



window.closeGalleryModal = function() {

    document.getElementById('gallery-modal').style.display = 'none';

    currentGalleryInputId = null;

};



window.fetchGalleryImages = function() {

    const grid = document.getElementById('gallery-grid');

    grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:20px;color:#64748b;"><i class="fa-solid fa-spinner fa-spin"></i> Loading...</div>';

    

    fetch('/api/gallery', {

        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }

    })

    .then(res => res.json())

    .then(data => {

        if (!Array.isArray(data)) {

            grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:20px;color:red;">Failed to load images.</div>';

            return;

        }

        if (data.length === 0) {

            grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:20px;color:#64748b;">No images found. Upload one to get started!</div>';

            return;

        }

        

        grid.innerHTML = data.map(media => `

            <div style="position:relative;border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;cursor:pointer;aspect-ratio:1;background:#f8fafc;" onclick="selectGalleryImage('${media.url}')">

                <img src="${media.url}" style="width:100%;height:100%;object-fit:contain;">

                <button onclick="event.stopPropagation(); deleteGalleryImage('${media.id}')" style="position:absolute;top:5px;right:5px;background:rgba(255,0,0,0.8);color:white;border:none;border-radius:4px;width:24px;height:24px;display:flex;align-items:center;justify-content:center;cursor:pointer;"><i class="fa-solid fa-trash"></i></button>

            </div>

        `).join('');

    })

    .catch(err => {

        grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:20px;color:red;">Error loading gallery.</div>';

    });

};



window.handleGalleryUpload = function(event) {

    const file = event.target.files[0];

    if (!file) return;

    

    const status = document.getElementById('gallery-upload-status');

    status.style.display = 'inline-block';

    

    const formData = new FormData();

    formData.append('file', file);

    

    fetch('/api/gallery/upload', {

        method: 'POST',

        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },

        body: formData

    })

    .then(res => res.json())

    .then(data => {

        status.style.display = 'none';

        event.target.value = '';

        if (data.status === 'success') {

            fetchGalleryImages();

        } else {

            alert('Upload failed: ' + (data.detail || 'Unknown error'));

        }

    })

    .catch(err => {

        status.style.display = 'none';

        alert('Upload error');

    });

};



window.deleteGalleryImage = function(id) {

    if(!confirm('Delete this image?')) return;

    fetch('/api/gallery/' + id, {

        method: 'DELETE',

        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }

    })

    .then(() => fetchGalleryImages());

};



window.selectGalleryImage = function(url) {

    if (currentGalleryInputId) {

        const input = document.getElementById(currentGalleryInputId);

        if (input) {

            input.value = url;

            // Trigger change event to update the preview

            const event = new Event('input', { bubbles: true });

            input.dispatchEvent(event);

        }

    }

    closeGalleryModal();

};

setInterval(async function() { try { await apiCall('/ping', 'GET'); } catch(e) {} }, 30000); 

function toggle3DHowToUse(btn) {

    const content = btn.nextElementSibling;

    const icon = btn.querySelector('.fa-chevron-down');

    

    if (content.style.maxHeight === '0px' || content.style.maxHeight === '') {

        content.style.maxHeight = content.scrollHeight + 'px';

        content.style.opacity = '1';

        content.style.transform = 'rotateX(0)';

        icon.style.transform = 'rotate(180deg)';

        btn.style.background = 'rgba(0,0,0,0.06)';

    } else {

        content.style.maxHeight = '0px';

        content.style.opacity = '0';

        content.style.transform = 'rotateX(-90deg)';

        icon.style.transform = 'rotate(0)';

        btn.style.background = 'rgba(0,0,0,0.02)';

    }

}

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

        

        let html = `

            <div style="margin-bottom:10px; position:relative;">

                <i class="fa-solid fa-search" style="position:absolute; left:10px; top:10px; color:var(--text-muted); font-size:12px;"></i>

                <input type="text" placeholder="Search accounts by name or email..." onkeyup="filterAccounts(this, '${containerId}')" style="width:100%; padding:8px 8px 8px 30px; font-size:13px; border:1px solid var(--border); border-radius:4px; background:var(--bg); color:var(--text); outline:none; box-sizing:border-box;">

            </div>

            <div class="accounts-list-scroll" style="max-height:160px; overflow-y:auto; padding-right:5px;">

        `;

        accounts.forEach(acc => {

            const isChecked = selectedIds.includes(acc.id) ? 'checked' : '';

            const searchStr = ((acc.name||'') + ' ' + (acc.email||'')).toLowerCase().replace(/'/g, "");

            html += `

                <label class="account-item-lbl" data-search="${searchStr}" style="display:flex; align-items:center; gap:8px; cursor:pointer; font-size:13px; padding:6px; border-radius:4px; transition:background 0.2s;" onmouseover="this.style.background='rgba(0,0,0,0.03)'" onmouseout="this.style.background='transparent'">

                    <input type="checkbox" class="sender-acc-checkbox" value="${acc.id}" ${isChecked} style="width:auto; margin:0;">

                    <div>

                        <div style="font-weight:600; color:var(--p);">${acc.name || 'No Name'}</div>

                        <div style="color:var(--text-muted); font-size:11px;">${acc.email}</div>

                    </div>

                </label>

            `;

        });

        html += '</div>';

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



window.filterAccounts = function(input, containerId) {

    const term = input.value.toLowerCase();

    const container = document.getElementById(containerId);

    if (!container) return;

    const labels = container.querySelectorAll('.account-item-lbl');

    labels.forEach(lbl => {

        if (lbl.getAttribute('data-search').includes(term)) {

            lbl.style.display = 'flex';

        } else {

            lbl.style.display = 'none';

        }

    });

};

