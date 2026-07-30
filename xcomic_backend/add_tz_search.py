import ftplib

ftp_host = "167.235.11.154"
ftp_user = "terapkco"
ftp_pass = "(3#JCk2Vyn94hY"

local_file = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_index_html.html"

with open(local_file, "r", encoding="utf-8") as f:
    content = f.read()

# Find and replace the script block to add keyboard arrow support
old_script_part = """    searchBox.addEventListener('input', function() { buildList(this.value); });"""

new_script_part = """    let activeIdx = -1;

    function highlightItem(idx) {
      const items = tzList.querySelectorAll('div[data-tz]');
      items.forEach((el, i) => {
        if (i === idx) {
          el.style.background = '#6366f120';
          el.style.fontWeight = '600';
          el.scrollIntoView({ block: 'nearest' });
        } else {
          el.style.background = '';
          el.style.fontWeight = '';
        }
      });
      activeIdx = idx;
    }

    searchBox.addEventListener('input', function() { activeIdx = -1; buildList(this.value); });

    searchBox.addEventListener('keydown', function(e) {
      const items = tzList.querySelectorAll('div[data-tz]');
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        activeIdx = Math.min(activeIdx + 1, items.length - 1);
        highlightItem(activeIdx);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        activeIdx = Math.max(activeIdx - 1, 0);
        highlightItem(activeIdx);
      } else if (e.key === 'Enter' && activeIdx >= 0 && activeIdx < items.length) {
        e.preventDefault();
        selectTZ(items[activeIdx].getAttribute('data-tz'));
      } else if (e.key === 'Escape') {
        closeDropdown();
      }
    });"""

if old_script_part in content:
    content = content.replace(old_script_part, new_script_part)
    print("✅ Added keyboard arrow navigation!")
else:
    print("❌ Could not find script part to replace")

# Also add data-tz attribute to each dropdown item so we can read it
old_div_create = """        const div = document.createElement('div');
        div.textContent = opt.value.replace(/_/g, ' ');
        const isSelected = opt.value === sel.value;
        div.style.cssText = 'padding:10px 16px; cursor:pointer; font-size:14px; color:var(--text,#333); transition:background 0.15s;'
          + (isSelected ? ' background:#6366f110; font-weight:600; color:#6366f1;' : '');
        div.onmouseenter = () => { if (!isSelected) div.style.background = '#f1f5f9'; };
        div.onmouseleave = () => { if (!isSelected) div.style.background = ''; };
        div.onmousedown = (e) => {
          e.preventDefault();
          selectTZ(opt.value);
        };"""

new_div_create = """        const div = document.createElement('div');
        div.textContent = opt.value.replace(/_/g, ' ');
        div.setAttribute('data-tz', opt.value);
        const isSelected = opt.value === sel.value;
        div.style.cssText = 'padding:10px 16px; cursor:pointer; font-size:14px; color:var(--text,#333); transition:background 0.15s;'
          + (isSelected ? ' background:#6366f110; font-weight:600; color:#6366f1;' : '');
        div.onmouseenter = () => { if (!isSelected) div.style.background = '#f1f5f9'; };
        div.onmouseleave = () => { if (!isSelected) div.style.background = ''; };
        div.onmousedown = (e) => {
          e.preventDefault();
          selectTZ(opt.value);
        };"""

if old_div_create in content:
    content = content.replace(old_div_create, new_div_create)
    print("✅ Added data-tz attribute to items!")
else:
    print("⚠️ Could not find div create block")

with open(local_file, "w", encoding="utf-8") as f:
    f.write(content)

try:
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)
    ftp.cwd("/xcomic.xyz")
    with open(local_file, "rb") as f:
        ftp.storbinary("STOR index.html", f)
    ftp.quit()
    print("✅ Uploaded! Ctrl+F5 করুন।")
    print("\n👉 এখন ড্রপডাউন ওপেন করে Arrow ↓↑ দিয়ে নেভিগেট করুন, Enter দিয়ে সিলেক্ট করুন!")
except Exception as e:
    print(f"❌ Upload failed: {e}")
