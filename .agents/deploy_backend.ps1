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

# Read cleaned content
$localPath = "C:\Users\higan\.gemini\antigravity\brain\8f07062c-edf1-410d-9e87-c5879f537c35\scratch\main_cleaned.py"
$cleanContent = [System.IO.File]::ReadAllText($localPath, [System.Text.Encoding]::UTF8)

# Upload via cPanel API
$uri = "https://167.235.11.154:2083/execute/Fileman/save_file_content"
$body = @{
    dir = "/home/terapkco/xcomic_backend"
    file = "main.py"
    content = $cleanContent
}
try {
    $r = Invoke-RestMethod -Uri $uri -Headers $headers -Method POST -Body $body -TimeoutSec 30
    if ($r.status -eq 1) {
        Write-Output "SUCCESS: main.py uploaded and saved on server!"
    } else {
        Write-Output "Response: $($r | ConvertTo-Json -Depth 3)"
    }
} catch {
    Write-Output "Error: $($_.Exception.Message)"
}
