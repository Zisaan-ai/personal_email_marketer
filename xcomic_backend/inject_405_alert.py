import ftplib

ftp_host = "167.235.11.154"
ftp_user = "terapkco"
ftp_pass = "(3#JCk2Vyn94hY"

local_app = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_app_js.js"

with open(local_app, "r", encoding="utf-8") as f:
    app_content = f.read()

# Add logging to apiCall for 405 errors
old_api_call_end = """    const ct = res.headers.get('content-type');
    if (res.status === 401) {"""

new_api_call_end = """    if (res.status === 405) {
        alert("405 Error on: " + method + " " + endpoint + "\\nCampaign ID: " + window.currentCampaignId);
    }
    const ct = res.headers.get('content-type');
    if (res.status === 401) {"""

app_content = app_content.replace(old_api_call_end, new_api_call_end)

with open(local_app, "w", encoding="utf-8") as f:
    f.write(app_content)

try:
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)
    ftp.cwd("/xcomic.xyz/assets")
    with open(local_app, "rb") as f:
        ftp.storbinary("STOR app.js", f)
    ftp.quit()
    print("✅ Injected 405 debugger into app.js!")
except Exception as e:
    print(f"❌ Upload failed: {e}")
