import ftplib

ftp_host = "167.235.11.154"
ftp_user = "terapkco"
ftp_pass = "(3#JCk2Vyn94hY"

local_app = r"C:\Users\higan\.gemini\antigravity\scratch\github_sync\live_app_js.js"

with open(local_app, "r", encoding="utf-8") as f:
    app_content = f.read()

# Replace the generic catch block with one that shows the exact error message
old_catch1 = """        } catch(e) {

            showToast('Error saving schedule', 'error');

        }"""

new_catch1 = """        } catch(e) {
            console.error('Save Schedule Error:', e);
            showToast('Error: ' + e.message, 'error');
        }"""

old_catch2 = """        } catch(e) {

            showToast('Error saving schedule', 'error');

        }"""

new_catch2 = """        } catch(e) {
            console.error('Save Schedule Error:', e);
            showToast('Error: ' + e.message, 'error');
        }"""
        
app_content = app_content.replace("showToast('Error saving schedule', 'error');", "console.error('Save Schedule Error:', e); showToast('Error: ' + e.message, 'error');")

with open(local_app, "w", encoding="utf-8") as f:
    f.write(app_content)

# Upload app.js
try:
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)
    ftp.cwd("/xcomic.xyz/assets")
    with open(local_app, "rb") as f:
        ftp.storbinary("STOR app.js", f)
    ftp.quit()
    print("✅ Uploaded app.js with better error messages!")
except Exception as e:
    print(f"❌ Upload failed: {e}")
