with open('frontend/assets/app.js', 'a', encoding='utf-8') as f:
    f.write('''\n
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

    const payload = {
        sending_days: JSON.stringify(selectedDays),
        start_hour: startHour,
        end_hour: endHour === 0 ? 24 : endHour,
        timezone: tz
    };

    if (!window.currentCampaignId) {
        showToast('Schedule settings will be saved automatically when you Launch or Save Draft!', 'success');
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
''')
