window.SUPPORT = window.SUPPORT || {};

window.SUPPORT.switchAdminTab = function(tabId) {
    document.querySelectorAll('.admin-tab').forEach(t => {
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

    document.querySelectorAll('.admin-section').forEach(s => s.style.display = 'none');
    const activeSection = document.getElementById('admin-section-' + tabId);
    if (activeSection) activeSection.style.display = 'block';

    if (tabId === 'users' || tabId === 'free-users' || tabId === 'starter-users' || tabId === 'pro-users' || tabId === 'enterprise-users') {
        if (typeof loadAdminUsers === 'function') {
            loadAdminUsers();
        } else if (window.loadAdminUsers) {
            window.loadAdminUsers();
        }
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

window.SUPPORT.showCreateModal = function() {
    var modal = document.getElementById('support-create-modal');
    if (modal) {
        var sub = document.getElementById('support-subject');
        var msg = document.getElementById('support-message');
        if (sub) sub.value = '';
        if (msg) msg.value = '';
        modal.style.display = 'flex';
    }
};

window.SUPPORT.createTicket = async function(btn) {
    var subEl = document.getElementById('support-subject');
    var msgEl = document.getElementById('support-message');
    var subject = subEl ? subEl.value.trim() : '';
    var message = msgEl ? msgEl.value.trim() : '';

    if (!subject || !message) {
        if (typeof showToast === 'function') showToast('Please enter both subject and message', 'error');
        return;
    }

    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Submitting...'; }

    try {
        var res = await apiCall('/support/tickets', 'POST', { subject: subject, message: message });
        if (res.ok) {
            if (typeof showToast === 'function') showToast('Ticket submitted successfully!', 'success');
            var modal = document.getElementById('support-create-modal');
            if (modal) modal.style.display = 'none';
            window.SUPPORT.loadUserTickets();
        } else {
            var err = await res.json().catch(function() { return {}; });
            if (typeof showToast === 'function') showToast(err.detail || 'Failed to submit ticket', 'error');
        }
    } catch(e) {
        console.error(e);
        if (typeof showToast === 'function') showToast('Error submitting ticket', 'error');
    } finally {
        if (btn) { btn.disabled = false; btn.innerHTML = 'Submit Ticket'; }
    }
};

window.SUPPORT.loadUserTickets = async function() {
    try {
        var res = await apiCall('/support/tickets', 'GET');
        if (!res.ok) return;
        var tickets = await res.json();
        var tbody = document.getElementById('user-tickets-body');
        if (!tbody) return;
        tbody.innerHTML = '';
        if (tickets.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="padding:20px;text-align:center;color:var(--text-muted);">No support tickets submitted yet</td></tr>';
            return;
        }
        tickets.forEach(function(t) {
            var tr = document.createElement('tr');
            var statusColor = t.status === 'open' ? '#eab308' : t.status === 'resolved' ? '#22c55e' : '#3b82f6';
            var dateStr = t.created_at ? new Date(t.created_at).toLocaleDateString() : '-';
            tr.innerHTML = `
                <td style="padding:16px 24px;font-weight:600;color:var(--text);">${escapeHtml(t.subject || '')}</td>
                <td style="padding:16px 24px;"><span style="background:${statusColor}20;color:${statusColor};padding:4px 10px;border-radius:12px;font-size:12px;font-weight:700;text-transform:capitalize;">${t.status || 'open'}</span></td>
                <td style="padding:16px 24px;font-size:13px;color:var(--text-muted);">${dateStr}</td>
                <td style="padding:16px 24px;"><button class="btn secondary" style="padding:6px 12px;font-size:12px;" onclick="SUPPORT.viewTicket('${t.id}')"><i class="fa-solid fa-eye"></i> View</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch(e) { console.error('loadUserTickets error:', e); }
};

window.SUPPORT.viewTicket = async function(ticketId) {
    try {
        var res = await apiCall('/support/tickets/' + ticketId, 'GET');
        if (!res.ok) return;
        var data = await res.json();
        var ticket = data.ticket || data;
        var replies = data.replies || [];

        var activeIdEl = document.getElementById('support-active-ticket-id');
        var titleEl = document.getElementById('support-view-title');
        var container = document.getElementById('support-replies-container');
        var adminActions = document.getElementById('support-admin-actions');

        if (activeIdEl) activeIdEl.value = ticket.id || ticketId;
        if (titleEl) titleEl.innerHTML = '<i class="fa-solid fa-comments"></i> ' + escapeHtml(ticket.subject || 'Ticket');

        var isAdmin = localStorage.getItem('is_admin') === 'true';
        if (adminActions) adminActions.style.display = isAdmin ? 'flex' : 'none';

        if (container) {
            container.innerHTML = '';
            var firstMsg = document.createElement('div');
            firstMsg.style.cssText = 'background:#fff;padding:14px 18px;border-radius:10px;box-shadow:0 1px 3px rgba(0,0,0,0.05);';
            firstMsg.innerHTML = `<div style="font-size:12px;font-weight:700;color:var(--primary);margin-bottom:4px;">Original Message</div><div style="font-size:14px;color:var(--text);">${escapeHtml(ticket.message || '')}</div>`;
            container.appendChild(firstMsg);

            replies.forEach(function(r) {
                var div = document.createElement('div');
                var isUser = r.sender_type === 'user';
                div.style.cssText = `background:${isUser ? '#e0e7ff' : '#fff'};padding:12px 16px;border-radius:10px;align-self:${isUser ? 'flex-end' : 'flex-start'};max-width:85%;box-shadow:0 1px 3px rgba(0,0,0,0.05);`;
                div.innerHTML = `<div style="font-size:11px;font-weight:700;color:#64748b;margin-bottom:2px;">${r.sender_name || (isUser ? 'You' : 'Support Team')}</div><div style="font-size:14px;color:var(--text);">${escapeHtml(r.message || '')}</div>`;
                container.appendChild(div);
            });
        }

        var modal = document.getElementById('support-view-modal');
        if (modal) modal.style.display = 'flex';
    } catch(e) { console.error('viewTicket error:', e); }
};

window.SUPPORT.replyToTicket = async function(btn) {
    var ticketIdEl = document.getElementById('support-active-ticket-id');
    var msgEl = document.getElementById('support-reply-message');
    var ticketId = ticketIdEl ? ticketIdEl.value : '';
    var message = msgEl ? msgEl.value.trim() : '';

    if (!ticketId || !message) {
        if (typeof showToast === 'function') showToast('Please enter a reply message', 'error');
        return;
    }

    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...'; }

    try {
        var res = await apiCall('/support/tickets/' + ticketId + '/reply', 'POST', { message: message });
        if (res.ok) {
            if (msgEl) msgEl.value = '';
            if (typeof showToast === 'function') showToast('Reply sent successfully!', 'success');
            window.SUPPORT.viewTicket(ticketId);
        } else {
            var err = await res.json().catch(function() { return {}; });
            if (typeof showToast === 'function') showToast(err.detail || 'Failed to send reply', 'error');
        }
    } catch(e) {
        console.error(e);
        if (typeof showToast === 'function') showToast('Error sending reply', 'error');
    } finally {
        if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Send Reply'; }
    }
};

window.SUPPORT.resolveTicket = async function() {
    var ticketId = document.getElementById('support-active-ticket-id')?.value;
    if (!ticketId) return;
    try {
        var res = await apiCall('/admin/tickets/' + ticketId + '/status', 'PUT', { status: 'resolved' });
        if (res.ok) {
            if (typeof showToast === 'function') showToast('Ticket marked as resolved!', 'success');
            document.getElementById('support-view-modal').style.display = 'none';
            window.SUPPORT.loadUserTickets();
        }
    } catch(e) {}
};

window.SUPPORT.deleteTicket = async function() {
    var ticketId = document.getElementById('support-active-ticket-id')?.value;
    if (!ticketId || !confirm('Are you sure you want to delete this ticket?')) return;
    try {
        var res = await apiCall('/admin/tickets/' + ticketId, 'DELETE');
        if (res.ok) {
            if (typeof showToast === 'function') showToast('Ticket deleted!', 'success');
            document.getElementById('support-view-modal').style.display = 'none';
            window.SUPPORT.loadUserTickets();
        }
    } catch(e) {}
};

window.SUPPORT.checkUnreadTickets = async function() {
    try {
        var res = await apiCall('/support/tickets/unread-count', 'GET');
        if (res.ok) {
            var data = await res.json();
            var badge = document.getElementById('user-support-badge');
            if (badge && data.unread_count > 0) {
                badge.textContent = data.unread_count;
                badge.style.display = 'inline-flex';
            }
        }
    } catch(e) {}
};
