import sys
with open('frontend/index.html', encoding='utf-8') as f:
    text = f.read()

# For Visual Builder
orig_vb_btns = '''<button id="save-newsletter-draft-btn" class="btn" style="padding:16px 32px;font-size:15px;flex:1;background:var(--surface-1);border:1px solid var(--border);"><i class="fa-solid fa-save"></i> Save Draft</button>
                            <button id="send-btn" class="btn primary" style="padding:16px 32px;font-size:15px;flex:1;"><i class="fa-solid fa-rocket"></i> Launch Newsletter</button>'''

new_vb_btns = '''<button id="save-newsletter-draft-btn" class="btn" style="padding:16px 32px;font-size:15px;flex:1;background:var(--surface-1);border:1px solid var(--border);"><i class="fa-solid fa-save"></i> Save Draft</button>
                            <button id="send-btn" class="btn primary" style="padding:16px 32px;font-size:15px;flex:1;"><i class="fa-solid fa-rocket"></i> Launch Newsletter</button>
                            <div id="vb-status-actions" style="display:none; flex:1; gap:12px;"></div>'''

# For Cold Mail
orig_cold_btns = '''<button id="inst-save-draft-btn" class="btn" style="padding:12px 24px;background:#e2e8f0;color:#1e293b;border:1px solid #cbd5e1;font-size:15px;border-radius:8px;font-weight:600;margin-right:8px;"><i class="fa-solid fa-save" style="margin-right:6px;"></i>Save Draft</button>
                    <button id="inst-send-seq-btn" class="btn" style="padding:12px 24px;background:#4f46e5;color:#ffffff;border:none;font-size:15px;border-radius:8px;font-weight:600;box-shadow:0 4px 12px rgba(99,102,241,0.3);"><i class="fa-solid fa-rocket" style="margin-right:6px;"></i>Launch Campaign</button>'''

new_cold_btns = '''<button id="inst-save-draft-btn" class="btn" style="padding:12px 24px;background:#e2e8f0;color:#1e293b;border:1px solid #cbd5e1;font-size:15px;border-radius:8px;font-weight:600;margin-right:8px;"><i class="fa-solid fa-save" style="margin-right:6px;"></i>Save Draft</button>
                    <button id="inst-send-seq-btn" class="btn" style="padding:12px 24px;background:#4f46e5;color:#ffffff;border:none;font-size:15px;border-radius:8px;font-weight:600;box-shadow:0 4px 12px rgba(99,102,241,0.3);"><i class="fa-solid fa-rocket" style="margin-right:6px;"></i>Launch Campaign</button>
                    <div id="cold-status-actions" style="display:none; gap:8px;"></div>'''

if orig_vb_btns in text and orig_cold_btns in text:
    text = text.replace(orig_vb_btns, new_vb_btns)
    text = text.replace(orig_cold_btns, new_cold_btns)
    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('index.html updated successfully!')
else:
    print('Failed to find buttons in index.html!')
    print(orig_vb_btns in text)
    print(orig_cold_btns in text)
