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
};
