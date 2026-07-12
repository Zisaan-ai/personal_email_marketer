with open('frontend/assets/app.js', encoding='utf-8') as f:
    text = f.read()

# 1. Inject openCampaignAnalytics function
if 'openCampaignAnalytics' not in text:
    analytics_fn = """
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

window.editCampaign = function(id) {"""
    text = text.replace("window.editCampaign = function(id) {", analytics_fn)

# 2. Add button to renderColdMailList
orig_cold_btns = """                    <button class="btn" style="padding:6px 12px;font-size:13px;background:#f8fafc;border:1px solid var(--border);" onclick="openColdMailBuilder('${c.id}')" title="Edit"><i class="fa-solid fa-pen-to-square" style="color:#64748b;"></i></button>"""
new_cold_btns = """                    <button class="btn" style="padding:6px 12px;font-size:13px;background:#eef2ff;border:1px solid #c7d2fe;" onclick="openCampaignAnalytics('${c.id}')" title="Analytics"><i class="fa-solid fa-chart-line" style="color:#4f46e5;"></i></button>
                    <button class="btn" style="padding:6px 12px;font-size:13px;background:#f8fafc;border:1px solid var(--border);" onclick="openColdMailBuilder('${c.id}')" title="Edit"><i class="fa-solid fa-pen-to-square" style="color:#64748b;"></i></button>"""
text = text.replace(orig_cold_btns, new_cold_btns)

# 3. Add button to renderNewsletterList
orig_news_btns = """                    <button class="btn" style="padding:6px 12px;font-size:13px;background:#f8fafc;border:1px solid var(--border);" onclick="editCampaign('${c.id}')" title="Edit"><i class="fa-solid fa-pen-to-square" style="color:#64748b;"></i></button>"""
new_news_btns = """                    <button class="btn" style="padding:6px 12px;font-size:13px;background:#eef2ff;border:1px solid #c7d2fe;" onclick="openCampaignAnalytics('${c.id}')" title="Analytics"><i class="fa-solid fa-chart-line" style="color:#4f46e5;"></i></button>
                    <button class="btn" style="padding:6px 12px;font-size:13px;background:#f8fafc;border:1px solid var(--border);" onclick="editCampaign('${c.id}')" title="Edit"><i class="fa-solid fa-pen-to-square" style="color:#64748b;"></i></button>"""
text = text.replace(orig_news_btns, new_news_btns)

with open('frontend/assets/app.js', 'w', encoding='utf-8') as f:
    f.write(text)
print("Added Analytics buttons!")
