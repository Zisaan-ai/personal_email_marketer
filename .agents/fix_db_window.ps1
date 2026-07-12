Add-Type @"
using System.Net;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
public class TrustCerts7 {
    public static void Enable() {
        ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
    }
}
"@
[TrustCerts7]::Enable()
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$pair = "terapkco:(3#JCk2Vyn94hY"
$bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
$base64 = [Convert]::ToBase64String($bytes)
$headers = @{ Authorization = "Basic $base64" }

# Upload the Python fix script
$pythonScript = "import sqlite3`ndb_path = '/home/terapkco/xcomic_backend/sql_app.db'`nconn = sqlite3.connect(db_path)`ncur = conn.cursor()`ncur.execute('UPDATE sending_accounts SET send_window_start=0, send_window_end=24')`nconn.commit()`ncur.execute('SELECT email, send_window_start, send_window_end FROM sending_accounts')`nrows = cur.fetchall()`nfor r in rows: print(f'  {r[0]}: {r[1]}-{r[2]}')`nconn.close()`nprint('Done')"

$body = @{
    dir = "/home/terapkco/xcomic_backend"
    filename = "fix_window.py"
    content = $pythonScript
}
$result = Invoke-RestMethod -Uri "https://167.235.11.154:2083/execute/Fileman/save_file_content" -Method POST -Headers $headers -Body $body
Write-Host "Upload fix_window.py status: $($result.status) error: $($result.errors)"

# Try to execute via cPanel API - CPANEL::API2::ExecRaw
$execUri = "https://167.235.11.154:2083/execute/Shell/bash"
$execBody = "cmd=cd+/home/terapkco/xcomic_backend+%26%26+python3+fix_window.py"
try {
    $execResult = Invoke-RestMethod -Uri $execUri -Method POST -Headers $headers -Body $execBody
    Write-Host "Exec: $($execResult | ConvertTo-Json -Depth 3)"
} catch {
    Write-Host "Shell API error: $_"
}
