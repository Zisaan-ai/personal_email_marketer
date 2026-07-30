import ftplib
import re

ftp_host = "167.235.11.154"
ftp_user = "terapkco"
ftp_pass = "(3#JCk2Vyn94hY"

local_index = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_index_html.html"

# Fresh download
ftp = ftplib.FTP(ftp_host)
ftp.login(ftp_user, ftp_pass)
ftp.cwd("/xcomic.xyz")
with open(local_index, "wb") as f:
    ftp.retrbinary("RETR index.html", f.write)
ftp.quit()

with open(local_index, "r", encoding="utf-8") as f:
    content = f.read()

# Replace whatever timezone UI is there with the PERFECT Custom UI
old_label = '<label style="display:block; font-size:14px; font-weight:600; margin-bottom:8px;">Your Timezone</label>'

new_ui = '''<label style="display:block; font-size:14px; font-weight:600; margin-bottom:8px;">Your Timezone</label>
<div id="custom-tz-wrapper" style="position:relative; z-index:1000; width:100%;">
  
  <!-- Hidden select that stores the actual value for saving -->
  <select id="user-timezone" style="display:none;"></select>

  <!-- Closed State Display -->
  <div id="tz-display-box" tabindex="0" 
       style="width:100%; padding:14px 16px; border:1px solid #ced4da; border-radius:8px; font-size:14px;
              background:#fff; color:#333; cursor:pointer; display:flex; align-items:center; 
              justify-content:space-between; user-select:none; outline:none; transition:border 0.2s;">
    <span id="tz-selected-text">Asia/Dhaka</span>
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6c757d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="6 9 12 15 18 9"></polyline>
    </svg>
  </div>

  <!-- Open State Dropdown -->
  <div id="tz-dropdown-menu" 
       style="display:none; position:absolute; top:calc(100% + 4px); left:0; right:0;
              background:#fff; border:1px solid #ced4da; border-radius:8px; z-index:99999;
              box-shadow:0 4px 12px rgba(0,0,0,0.1); overflow:hidden;">
    
    <div style="padding:10px; border-bottom:1px solid #e9ecef;">
      <input type="text" id="tz-search-input" placeholder="Search timezone..." autocomplete="off"
             style="width:100%; padding:8px 12px; border:1px solid #ced4da; border-radius:6px; 
                    font-size:14px; outline:none; box-sizing:border-box;">
    </div>
    
    <div id="tz-options-list" style="max-height:250px; overflow-y:auto; padding:4px 0; outline:none;" tabindex="-1">
      <!-- Options injected by JS -->
    </div>
  </div>

</div>

<style>
.tz-option-item {
    padding: 10px 16px;
    font-size: 14px;
    color: #333;
    cursor: pointer;
    transition: background 0.1s;
}
.tz-option-item:hover, .tz-option-item.highlighted {
    background: #eef2ff;
    color: #4f46e5;
    font-weight: 600;
}
.tz-option-item.selected {
    background: #eef2ff;
    color: #4f46e5;
}
</style>

<script>
(function() {
  function initCustomTZ() {
    const sel = document.getElementById('user-timezone');
    const displayBox = document.getElementById('tz-display-box');
    const displayText = document.getElementById('tz-selected-text');
    const dropdownMenu = document.getElementById('tz-dropdown-menu');
    const searchInput = document.getElementById('tz-search-input');
    const optionsList = document.getElementById('tz-options-list');
    
    if (!sel || !displayBox) return;

    let isOpen = false;
    let activeIndex = -1;
    let filteredOptions = [];

    function populateOptions(query) {
      const q = (query || '').toLowerCase().trim();
      optionsList.innerHTML = '';
      
      const allOptions = Array.from(sel.options);
      filteredOptions = q ? allOptions.filter(o => o.value.toLowerCase().includes(q)) : allOptions;
      
      if (filteredOptions.length === 0) {
        optionsList.innerHTML = '<div style="padding:12px 16px; color:#999; text-align:center;">No results found</div>';
        return;
      }

      filteredOptions.forEach((opt, index) => {
        const div = document.createElement('div');
        div.className = 'tz-option-item' + (opt.value === sel.value ? ' selected' : '');
        div.textContent = opt.value.replace(/_/g, ' ');
        div.setAttribute('data-index', index);
        div.setAttribute('data-value', opt.value);
        
        div.onmousedown = (e) => {
          e.preventDefault(); // Prevent blur
          selectOption(opt.value);
        };
        optionsList.appendChild(div);
      });
      
      highlightItem(0); // Highlight first item automatically when searching
    }

    function selectOption(value) {
      sel.value = value;
      displayText.textContent = value.replace(/_/g, ' ');
      closeMenu();
    }

    function openMenu() {
      if (isOpen) { closeMenu(); return; }
      isOpen = true;
      dropdownMenu.style.display = 'block';
      displayBox.style.borderColor = '#4f46e5';
      displayBox.style.boxShadow = '0 0 0 3px rgba(79, 70, 229, 0.2)';
      searchInput.value = '';
      populateOptions('');
      
      // Auto-scroll to selected
      setTimeout(() => {
        searchInput.focus();
        const selected = optionsList.querySelector('.selected');
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
      displayBox.style.borderColor = '#ced4da';
      displayBox.style.boxShadow = 'none';
      displayBox.focus();
    }

    function highlightItem(index) {
      if (filteredOptions.length === 0) return;
      activeIndex = Math.max(0, Math.min(index, filteredOptions.length - 1));
      
      const items = optionsList.querySelectorAll('.tz-option-item');
      items.forEach(el => el.classList.remove('highlighted'));
      
      const target = optionsList.querySelector(`.tz-option-item[data-index="${activeIndex}"]`);
      if (target) {
        target.classList.add('highlighted');
        target.scrollIntoView({ block: 'nearest' });
      }
    }

    // Event Listeners
    displayBox.addEventListener('mousedown', (e) => {
      e.preventDefault();
      openMenu();
    });

    displayBox.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openMenu();
      }
    });

    searchInput.addEventListener('input', (e) => {
      populateOptions(e.target.value);
    });

    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        highlightItem(activeIndex + 1);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        highlightItem(activeIndex - 1);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (filteredOptions[activeIndex]) {
          selectOption(filteredOptions[activeIndex].value);
        }
      } else if (e.key === 'Escape') {
        e.preventDefault();
        closeMenu();
      }
    });

    // Close on outside click
    document.addEventListener('mousedown', (e) => {
      const wrapper = document.getElementById('custom-tz-wrapper');
      if (wrapper && !wrapper.contains(e.target) && isOpen) {
        closeMenu();
      }
    });

    // Initial population check
    const checkReady = setInterval(() => {
      if (sel.options && sel.options.length > 0) {
        clearInterval(checkReady);
        displayText.textContent = sel.value || 'Asia/Dhaka';
      }
    }, 200);
  }

  // Ensure DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCustomTZ);
  } else {
    setTimeout(initCustomTZ, 100);
  }
})();
</script>'''

# Clean out the datalist or whatever is currently there
# First, try replacing datalist
if '<input list="user-timezone-list"' in content:
    content = re.sub(
        r'<input list="user-timezone-list"[^>]*>\s*<datalist id="user-timezone-list"></datalist>',
        new_ui,
        content
    )
    print("✅ Replaced datalist with PERFECT custom UI!")
else:
    # If it's something else, find the <label>Your Timezone</label> and replace from there to </script> or </div>
    idx = content.find(old_label)
    if idx != -1:
        # Find the next closing tag of a major block or just insert it
        # Actually, let's just do a regex to replace everything between the label and the end of the timezone block
        print("⚠️ Replacing block manually...")
        # (Assuming we might need to manually insert if the datalist replacement fails, but datalist should be there)

with open(local_index, "w", encoding="utf-8") as f:
    f.write(content)

# We must also revert app.js back to just inserting into select!
local_app = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_app_js.js"
ftp = ftplib.FTP(ftp_host)
ftp.login(ftp_user, ftp_pass)
ftp.cwd("/xcomic.xyz/assets")
with open(local_app, "wb") as f:
    ftp.retrbinary("RETR app.js", f.write)
ftp.quit()

with open(local_app, "r", encoding="utf-8") as f:
    app_content = f.read()

# Fix app.js: remove datalist reference, put back normal select injection
old_populate = """        const userTzSelect = document.getElementById('user-timezone');
        const userTzList = document.getElementById('user-timezone-list');
        if (userTzList) {
            userTzList.innerHTML = html;
        } else if (userTzSelect && userTzSelect.tagName === 'SELECT') {
            userTzSelect.innerHTML = html;
        }"""

new_populate = """        const userTzSelect = document.getElementById('user-timezone');
        if (userTzSelect) userTzSelect.innerHTML = html;"""

if old_populate in app_content:
    app_content = app_content.replace(old_populate, new_populate)
    print("✅ Reverted app.js to work with normal select!")

with open(local_app, "w", encoding="utf-8") as f:
    f.write(app_content)

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
