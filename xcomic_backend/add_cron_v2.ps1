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

$addUri = "https://167.235.11.154:2083/json-api/cpanel?cpanel_jsonapi_user=terapkco&cpanel_jsonapi_apiversion=2&cpanel_jsonapi_module=Cron&cpanel_jsonapi_func=add_line"
$body = @{
    command = "curl -s https://xcomic.xyz/api/cron/run > /dev/null 2>&1"
    day = "*"
    hour = "*"
    minute = "*"
    month = "*"
    weekday = "*"
}

$r = Invoke-RestMethod -Uri $addUri -Headers $headers -Method POST -Body $body
if ($r.cpanelresult.data[0].status -eq 1) {
    Write-Output "SUCCESS: Cron job added successfully!"
} else {
    Write-Output "Response: $($r | ConvertTo-Json -Depth 5)"
}
