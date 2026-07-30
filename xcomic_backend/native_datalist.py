import ftplib
import re

ftp_host = "167.235.11.154"
ftp_user = "terapkco"
ftp_pass = "(3#JCk2Vyn94hY"

local_index = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_index_html.html"

# Download fresh index.html
ftp = ftplib.FTP(ftp_host)
ftp.login(ftp_user, ftp_pass)
ftp.cwd("/xcomic.xyz")
with open(local_index, "wb") as f:
    ftp.retrbinary("RETR index.html", f.write)
ftp.quit()

with open(local_index, "r", encoding="utf-8") as f:
    content = f.read()

# We will replace the <select id="user-timezone"> with an input + datalist
old_select_pattern = re.compile(r'<select class="form-control" id="user-timezone"[^>]*></select>')

new_ui = '''<input list="user-timezone-list" id="user-timezone" class="form-control" style="width:100%; padding:14px 16px; border:2px solid var(--border); border-radius:12px; font-size:14px; background:var(--bg); color:var(--text);" placeholder="Type to search timezone... (e.g. Asia/Dhaka)">
<datalist id="user-timezone-list"></datalist>'''

if old_select_pattern.search(content):
    content = old_select_pattern.sub(new_ui, content)
    print("✅ Replaced select with native searchable datalist!")
elif '<select id="user-timezone"' in content:
    # Fallback if class is missing
    content = re.sub(r'<select id="user-timezone"[^>]*></select>', new_ui, content)
    print("✅ Replaced select with native searchable datalist (fallback match)!")
else:
    print("❌ Could not find user-timezone select!")
    exit(1)

with open(local_index, "w", encoding="utf-8") as f:
    f.write(content)

# Now we need to update app.js to populate the datalist instead of select
local_app = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_app_js.js"
ftp = ftplib.FTP(ftp_host)
ftp.login(ftp_user, ftp_pass)
ftp.cwd("/xcomic.xyz/assets")
with open(local_app, "wb") as f:
    ftp.retrbinary("RETR app.js", f.write)
ftp.quit()

with open(local_app, "r", encoding="utf-8") as f:
    app_content = f.read()

# Update populateTimezones in app.js
old_populate = """        const userTzSelect = document.getElementById('user-timezone');
        if (userTzSelect) userTzSelect.innerHTML = html;
        if (typeof Choices !== 'undefined') {
            if (userTzSelect) {
                try {
                    if (userTzSelect.choicesInstance) userTzSelect.choicesInstance.destroy();
                    userTzSelect.choicesInstance = new Choices(userTzSelect, { searchEnabled: true, itemSelectText: '', shouldSort: false });
                } catch(e) {}
            }
        }"""

new_populate = """        const userTzSelect = document.getElementById('user-timezone');
        const userTzList = document.getElementById('user-timezone-list');
        if (userTzList) {
            userTzList.innerHTML = html;
        } else if (userTzSelect && userTzSelect.tagName === 'SELECT') {
            userTzSelect.innerHTML = html;
        }"""

if old_populate in app_content:
    app_content = app_content.replace(old_populate, new_populate)
    print("✅ Updated app.js to populate datalist!")
else:
    # Try alternate match if the exact string differs
    print("⚠️ Exact app.js block not found, doing generic replace...")
    app_content = app_content.replace(
        "if (userTzSelect) userTzSelect.innerHTML = html;", 
        "if (document.getElementById('user-timezone-list')) document.getElementById('user-timezone-list').innerHTML = html; else if (userTzSelect) userTzSelect.innerHTML = html;"
    )

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
    print("✅ Successfully uploaded both files! (index.html & app.js)")
except Exception as e:
    print(f"❌ Upload failed: {e}")
