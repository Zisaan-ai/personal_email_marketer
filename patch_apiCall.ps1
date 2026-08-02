$content = Get-Content -Path 'C:\Users\higan\.gemini\antigravity\scratch\github_sync\xcomic.xyz\assets\app.js' -Raw

$replacement = "window._isSavingCampaign = false;
async function apiCall(endpoint, method = 'GET', body = null) {
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

# We need to find the old apiCall and replace it.
# The old apiCall looks like:
# async function apiCall(endpoint, method = 'GET', body = null) {
#     ...
#     if (res.status === 401) { logout(); throw new Error('Unauthorized'); }
#     return res;
# }

$regex = '(?s)async function apiCall\(endpoint, method = ''GET'', body = null\) \{.*?(?:return res;?
|return res;).*?\}'
$content = $content -replace $regex, $replacement

Set-Content -Path 'C:\Users\higan\.gemini\antigravity\scratch\github_sync\xcomic.xyz\assets\app.js' -Value $content
