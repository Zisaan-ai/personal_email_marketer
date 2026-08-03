window.SUPPORT = window.SUPPORT || {};

// Admin tab switching
window.SUPPORT.switchAdminTab = function(tabId) {
    document.querySelectorAll('.admin-tab').forEach(function(t) {
        t.classList.remove('active');
        t.style.borderBottom = '2px solid transparent';
        t.style.color = 'var(--text-muted)';
    });
    const activeTab = document.getElementById('tab-btn-' + tabId);
    if (activeTab) {
        activeTab.classList.add('active');
        activeTab.style.borderBottom = '2px solid var(--primary)';
        activeTab.style.color = 'var(--primary)';
    }

    document.querySelectorAll('.admin-section').forEach(function(s) { s.style.display = 'none'; });
    const activeSection = document.getElementById('admin-section-' + tabId);
    if (activeSection) activeSection.style.display = 'block';

    if (tabId === 'users' || tabId === 'free-users' || tabId === 'starter-users' || tabId === 'pro-users' || tabId === 'enterprise-users') {
        if (typeof loadAdminUsers === 'function') {
            loadAdminUsers();
        } else if (window.loadAdminUsers) {
            window.loadAdminUsers();
        }
    }
    if (tabId === 'tickets') {
        window.SUPPORT.loadAdminTickets();
    }
    if (tabId === 'payment') {
        if (typeof loadPaddleAdminSettings === 'function') {
            loadPaddleAdminSettings();
        } else if (window.loadPaddleAdminSettings) {
            window.loadPaddleAdminSettings();
        }
    }
    if (tabId === 'email') {
        if (typeof loadSmtpStatus === 'function') {
            loadSmtpStatus();
        } else if (window.loadSmtpStatus) {
            window.loadSmtpStatus();
        }
    }
};

// Show Create Ticket Modal
window.SUPPORT.showCreateModal = function() {
    var modal = document.getElementById('support-create-modal');
    if (modal) {
        var subj = document.getElementById('support-subject');
        var msg = document.getElementById('support-message');
        if (subj) subj.value = '';
        if (msg) msg.value = '';
        modal.style.display = 'flex';
    }
};

// Create Ticket
window.SUPPORT.createTicket = async function(btn) {
    var subject = (document.getElementById('support-subject') || {}).value || '';
    var message = (document.getElementById('support-message') || {}).value || '';

    if (!subject.trim() || !message.trim()) {
        if (typeof showToast === 'function') showToast('Please enter both subject and message', 'warning');
        return;
    }

    if (btn) { btn.disabled = true; btn.innerText = 'Submitting...'; }

    try {
        var res = await apiCall('/support/tickets', 'POST', { subject: subject, message: message });
        if (res.ok) {
            if (typeof showToast === 'function') showToast('Support ticket created successfully!', 'success');
            var modal = document.getElementById('support-create-modal');
            if (modal) modal.style.display = 'none';
            window.SUPPORT.loadUserTickets();
        } else {
            var err = await res.json().catch(function(){ return {}; });
            if (typeof showToast === 'function') showToast(err.detail || 'Failed to create ticket', 'error');
        }
    } catch(e) {
        if (typeof showToast === 'function') showToast('Error creating ticket: ' + e.message, 'error');
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Submit Ticket'; }
    }
};

// Load User Tickets
window.SUPPORT.loadUserTickets = async function() {
    var tbody = document.getElementById('user-tickets-body');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:24px;color:var(--text-muted);">Loading tickets...</td></tr>';

    try {
        var res = await apiCall('/support/tickets', 'GET');
        if (res.ok) {
            var data = await res.json();
            var tickets = data.tickets || [];
            tbody.innerHTML = '';
            if (tickets.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:24px;color:var(--text-muted);">No support tickets submitted yet. Click "New Ticket" to request help.</td></tr>';
                return;
            }

            tickets.forEach(function(t) {
                var tr = document.createElement('tr');
                var statusColor = t.status === 'Open' ? '#3b82f6' : t.status === 'Admin Reply' ? '#10b981' : t.status === 'Closed' ? '#64748b' : '#f59e0b';
                var statusBadge = `<span style="background:${statusColor}20; color:${statusColor}; padding:4px 10px; border-radius:12px; font-size:12px; font-weight:700;">${t.status}</span>`;

                tr.innerHTML = `
                    <td style="font-weight:600;">${t.subject}</td>
                    <td>${statusBadge}</td>
                    <td style="font-size:13px; color:var(--text-muted);">${t.updated_at ? t.updated_at.split('T')[0] : ''}</td>
                    <td>
                        <button class="btn" onclick="SUPPORT.viewTicket('${t.id}')" style="padding:4px 12px; font-size:12px; background:#3b82f6; color:#fff; border:none; border-radius:6px; cursor:pointer;"><i class="fa-solid fa-eye"></i> View</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch(e) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:24px;color:var(--danger);">Error loading tickets</td></tr>';
    }
};

// Load Admin Tickets
window.SUPPORT.loadAdminTickets = async function() {
    var tbody = document.getElementById('admin-all-tickets-body');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:24px;color:var(--text-muted);">Loading support tickets...</td></tr>';

    try {
        var res = await apiCall('/admin/tickets', 'GET');
        if (res.ok) {
            var data = await res.json();
            var tickets = data.tickets || [];
            tbody.innerHTML = '';
            if (tickets.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:24px;color:var(--text-muted);">No support tickets found.</td></tr>';
                return;
            }

            tickets.forEach(function(t) {
                var tr = document.createElement('tr');
                var statusColor = t.status === 'Open' ? '#ef4444' : t.status === 'User Reply' ? '#f59e0b' : t.status === 'Admin Reply' ? '#10b981' : '#64748b';
                var statusBadge = `<span style="background:${statusColor}20; color:${statusColor}; padding:4px 10px; border-radius:12px; font-size:12px; font-weight:700;">${t.status}</span>`;

                tr.innerHTML = `
                    <td><strong>${t.user_email || t.user_id}</strong></td>
                    <td style="font-weight:600;">${t.subject}</td>
                    <td>${statusBadge}</td>
                    <td>
                        <button class="btn" onclick="SUPPORT.viewTicket('${t.id}')" style="padding:5px 12px; font-size:12px; background:#4f46e5; color:#fff; border:none; border-radius:6px; cursor:pointer;"><i class="fa-solid fa-comments"></i> Manage</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch(e) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:24px;color:var(--danger);">Error loading tickets</td></tr>';
    }
};

// View Ticket Details
window.SUPPORT.viewTicket = async function(ticketId) {
    var modal = document.getElementById('support-view-modal');
    var container = document.getElementById('support-replies-container');
    var activeInput = document.getElementById('support-active-ticket-id');
    var adminActions = document.getElementById('support-admin-actions');
    var replyBox = document.getElementById('support-reply-box');

    if (!modal || !container) return;

    if (activeInput) activeInput.value = ticketId;
    container.innerHTML = '<div style="text-align:center;padding:20px;color:#64748b;">Loading ticket conversation...</div>';
    modal.style.display = 'flex';

    var isAdmin = localStorage.getItem('is_admin') === 'true' || localStorage.getItem('is_admin') === '1' || (window.currentUser && window.currentUser.is_admin);
    if (adminActions) {
        adminActions.style.display = isAdmin ? 'flex' : 'none';
    }

    try {
        var res = await apiCall('/support/tickets/' + ticketId, 'GET');
        if (res.ok) {
            var t = await res.json();
            var titleEl = document.getElementById('support-view-title');
            if (titleEl) titleEl.innerHTML = `<i class="fa-solid fa-comments"></i> Ticket #${t.id.substring(0,8)}: ${t.subject}`;
            
            container.innerHTML = '';
            var msgs = t.messages || [];
            
            msgs.forEach(function(m) {
                var isSelf = (isAdmin && m.is_admin) || (!isAdmin && !m.is_admin);
                var div = document.createElement('div');
                div.style.cssText = `max-width:80%; padding:12px 16px; border-radius:12px; margin-bottom:8px; align-self:${isSelf ? 'flex-end' : 'flex-start'}; background:${isSelf ? '#4f46e5' : '#fff'}; color:${isSelf ? '#fff' : '#1e293b'}; border:${isSelf ? 'none' : '1px solid #e2e8f0'}; box-shadow:0 2px 4px rgba(0,0,0,0.05);`;

                var timeStr = m.created_at ? new Date(m.created_at).toLocaleString() : '';
                div.innerHTML = `
                    <div style="font-size:11px; font-weight:700; opacity:0.8; margin-bottom:4px;">${m.sender_email || (m.is_admin ? 'Support Admin' : 'User')} • ${timeStr}</div>
                    <div style="font-size:14px; white-space:pre-wrap; line-height:1.5;">${m.message}</div>
                `;
                container.appendChild(div);
            });

            container.scrollTop = container.scrollHeight;

            if (replyBox) {
                if (t.status === 'Closed') {
                    replyBox.style.display = 'none';
                } else {
                    replyBox.style.display = 'block';
                }
            }
        }
    } catch(e) {
        container.innerHTML = '<div style="text-align:center;padding:20px;color:#ef4444;">Error loading conversation</div>';
    }
};

// Reply to Ticket
window.SUPPORT.replyToTicket = async function(btn) {
    var ticketId = (document.getElementById('support-active-ticket-id') || {}).value;
    var msgInput = document.getElementById('support-reply-message');
    var message = (msgInput || {}).value || '';

    if (!ticketId || !message.trim()) {
        if (typeof showToast === 'function') showToast('Please enter a reply message', 'warning');
        return;
    }

    if (btn) { btn.disabled = true; btn.innerText = 'Sending...'; }

    try {
        var res = await apiCall('/support/tickets/' + ticketId + '/reply', 'POST', { message: message });
        if (res.ok) {
            if (msgInput) msgInput.value = '';
            if (typeof showToast === 'function') showToast('Reply sent!', 'success');
            window.SUPPORT.viewTicket(ticketId);
            var isAdmin = localStorage.getItem('is_admin') === 'true';
            if (isAdmin) window.SUPPORT.loadAdminTickets();
            else window.SUPPORT.loadUserTickets();
        } else {
            var err = await res.json().catch(function(){ return {}; });
            if (typeof showToast === 'function') showToast(err.detail || 'Failed to send reply', 'error');
        }
    } catch(e) {
        if (typeof showToast === 'function') showToast('Error sending reply: ' + e.message, 'error');
    } finally {
        if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Send Reply'; }
    }
};

// Resolve Ticket
window.SUPPORT.resolveTicket = async function() {
    var ticketId = (document.getElementById('support-active-ticket-id') || {}).value;
    if (!ticketId) return;

    try {
        var res = await apiCall('/admin/tickets/' + ticketId + '/status', 'PUT', { status: 'Closed' });
        if (res.ok) {
            if (typeof showToast === 'function') showToast('Ticket resolved and closed', 'success');
            var modal = document.getElementById('support-view-modal');
            if (modal) modal.style.display = 'none';
            window.SUPPORT.loadAdminTickets();
        }
    } catch(e) {
        if (typeof showToast === 'function') showToast('Error resolving ticket', 'error');
    }
};

// Delete Ticket
window.SUPPORT.deleteTicket = async function() {
    var ticketId = (document.getElementById('support-active-ticket-id') || {}).value;
    if (!ticketId) return;
    if (!confirm('Are you sure you want to delete this ticket?')) return;

    try {
        var res = await apiCall('/admin/tickets/' + ticketId, 'DELETE');
        if (res.ok) {
            if (typeof showToast === 'function') showToast('Ticket deleted', 'success');
            var modal = document.getElementById('support-view-modal');
            if (modal) modal.style.display = 'none';
            window.SUPPORT.loadAdminTickets();
        }
    } catch(e) {
        if (typeof showToast === 'function') showToast('Error deleting ticket', 'error');
    }
};

// Check unread tickets badge
window.SUPPORT.checkUnreadTickets = async function() {
    try {
        var isAdmin = localStorage.getItem('is_admin') === 'true';
        var endpoint = isAdmin ? '/admin/tickets/unread-count' : '/support/tickets/unread-count';
        var res = await apiCall(endpoint, 'GET');
        if (res.ok) {
            var data = await res.json();
            var count = data.count || 0;
            var badge = document.getElementById('tab-tickets-unread-badge');
            if (badge) {
                if (count > 0) {
                    badge.innerText = count;
                    badge.style.display = 'inline-flex';
                } else {
                    badge.style.display = 'none';
                }
            }
        }
    } catch(e) {}
};
