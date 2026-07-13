Add-Type @"
using System.Net;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
public class TrustCerts5 {
    public static void Enable() {
        ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
    }
}
"@
[TrustCerts5]::Enable()
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$pair = "terapkco:(3#JCk2Vyn94hY"
$bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
$base64 = [Convert]::ToBase64String($bytes)
$headers = @{ Authorization = "Basic $base64" }

# First, let's list existing cron jobs to make sure we don't add duplicates
$listUri = "https://167.235.11.154:2083/execute/Cron/list_cron"
$listR = Invoke-RestMethod -Uri $listUri -Headers $headers -Method GET
$exists = $false

if ($listR.status -eq 1) {
    foreach ($cron in $listR.data) {
        if ($cron.command -match "api/cron/run") {
            Write-Output "Cron job already exists!"
            $exists = $true
            break
        }
    }
}

if (-not $exists) {
    $addUri = "https://167.235.11.154:2083/execute/Cron/add_line"
    $body = @{
        command = "curl -s https://xcomic.xyz/api/cron/run > /dev/null 2>&1"
        day = "*"
        hour = "*"
        minute = "*"
        month = "*"
        weekday = "*"
    }
    
    $r = Invoke-RestMethod -Uri $addUri -Headers $headers -Method POST -Body $body
    if ($r.status -eq 1) {
        Write-Output "SUCCESS: Cron job added successfully!"
    } else {
        Write-Output "FAILED to add cron job: $($r | ConvertTo-Json -Depth 3)"
    }
}
