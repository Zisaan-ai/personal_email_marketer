Add-Type @"
using System.Net;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
public class TrustCerts4 {
    public static void Enable() {
        ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
    }
}
"@
[TrustCerts4]::Enable()
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$pair = "terapkco:(3#JCk2Vyn94hY"
$bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
$base64 = [Convert]::ToBase64String($bytes)
$headers = @{ Authorization = "Basic $base64" }
$uri = "https://167.235.11.154:2083/execute/Fileman/save_file_content"

$filesToUpload = @(
    @{ Local = "C:\Users\higan\.antigravity-ide\personal_email_marketer\frontend\index.html"; RemoteDir = "/home/terapkco/xcomic.xyz"; RemoteFile = "index.html" },
    @{ Local = "C:\Users\higan\.antigravity-ide\personal_email_marketer\frontend\assets\app.js"; RemoteDir = "/home/terapkco/xcomic.xyz/assets"; RemoteFile = "app.js" },
    @{ Local = "C:\Users\higan\.antigravity-ide\personal_email_marketer\frontend\assets\sending_accounts.js"; RemoteDir = "/home/terapkco/xcomic.xyz/assets"; RemoteFile = "sending_accounts.js" },
    @{ Local = "C:\Users\higan\.antigravity-ide\personal_email_marketer\backend\main.py"; RemoteDir = "/home/terapkco/xcomic_backend"; RemoteFile = "main.py" },
    @{ Local = "C:\Users\higan\.antigravity-ide\personal_email_marketer\backend\email_service.py"; RemoteDir = "/home/terapkco/xcomic_backend"; RemoteFile = "email_service.py" },
    @{ Local = "C:\Users\higan\.antigravity-ide\personal_email_marketer\backend\passenger_wsgi.py"; RemoteDir = "/home/terapkco/xcomic_backend"; RemoteFile = "passenger_wsgi.py" },
    @{ Local = "C:\Users\higan\.antigravity-ide\personal_email_marketer\backend\database.py"; RemoteDir = "/home/terapkco/xcomic_backend"; RemoteFile = "database.py" },
    @{ Local = "C:\Users\higan\.antigravity-ide\personal_email_marketer\backend\health_monitor.py"; RemoteDir = "/home/terapkco/xcomic_backend"; RemoteFile = "health_monitor.py" },
    @{ Local = "C:\Users\higan\.antigravity-ide\personal_email_marketer\backend\domain_checker.py"; RemoteDir = "/home/terapkco/xcomic_backend"; RemoteFile = "domain_checker.py" },
    @{ Local = "C:\Users\higan\.antigravity-ide\personal_email_marketer\backend\bounce_processor.py"; RemoteDir = "/home/terapkco/xcomic_backend"; RemoteFile = "bounce_processor.py" }
)

foreach ($f in $filesToUpload) {
    Write-Output "Uploading $($f.RemoteFile)..."
    $cleanContent = [System.IO.File]::ReadAllText($f.Local, [System.Text.Encoding]::UTF8)
    $body = @{
        dir = $f.RemoteDir
        file = $f.RemoteFile
        content = $cleanContent
    }
    try {
        $r = Invoke-RestMethod -Uri $uri -Headers $headers -Method POST -Body $body -TimeoutSec 30
        if ($r.status -eq 1) {
            Write-Output "SUCCESS: $($f.RemoteFile) uploaded!"
        } else {
            Write-Output "FAILED: $($f.RemoteFile) - Response: $($r | ConvertTo-Json -Depth 3)"
        }
    } catch {
        Write-Output "Error uploading $($f.RemoteFile): $($_.Exception.Message)"
    }
}
Write-Output "Restarting Python App via Passenger..."
try {
    # We touch the passenger_wsgi.py to restart the app
    # Or just hit the restart endpoint if there is one. We will touch the tmp/restart.txt
    $restartUri = "https://167.235.11.154:2083/execute/Fileman/save_file_content"
    $restartBody = @{
        dir = "/home/terapkco/xcomic_backend/tmp"
        file = "restart.txt"
        content = "restart"
    }
    $r2 = Invoke-RestMethod -Uri $restartUri -Headers $headers -Method POST -Body $restartBody -TimeoutSec 30
    if ($r2.status -eq 1) {
        Write-Output "SUCCESS: App restarted successfully!"
    }
} catch {
    Write-Output "Error restarting app: $($_.Exception.Message)"
}
