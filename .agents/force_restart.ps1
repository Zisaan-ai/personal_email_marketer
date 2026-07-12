Add-Type @"
using System.Net;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
public class TrustCerts6 {
    public static void Enable() {
        ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
    }
}
"@
[TrustCerts6]::Enable()
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$pair = "terapkco:(3#JCk2Vyn94hY"
$bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
$base64 = [Convert]::ToBase64String($bytes)
$headers = @{ Authorization = "Basic $base64" }
$uri = "https://167.235.11.154:2083/execute/Fileman/save_file_content"

# Add a random comment to passenger_wsgi.py to force Passenger to notice the change
$passengerPath = "C:\Users\higan\.antigravity-ide\personal_email_marketer\backend\passenger_wsgi.py"
$passengerContent = [System.IO.File]::ReadAllText($passengerPath, [System.Text.Encoding]::UTF8)
$passengerContent = $passengerContent + "`n# Trigger restart $(Get-Date -Format 'HH:mm:ss')"
[System.IO.File]::WriteAllText($passengerPath, $passengerContent)

Write-Output "Uploading passenger_wsgi.py to force restart..."
$body = @{
    dir = "/home/terapkco/xcomic_backend"
    file = "passenger_wsgi.py"
    content = $passengerContent
}
$r = Invoke-RestMethod -Uri $uri -Headers $headers -Method POST -Body $body -TimeoutSec 30
if ($r.status -eq 1) {
    Write-Output "SUCCESS: passenger_wsgi.py modified and uploaded!"
} else {
    Write-Output "FAILED to upload passenger_wsgi.py: $($r | ConvertTo-Json -Depth 3)"
}

Write-Output "Attempting to create tmp/restart.txt as well..."
# Creating a folder via Fileman if it doesn't exist requires UAPI, but let's just write restart.txt
$restartBody = @{
    dir = "/home/terapkco/xcomic_backend/tmp"
    file = "restart.txt"
    content = "restart $(Get-Date)"
}
try {
    $r2 = Invoke-RestMethod -Uri $uri -Headers $headers -Method POST -Body $restartBody -TimeoutSec 30
    if ($r2.status -eq 1) {
        Write-Output "SUCCESS: tmp/restart.txt updated!"
    } else {
        Write-Output "FAILED tmp/restart.txt: $($r2 | ConvertTo-Json -Depth 3)"
    }
} catch {
    Write-Output "Error: $($_.Exception.Message)"
}
