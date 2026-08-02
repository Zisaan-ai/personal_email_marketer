$content = Get-Content -Path 'C:\Users\higan\.gemini\antigravity\scratch\github_sync\xcomic.xyz\assets\app.js' -Raw

$content = $content -replace 'window.saveSchedule = async function\(event\) \{', "window.isSavingCampaign = false;

window.saveSchedule = async function(event) {
    if (window.isSavingCampaign) return; window.isSavingCampaign = true;"
$content = $content -replace '        const res = await apiCall\(/campaigns/\$\{window.currentCampaignId\}/save-schedule, ''POST'', payload\);', "        const res = await apiCall(/campaigns/ + window.currentCampaignId + /save-schedule, 'POST', payload);"

Set-Content -Path 'C:\Users\higan\.gemini\antigravity\scratch\github_sync\xcomic.xyz\assets\app.js' -Value $content
