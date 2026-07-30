import ftplib

ftp_host = "167.235.11.154"
ftp_user = "terapkco"
ftp_pass = "(3#JCk2Vyn94hY"

local_app = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_app_js.js"

# Download app.js
ftp = ftplib.FTP(ftp_host)
ftp.login(ftp_user, ftp_pass)
ftp.cwd("/xcomic.xyz/assets")
with open(local_app, "wb") as f:
    ftp.retrbinary("RETR app.js", f.write)
ftp.quit()
print("✅ Downloaded fresh app.js")

with open(local_app, "r", encoding="utf-8") as f:
    content = f.read()

custom_tz_script = """
// --- PERFECT CUSTOM TIMEZONE PICKER ---
function upgradeToCustomTZPicker(selectId) {
    const sel = document.getElementById(selectId);
    if (!sel || sel.tagName !== 'SELECT' || sel.dataset.customTzInit) return;
    sel.dataset.customTzInit = "1";
    sel.style.display = 'none';

    const wrapper = document.createElement('div');
    wrapper.id = selectId + '-wrapper';
    wrapper.style.cssText = 'position:relative; z-index:1000; width:100%; font-family:inherit;';

    const displayBox = document.createElement('div');
    displayBox.id = selectId + '-display';
    displayBox.tabIndex = 0;
    displayBox.style.cssText = 'width:100%; padding:14px 16px; border:2px solid var(--border, #e2e8f0); border-radius:12px; font-size:14px; background:var(--bg, #fff); color:var(--text, #333); cursor:pointer; display:flex; align-items:center; justify-content:space-between; user-select:none; outline:none; transition:all 0.2s;';

    const displayText = document.createElement('span');
    displayText.id = selectId + '-selected-text';
    displayText.style.fontWeight = '500';
    displayText.textContent = (sel.value || 'Asia/Dhaka').replace(/_/g, ' ');

    const svgIcon = document.createElement('div');
    svgIcon.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>';
    svgIcon.style.cssText = 'display:flex; align-items:center; color:var(--text-muted, #64748b);';

    displayBox.appendChild(displayText);
    displayBox.appendChild(svgIcon);

    const dropdownMenu = document.createElement('div');
    dropdownMenu.style.cssText = 'display:none; position:absolute; top:calc(100% + 6px); left:0; right:0; background:var(--card, #fff); border:2px solid var(--border, #e2e8f0); border-radius:14px; z-index:99999; box-shadow:0 20px 60px rgba(0,0,0,0.15); overflow:hidden;';

    const searchContainer = document.createElement('div');
    searchContainer.style.cssText = 'padding:12px; border-bottom:1px solid var(--border, #e2e8f0);';

    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = 'Search timezone...';
    searchInput.autocomplete = 'off';
    searchInput.style.cssText = 'width:100%; padding:10px 14px; border:2px solid var(--border, #e2e8f0); border-radius:10px; font-size:14px; outline:none; background:var(--bg, #f8fafc); color:var(--text, #333); box-sizing:border-box; transition:border 0.2s;';
    searchInput.onfocus = () => searchInput.style.borderColor = '#6366f1';
    searchInput.onblur = () => searchInput.style.borderColor = '';

    searchContainer.appendChild(searchInput);

    const optionsList = document.createElement('div');
    optionsList.style.cssText = 'max-height:240px; overflow-y:auto; padding:4px 0; outline:none;';
    optionsList.tabIndex = -1;

    dropdownMenu.appendChild(searchContainer);
    dropdownMenu.appendChild(optionsList);

    wrapper.appendChild(displayBox);
    wrapper.appendChild(dropdownMenu);
    
    sel.parentNode.insertBefore(wrapper, sel.nextSibling);

    let isOpen = false;
    let activeIndex = -1;
    let filteredOptions = [];

    function populateOptions(query) {
      const q = (query || '').toLowerCase().trim();
      optionsList.innerHTML = '';
      
      const allOptions = Array.from(sel.options);
      filteredOptions = q ? allOptions.filter(o => o.value.toLowerCase().includes(q)) : allOptions;
      
      if (filteredOptions.length === 0) {
        optionsList.innerHTML = '<div style="padding:14px 16px; color:#94a3b8; font-size:14px; text-align:center;">No timezone found</div>';
        return;
      }

      filteredOptions.forEach((opt, index) => {
        const div = document.createElement('div');
        const isSelected = opt.value === sel.value;
        div.className = 'custom-tz-item';
        div.textContent = opt.value.replace(/_/g, ' ');
        div.setAttribute('data-index', index);
        div.style.cssText = 'padding:10px 16px; cursor:pointer; font-size:14px; color:var(--text, #333); transition:background 0.1s;' + 
                            (isSelected ? ' background:#6366f115; font-weight:600; color:#6366f1;' : '');
        
        div.onmouseenter = () => { if (!isSelected) div.style.background = 'var(--bg, #f1f5f9)'; };
        div.onmouseleave = () => { if (!isSelected) div.style.background = ''; };
        div.onmousedown = (e) => {
          e.preventDefault();
          selectOption(opt.value);
        };
        optionsList.appendChild(div);
      });
      highlightItem(0);
    }

    function selectOption(value) {
      sel.value = value;
      displayText.textContent = value.replace(/_/g, ' ');
      // Also trigger change event for native select in case app relies on it
      sel.dispatchEvent(new Event('change', { bubbles: true }));
      closeMenu();
    }

    function openMenu() {
      if (isOpen) { closeMenu(); return; }
      isOpen = true;
      dropdownMenu.style.display = 'block';
      displayBox.style.borderColor = '#6366f1';
      searchInput.value = '';
      populateOptions('');
      
      setTimeout(() => {
        searchInput.focus();
        const selected = optionsList.querySelector('.custom-tz-item[style*="font-weight: 600"]');
        if (selected) {
          activeIndex = parseInt(selected.getAttribute('data-index') || 0);
          highlightItem(activeIndex);
          selected.scrollIntoView({ block: 'nearest' });
        }
      }, 50);
    }

    function closeMenu() {
      isOpen = false;
      dropdownMenu.style.display = 'none';
      displayBox.style.borderColor = '';
      displayBox.focus();
    }

    function highlightItem(index) {
      if (filteredOptions.length === 0) return;
      activeIndex = Math.max(0, Math.min(index, filteredOptions.length - 1));
      const items = optionsList.querySelectorAll('.custom-tz-item');
      items.forEach(el => {
         if(!el.style.cssText.includes('font-weight: 600')) {
             el.style.background = '';
         }
      });
      const target = optionsList.querySelector(`.custom-tz-item[data-index="${activeIndex}"]`);
      if (target) {
        if(!target.style.cssText.includes('font-weight: 600')) target.style.background = 'var(--bg, #f1f5f9)';
        target.scrollIntoView({ block: 'nearest' });
      }
    }

    displayBox.addEventListener('mousedown', (e) => { e.preventDefault(); openMenu(); });
    displayBox.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openMenu(); } });
    
    searchInput.addEventListener('input', (e) => populateOptions(e.target.value));
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown') { e.preventDefault(); highlightItem(activeIndex + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); highlightItem(activeIndex - 1); }
      else if (e.key === 'Enter') { 
          e.preventDefault(); 
          if (filteredOptions[activeIndex]) selectOption(filteredOptions[activeIndex].value); 
      }
      else if (e.key === 'Escape') { e.preventDefault(); closeMenu(); }
    });

    document.addEventListener('mousedown', (e) => {
      if (wrapper && !wrapper.contains(e.target) && isOpen) closeMenu();
    });

    // Keep display text in sync if sel value changes programmatically
    sel.addEventListener('change', () => {
        displayText.textContent = sel.value.replace(/_/g, ' ');
    });
}
// ----------------------------------------
"""

# Insert the function at the top of app.js
if 'function upgradeToCustomTZPicker' not in content:
    content = custom_tz_script + "\n" + content
    print("✅ Injected custom timezone JS function!")

# Replace the Choices.js block in populateTimezones
choices_block = """        if (typeof Choices !== 'undefined') {
            if (schTimezone) {
                new Choices(schTimezone, {
                    searchEnabled: true,
                    itemSelectText: '',
                    shouldSort: false
                });
            }
            if (vbSchTimezone) {
                new Choices(vbSchTimezone, {
                    searchEnabled: true,
                    itemSelectText: '',
                    shouldSort: false
                });
            }
        }"""

new_block = """        // Automatically upgrade all timezones to the Perfect Custom UI!
        if (schTimezone) upgradeToCustomTZPicker('sch-timezone');
        if (vbSchTimezone) upgradeToCustomTZPicker('vb-sch-timezone');
        if (userTzSelect) upgradeToCustomTZPicker('user-timezone');"""

if choices_block in content:
    content = content.replace(choices_block, new_block)
    print("✅ Replaced Choices.js with global custom UI upgrade!")
else:
    print("⚠️ Choices block not found, doing generic replace...")
    # Just append it after userTzSelect assignment
    old_assign = "if (userTzSelect) userTzSelect.innerHTML = html;"
    new_assign = old_assign + "\n" + new_block
    if old_assign in content:
        content = content.replace(old_assign, new_assign)
        print("✅ Added upgrade calls generically!")

with open(local_app, "w", encoding="utf-8") as f:
    f.write(content)

# Remove the hardcoded UI from index.html since app.js handles it dynamically now!
local_index = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_index_html.html"
ftp = ftplib.FTP(ftp_host)
ftp.login(ftp_user, ftp_pass)
ftp.cwd("/xcomic.xyz")
with open(local_index, "wb") as f:
    ftp.retrbinary("RETR index.html", f.write)
ftp.quit()
print("✅ Downloaded fresh index.html")

with open(local_index, "r", encoding="utf-8") as f:
    index_content = f.read()

# Replace hardcoded UI back to simple select
hardcoded_start = '<div id="custom-tz-wrapper"'
hardcoded_end = '</script>'
if hardcoded_start in index_content:
    s_idx = index_content.find(hardcoded_start)
    e_idx = index_content.find(hardcoded_end, s_idx)
    if e_idx != -1:
        chunk = index_content[s_idx:e_idx + len(hardcoded_end)]
        index_content = index_content.replace(chunk, '<select id="user-timezone" style="display:none;"></select>')
        print("✅ Cleaned hardcoded UI from index.html (app.js handles it now)!")

with open(local_index, "w", encoding="utf-8") as f:
    f.write(index_content)

# Upload both
try:
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)
    ftp.cwd("/xcomic.xyz")
    with open(local_index, "rb") as f:
        ftp.storbinary("STOR index.html", f)
    ftp.cwd("assets")
    with open(local_app, "rb") as f:
        ftp.storbinary("STOR app.js", f)
    ftp.quit()
    print("✅ Uploaded everything! Ctrl+F5 করুন।")
except Exception as e:
    print(f"❌ Upload failed: {e}")
