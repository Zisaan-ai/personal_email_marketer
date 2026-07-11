Add-Type @"
using System.Net;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
public class TrustCertsAll {
    public static void Enable() {
        ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
    }
}
"@
[TrustCertsAll]::Enable()
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$pair = "terapkco:(3#JCk2Vyn94hY"
$bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
$base64 = [Convert]::ToBase64String($bytes)
$headers = @{ Authorization = "Basic $base64" }

$uri = "https://167.235.11.154:2083/execute/Fileman/save_file_content"

# Map of local paths to remote paths
$files = @(
    @{ local="backend\database.py"; remoteDir="/home/terapkco/xcomic_backend"; remoteFile="database.py" },
    @{ local="backend\main.py"; remoteDir="/home/terapkco/xcomic_backend"; remoteFile="main.py" },
    @{ local="backend\health_monitor.py"; remoteDir="/home/terapkco/xcomic_backend"; remoteFile="health_monitor.py" },
    @{ local="backend\domain_checker.py"; remoteDir="/home/terapkco/xcomic_backend"; remoteFile="domain_checker.py" },
    @{ local="backend\bounce_processor.py"; remoteDir="/home/terapkco/xcomic_backend"; remoteFile="bounce_processor.py" },
    @{ local="frontend\index.html"; remoteDir="/home/terapkco/public_html"; remoteFile="index.html" },
    @{ local="frontend\assets\app.js"; remoteDir="/home/terapkco/public_html/assets"; remoteFile="app.js" },
    @{ local="frontend\assets\sending_accounts.js"; remoteDir="/home/terapkco/public_html/assets"; remoteFile="sending_accounts.js" }
)

foreach ($file in $files) {
    try {
        $content = [System.IO.File]::ReadAllText($file.local, [System.Text.Encoding]::UTF8)
        
        # NOTE: cPanel's save_file_content API doesn't auto-create files well if they don't exist.
        # We might need to ensure the file exists or use upload_files. 
        # But let's try save_file_content first as it works for existing.
        
        $body = @{
            dir = $file.remoteDir
            file = $file.remoteFile
            content = $content
        }
        
        $r = Invoke-RestMethod -Uri $uri -Headers $headers -Method POST -Body $body -TimeoutSec 30
        if ($r.status -eq 1) {
            Write-Output "SUCCESS: $($file.remoteFile) uploaded to $($file.remoteDir)!"
        } else {
            Write-Output "FAILED: $($file.remoteFile) - Response: $($r | ConvertTo-Json -Depth 3)"
            
            # If it failed, it might be because the file doesn't exist. Let's try creating it empty first, then saving.
            $createUri = "https://167.235.11.154:2083/execute/Fileman/file_op"
            $createBody = @{
                op = "create"
                sourcefiles = $file.remoteFile
                destfiles = $file.remoteDir
            }
            Invoke-RestMethod -Uri $createUri -Headers $headers -Method POST -Body $createBody -TimeoutSec 30 | Out-Null
            
            # Try saving again
            $r2 = Invoke-RestMethod -Uri $uri -Headers $headers -Method POST -Body $body -TimeoutSec 30
            if ($r2.status -eq 1) {
                Write-Output "SUCCESS (after create): $($file.remoteFile) uploaded!"
            } else {
                Write-Output "FAILED AGAIN: $($file.remoteFile)"
            }
        }
    } catch {
        Write-Output "Error processing $($file.local): $($_.Exception.Message)"
    }
}

# Restart the Python App via Passenger
$restartUri = "https://167.235.11.154:2083/execute/Fileman/file_op"
$restartBody = @{
    op = "create"
    sourcefiles = "restart.txt"
    destfiles = "/home/terapkco/xcomic_backend/tmp"
}
try {
    Invoke-RestMethod -Uri $restartUri -Headers $headers -Method POST -Body $restartBody -TimeoutSec 30 | Out-Null
    Write-Output "SUCCESS: Passenger triggered to restart via tmp/restart.txt"
} catch {
    Write-Output "Error restarting app: $($_.Exception.Message)"
}
