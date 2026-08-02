// Deliverability & Audience Health Logic
let preflightResolve = null;

async function runPreflightAsync(subject, body) {
    return new Promise((resolve) => {
        const modal = document.getElementById('preflight-modal');
        const loading = document.getElementById('preflight-loading');
        const results = document.getElementById('preflight-results');
        const scoreSpan = document.getElementById('preflight-score');
        const warningsDiv = document.getElementById('preflight-warnings');
        
        modal.style.display = 'flex';
        loading.style.display = 'flex';
        results.style.display = 'none';
        preflightResolve = resolve;
        
        apiCall('/preflight', 'POST', { subject: subject, body: body })
            .then(res => res.json())
            .then(data => {
                loading.style.display = 'none';
                results.style.display = 'block';
                
                scoreSpan.innerText = `${data.score}/10 (${data.rating})`;
                if (data.score >= 8) scoreSpan.style.color = '#10b981';
                else if (data.score >= 5) scoreSpan.style.color = '#f59e0b';
                else scoreSpan.style.color = '#ef4444';
                
                let warningsHtml = '';
                if (data.found_words && data.found_words.length > 0) {
                    warningsHtml += `<div><i class="fa-solid fa-triangle-exclamation"></i> <strong>Spam Words Found:</strong> ${data.found_words.join(', ')}</div>`;
                }
                if (data.warnings && data.warnings.length > 0) {
                    data.warnings.forEach(w => {
                        warningsHtml += `<div style="margin-top:8px;"><i class="fa-solid fa-circle-info"></i> ${w}</div>`;
                    });
                }
                
                if (!warningsHtml) {
                    warningsHtml = '<div style="color:#10b981;"><i class="fa-solid fa-check-circle"></i> Looks great! Your email is highly deliverable.</div>';
                }
                
                warningsDiv.innerHTML = warningsHtml;
            })
            .catch(err => {
                // If error, just allow them to send anyway
                resolve(true);
                modal.style.display = 'none';
            });
    });
}

function confirmPreflightSend() {
    if (preflightResolve) preflightResolve(true);
    document.getElementById('preflight-modal').style.display = 'none';
}

// Override the modal cancel button
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('preflight-modal');
    if(modal) {
        const cancelBtn = modal.querySelector('button.btn:not(.primary)');
        if (cancelBtn) {
            cancelBtn.onclick = () => {
                if (preflightResolve) preflightResolve(false);
                modal.style.display = 'none';
            };
        }
    }
});

async function runAudienceHealthScan() {
    const btn = document.getElementById('btn-scan-health');
    const resDiv = document.getElementById('health-scan-result');
    
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin" style="margin-right:8px;"></i> Scanning...';
    btn.disabled = true;
    resDiv.style.display = 'none';
    
    try {
        const res = await apiCall('/clean-inactive-leads', 'POST');
        if (res.ok) {
            const data = await res.json();
            resDiv.innerHTML = `<i class="fa-solid fa-check-circle" style="margin-right:8px;"></i> Health Scan Complete. ${data.tagged_count} inactive leads were found and tagged!`;
            resDiv.style.display = 'block';
            resDiv.style.opacity = '1';
            setTimeout(() => {
                resDiv.style.display = 'none';
            }, 3000);
        } else {
            const data = await res.json();
            showToast(data.detail || 'Failed to run health scan', 'error');
        }
    } catch(e) {
        showToast('Error running health scan', 'error');
    }
    
    btn.innerHTML = '<i class="fa-solid fa-broom" style="margin-right:8px;"></i> Scan & Clean Inactive Leads';
    btn.disabled = false;
}
