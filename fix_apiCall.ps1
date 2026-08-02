$content = Get-Content -Path 'C:\Users\higan\.gemini\antigravity\scratch\github_sync\xcomic.xyz\assets\app.js' -Raw

$old = "async function apiCall(endpoint, method = 'GET', body = null) {
    if ((endpoint === '/campaigns/send' || endpoint.endsWith('/save-schedule')) && method === 'POST') {
        if (window._isSavingCampaign) {
            return new Response(JSON.stringify({ detail: 'Please wait, saving...' }), { status: 429, headers: { 'Content-Type': 'application/json' } });
        }
        window._isSavingCampaign = true;
    }
    try {
        const token = getToken();
        const headers = { 'Authorization': `Bearer ${token}` };
        if (body) headers['Content-Type'] = 'application/json';
        const res = await fetch(API_BASE + endpoint, {
            method,
            headers,
            body: body ? JSON.stringify(body) : null
        });
        if ((endpoint === '/campaigns/send' || endpoint.endsWith('/save-schedule')) && method === 'POST') {
            window._isSavingCampaign = false;
        }
        if (res.status === 401) { logout(); throw new Error('Unauthorized'); }
        return res;
    } catch (err) {
        if ((endpoint === '/campaigns/send' || endpoint.endsWith('/save-schedule')) && method === 'POST') {
            window._isSavingCampaign = false;
        }
        throw err;
    }
}"

$new = "async function apiCall(endpoint, method = 'GET', body = null) {
    if ((endpoint === '/campaigns/send' || endpoint.endsWith('/save-schedule')) && method === 'POST') {
        if (window._isSavingCampaign) {
            return new Response(JSON.stringify({ detail: 'Please wait, saving...' }), { status: 429, headers: { 'Content-Type': 'application/json' } });
        }
        window._isSavingCampaign = true;
    }
    try {
        const token = getToken();
        const headers = { 'Authorization': `Bearer ${token}` };
        if (body) headers['Content-Type'] = 'application/json';
        if (method === 'GET') { endpoint += (endpoint.includes('?') ? '&' : '?') + 't=' + new Date().getTime(); }
        const res = await fetch(API_URL + endpoint, {
            method,
            headers,
            body: body ? JSON.stringify(body) : null,
            cache: 'no-store'
        });
        if ((endpoint === '/campaigns/send' || endpoint.endsWith('/save-schedule')) && method === 'POST') {
            window._isSavingCampaign = false;
        }
        if (res.status === 401) {
            try { localStorage.removeItem('token'); localStorage.removeItem('is_admin'); localStorage.removeItem('user'); localStorage.removeItem('xcomic_token'); } catch(e) {}
            var authPage = document.getElementById('auth-page');
            if (authPage && authPage.classList.contains('hidden')) { location.reload(); } else { throw new Error('Unauthorized'); }
        }
        return res;
    } catch (err) {
        if ((endpoint === '/campaigns/send' || endpoint.endsWith('/save-schedule')) && method === 'POST') {
            window._isSavingCampaign = false;
        }
        throw err;
    }
}"

$content = $content.Replace($old, $new)
Set-Content -Path 'C:\Users\higan\.gemini\antigravity\scratch\github_sync\xcomic.xyz\assets\app.js' -Value $content
