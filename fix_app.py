import sys

with open('frontend/assets/app_v2.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''        let html = '';
        accounts.forEach(acc => {
            const isChecked = selectedIds.includes(acc.id) ? 'checked' : '';
            html += 
                <label style="display:flex; align-items:center; gap:8px; cursor:pointer; font-size:13px; padding:4px 0;">
                    <input type="checkbox" class="sender-acc-checkbox" value=" + "" + "  + "" + >
                    <div>
                        <div style="font-weight:600; color:var(--p);"> + "" + </div>
                        <div style="color:var(--text-muted); font-size:11px;"> + "" + </div>
                    </div>
                </label>
            ;
        });
        container.innerHTML = html;'''

new_code = '''        let html = 
            <div style="margin-bottom:10px; position:relative;">
                <i class="fa-solid fa-search" style="position:absolute; left:10px; top:10px; color:var(--text-muted); font-size:12px;"></i>
                <input type="text" placeholder="Search accounts by name or email..." onkeyup="filterAccounts(this, '')" style="width:100%; padding:8px 8px 8px 30px; font-size:13px; border:1px solid var(--border); border-radius:4px; background:var(--bg); color:var(--text); outline:none; box-sizing:border-box;">
            </div>
            <div class="accounts-list-scroll" style="max-height:160px; overflow-y:auto; padding-right:5px;">
        ;
        accounts.forEach(acc => {
            const isChecked = selectedIds.includes(acc.id) ? 'checked' : '';
            const searchStr = ((acc.name||'') + ' ' + (acc.email||'')).toLowerCase().replace(/'/g, "");
            html += 
                <label class="account-item-lbl" data-search=" + "" + " style="display:flex; align-items:center; gap:8px; cursor:pointer; font-size:13px; padding:6px; border-radius:4px; transition:background 0.2s;" onmouseover="this.style.background='rgba(0,0,0,0.03)'" onmouseout="this.style.background='transparent'">
                    <input type="checkbox" class="sender-acc-checkbox" value=" + "" + "  + "" + >
                    <div>
                        <div style="font-weight:600; color:var(--p);"> + "" + </div>
                        <div style="color:var(--text-muted); font-size:11px;"> + "" + </div>
                    </div>
                </label>
            ;
        });
        html += '</div>';
        container.innerHTML = html;'''

content = content.replace(old_code, new_code)
content = content.replace(old_code.replace('\n', '\r\n'), new_code)

with open('frontend/assets/app_v2.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
