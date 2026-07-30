import ftplib

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

# Remove the custom tz-picker-wrapper and put back a clean select
start_idx = content.find('<div id="tz-picker-wrapper"')
if start_idx != -1:
    end_script = content.find('</script>', start_idx)
    if end_script != -1:
        # We need to find the exact end of the block.
        # The block we added ends with:
        #     // Close when clicking outside
        # ...
        #     }, 200);
        # })();
        # </script>
        # Just replace the whole chunk from <div id="tz-picker-wrapper" to </script>
        chunk = content[start_idx:end_script + 9]
        clean_select = '<select class="form-control" id="user-timezone" style="width:100%;"></select>'
        content = content.replace(chunk, clean_select)
        print("✅ Reverted custom UI to clean select for Choices.js!")
else:
    print("⚠️ tz-picker-wrapper not found. Maybe already reverted?")
    if 'id="user-timezone"' in content:
        print("Select tag already exists.")

# Write back index.html
with open(local_index, "w", encoding="utf-8") as f:
    f.write(content)

# Upload index.html
try:
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)
    ftp.cwd("/xcomic.xyz")
    with open(local_index, "rb") as f:
        ftp.storbinary("STOR index.html", f)
    ftp.quit()
    print("✅ Uploaded clean index.html!")
except Exception as e:
    print(f"❌ Upload failed: {e}")
