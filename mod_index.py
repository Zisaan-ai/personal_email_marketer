analytics_tab_html = """
            <!-- ANALYTICS TAB -->
            <div id="vb-tab-analytics" class="vb-tab-content" style="display:none;">
                <div style="display:flex;align-items:center;margin-bottom:32px;background:#f8fafc;padding:16px 24px;border-radius:12px;border:1px solid var(--border);">
                    <span style="font-size:14px;color:var(--text-muted);font-weight:600;margin-right:12px;">Campaign Status:</span>
                    <span class="status-pill" id="vb-analytics-status" style="font-size:13px;padding:4px 12px;">Loading</span>
                </div>

                <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:24px;margin-bottom:32px;">
                    <div class="stat-card" style="background:#fff;padding:24px;border-radius:16px;box-shadow:0 2px 12px rgba(0,0,0,0.03);border:1px solid rgba(0,0,0,0.04);">
                        <div style="font-size:14px;color:var(--text-muted);font-weight:600;margin-bottom:8px;">Leads Contacted</div>
                        <div style="font-size:32px;font-weight:800;color:var(--text);" id="vb-analytics-seq-started">0</div>
                    </div>
                    <div class="stat-card" style="background:#fff;padding:24px;border-radius:16px;box-shadow:0 2px 12px rgba(0,0,0,0.03);border:1px solid rgba(0,0,0,0.04);">
                        <div style="font-size:14px;color:var(--text-muted);font-weight:600;margin-bottom:8px;">Open Rate</div>
                        <div style="display:flex;align-items:baseline;gap:12px;">
                            <div style="font-size:32px;font-weight:800;color:var(--text);" id="vb-analytics-open-rate">0%</div>
                            <div style="font-size:14px;color:var(--text-muted);font-weight:600;" id="vb-analytics-open-count">(0 opens)</div>
                        </div>
                    </div>
                    <div class="stat-card" style="background:#fff;padding:24px;border-radius:16px;box-shadow:0 2px 12px rgba(0,0,0,0.03);border:1px solid rgba(0,0,0,0.04);">
                        <div style="font-size:14px;color:var(--text-muted);font-weight:600;margin-bottom:8px;">Click Rate</div>
                        <div style="display:flex;align-items:baseline;gap:12px;">
                            <div style="font-size:32px;font-weight:800;color:var(--text);" id="vb-analytics-click-rate">0%</div>
                            <div style="font-size:14px;color:var(--text-muted);font-weight:600;" id="vb-analytics-click-count">(0 clicks)</div>
                        </div>
                    </div>
                </div>
                
                <div class="glass" style="padding:24px;border-radius:16px;">
                    <h4 style="font-size:16px;font-weight:700;margin-bottom:16px;">Campaign Leads Analytics</h4>
                    <div style="overflow-x:auto;">
                        <table class="table" style="margin:0;">
                            <thead>
                                <tr>
                                    <th style="padding:12px 16px; font-weight:600; color:var(--text-muted); font-size:12px;">Email</th>
                                    <th style="padding:12px 16px; font-weight:600; color:var(--text-muted); font-size:12px;">Name</th>
                                    <th style="padding:12px 16px; font-weight:600; color:var(--text-muted); font-size:12px;">Status</th>
                                </tr>
                            </thead>
                            <tbody id="vb-analytics-leads-tbody">
                                <!-- Populated dynamically by JS -->
                                <tr><td colspan="3" style="text-align:center;padding:24px;color:var(--text-muted);">Loading leads...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
"""

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

if 'vb-tab-analytics' not in text:
    text = text.replace('<div id="tab-builder">', '<div id="tab-builder">\n' + analytics_tab_html)
    
    tab_html = '<div class="vb-tab" data-vbtab="analytics" style="padding-bottom:12px;font-weight:600;color:var(--text-muted);cursor:pointer;">Analytics</div>\n                '
    text = text.replace('<div class="vb-tab active" data-vbtab="audience"', tab_html + '<div class="vb-tab active" data-vbtab="audience"')
    
    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Added Analytics tab to Visual Builder in index.html')
