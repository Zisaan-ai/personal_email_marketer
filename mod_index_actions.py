with open('frontend/index.html', encoding='utf-8') as f:
    text = f.read()

vb_orig = '''<span class="status-pill" id="vb-analytics-status" style="font-size:13px;padding:4px 12px;">Loading</span>
                </div>'''
vb_new = '''<span class="status-pill" id="vb-analytics-status" style="font-size:13px;padding:4px 12px;">Loading</span>
                    <div style="flex:1;"></div>
                    <div id="vb-analytics-actions" style="display:flex;gap:12px;"></div>
                </div>'''

cold_orig = '''<span class="status-pill" id="cold-analytics-status" style="font-size:13px;padding:4px 12px;">Loading</span>
                    
                    <div style="flex:1;"></div>
                    
                    <div style="display:flex;gap:12px;">
                        <button class="btn" style="padding:8px 16px;font-size:13px;background:#fff;"><i class="fa-solid fa-share-nodes"></i> Share Report</button>
                    </div>'''
cold_new = '''<span class="status-pill" id="cold-analytics-status" style="font-size:13px;padding:4px 12px;">Loading</span>
                    
                    <div style="flex:1;"></div>
                    
                    <div style="display:flex;gap:12px;">
                        <div id="cold-analytics-actions" style="display:flex;gap:12px;"></div>
                        <button class="btn" style="padding:8px 16px;font-size:13px;background:#fff;"><i class="fa-solid fa-share-nodes"></i> Share Report</button>
                    </div>'''

text = text.replace(vb_orig, vb_new)
text = text.replace(cold_orig, cold_new)
text = text.replace('app.js?v=3002', 'app.js?v=3004')

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
