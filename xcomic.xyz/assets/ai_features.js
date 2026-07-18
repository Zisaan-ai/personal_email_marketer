
// AI Features - Fixed to use proper apiCall (no hardcoded localhost)

window.aiToast = function(msg, type='info') {
    // BUG-36 FIX: was passing hex colors, but showToast expects type strings ('error'/'success'/'warning')
    showToast('🤖 ' + msg, type);
};

// =============================================
// AI: Generate Email (used in Visual Builder)
// =============================================
window.generateEmail = async function(targetId) {
    const prompt = window.prompt('What should this email be about? (e.g. "Flash sale 50% off shoes for Black Friday")');
    if (!prompt || !prompt.trim()) return;

    aiToast('Generating email...');
    try {
        const res = await apiCall('/ai/generate', 'POST', { prompt });
        const data = await res.json();
        if (!res.ok || data.error) {
            aiToast(data.error || data.detail || 'AI generation failed', 'error');
        } else {
            const el = document.getElementById(targetId);
            if (el) el.value = data.html || data.body_a || '';
            aiToast('Email generated!', 'success');
        }
    } catch (e) {
        aiToast('Failed to reach server: ' + e.message, 'error');
    }
};

// =============================================
// AI: Optimize Subject Line
// =============================================
window.optimizeSubject = async function(targetId) {
    const el = document.getElementById(targetId);
    if (!el || !el.value.trim()) {
        aiToast('Please enter a subject line first.', 'error');
        return;
    }

    const original = el.value;
    aiToast('Optimizing subject line...');
    try {
        const res = await apiCall('/ai/optimize-subject', 'POST', { subject: original });
        const data = await res.json();
        if (!res.ok || data.error) {
            aiToast(data.error || data.detail || 'Optimization failed', 'error');
        } else {
            el.value = data.subject || original;
            aiToast('Subject optimized! ✨', 'success');
        }
    } catch (e) {
        aiToast('Failed: ' + e.message, 'error');
    }
};

// =============================================
// AI: Generate Icebreakers for leads CSV
// =============================================
window.generateIcebreakers = async function(targetId) {
    const el = document.getElementById(targetId);
    if (!el || !el.value.trim()) {
        aiToast('Please paste CSV leads first.', 'error');
        return;
    }

    aiToast('Generating icebreakers... Please wait (~15s)');
    try {
        const res = await apiCall('/ai/generate-icebreakers', 'POST', { leads_csv: el.value });
        const data = await res.json();
        if (!res.ok || data.error) {
            aiToast(data.error || data.detail || 'Failed to generate icebreakers', 'error');
        } else {
            el.value = data.csv || el.value;
            aiToast('Icebreakers added to CSV! ✨', 'success');
        }
    } catch (e) {
        aiToast('Failed: ' + e.message, 'error');
    }
};

// =============================================
// AI: Auto-Pilot (scrape URL + write campaign)
// =============================================
window.runAutopilot = async function() {
    const inputEl = document.getElementById('autopilot-input');
    if (!inputEl || !inputEl.value.trim()) {
        aiToast('Please enter a link or product description!', 'error');
        return;
    }

    const btn = document.getElementById('autopilot-btn');
    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Running...'; }
    aiToast('Auto-Pilot initiated! Scraping & writing... (~15s)');

    try {
        const res = await apiCall('/ai/autopilot', 'POST', { prompt: inputEl.value });
        const data = await res.json();

        if (!res.ok || data.error) {
            aiToast(data.error || data.detail || 'Auto-Pilot failed', 'error');
            return;
        }

        const subjEl = document.getElementById('inst-subject');
        const bodyEl = document.getElementById('inst-body');
        if (subjEl) subjEl.value = data.subject_a || data.subject || '';
        if (bodyEl) bodyEl.value = data.body_a || data.body || '';

        // BUG-39 FIX: 'ab-test-container' doesn't exist — correct ID is 'inst-ab-section'
        // Also 'toggleABTest' doesn't exist — correct function is 'toggleInstAB'
        const abContainer = document.getElementById('inst-ab-section');
        if (abContainer && getComputedStyle(abContainer).display === 'none') {
            if (typeof window.toggleInstAB === 'function') window.toggleInstAB();
        }
        
        // A/B test
        if (data.subject_b) {
            const subjBEl = document.getElementById('inst-subject-b');
            const bodyBEl = document.getElementById('inst-body-b');
            if (subjBEl) subjBEl.value = data.subject_b;
            if (bodyBEl) bodyBEl.value = data.body_b || '';
        }

        aiToast('Campaign fully generated! 🚀', 'success');
    } catch (e) {
        aiToast('Auto-Pilot error: ' + e.message, 'error');
    } finally {
        if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fa-solid fa-robot"></i> Run Auto-Pilot'; }
    }
};

// =============================================
// AI: Copilot Chat
// =============================================
window.setupAICopilot = function() {
    // BUG-37 FIX: guard against duplicate listener registration
    if (window._copilotSetupDone) return;
    window._copilotSetupDone = true;

    const chatHistory = [];
    // BUG-3 FIX: HTML uses ai-chat-messages/ai-chat-input/ai-chat-send NOT copilot-* IDs
    const chatMessages = document.getElementById('ai-chat-messages') || document.getElementById('copilot-messages');
    const chatInput = document.getElementById('ai-chat-input') || document.getElementById('copilot-input');
    const sendBtn = document.getElementById('ai-chat-send') || document.getElementById('copilot-send-btn');

    function formatMarkdown(rawText) {
        if (!rawText) return '';
        // Escape HTML to prevent XSS
        let html = rawText
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

        // Code Block: ```code``` -> <pre><code>code</code></pre>
        html = html.replace(/```([^`]+)```/g, '<pre style="background:rgba(0,0,0,0.05);padding:10px;border-radius:8px;overflow-x:auto;font-family:monospace;font-size:13px;margin:8px 0;"><code>$1</code></pre>');

        // Inline Code: `code` -> <code>code</code>
        html = html.replace(/`([^`]+)`/g, '<code style="background:rgba(0,0,0,0.05);padding:2px 4px;border-radius:4px;font-family:monospace;font-size:13px;">$1</code>');

        // Bold: **text** -> <strong>text</strong>
        html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Italic: *text* -> <em>text</em>
        html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

        // Newlines to <br>
        html = html.replace(/\n/g, '<br>');

        return html;
    }

    function appendMsg(role, text) {
        if (!chatMessages) return;
        const isUser = role === 'user';
        const div = document.createElement('div');
        div.style.cssText = 'display:flex;gap:10px;align-items:flex-start;margin-bottom:14px;' + (isUser ? 'flex-direction:row-reverse;' : '');
        div.innerHTML = `
            <div style="width:32px;height:32px;border-radius:50%;background:${isUser ? '#4f46e5' : '#10b981'};display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;">
                ${isUser ? '👤' : '🤖'}
            </div>
            <div style="background:${isUser ? '#ede9fe' : '#f0fdf4'};padding:10px 14px;border-radius:12px;max-width:85%;font-size:14px;line-height:1.6;color:#0f172a;">
                ${formatMarkdown(text)}
            </div>
        `;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendMessage() {
        const msg = chatInput ? chatInput.value.trim() : '';
        if (!msg) return;
        if (chatInput) chatInput.value = '';
        if (sendBtn) sendBtn.disabled = true;

        appendMsg('user', msg);
        chatHistory.push({ role: 'user', content: msg });

        // Typing indicator
        const typing = document.createElement('div');
        typing.id = 'copilot-typing';
        typing.style.cssText = 'display:flex;gap:10px;align-items:center;margin-bottom:14px;';
        typing.innerHTML = '<div style="width:32px;height:32px;border-radius:50%;background:#10b981;display:flex;align-items:center;justify-content:center;font-size:14px;">🤖</div><div style="background:#f0fdf4;padding:10px 14px;border-radius:12px;font-size:14px;color:#64748b;"><i class="fa-solid fa-spinner fa-spin"></i> Thinking...</div>';
        if (chatMessages) { chatMessages.appendChild(typing); chatMessages.scrollTop = chatMessages.scrollHeight; }

        try {
            const res = await apiCall('/ai/chat', 'POST', { message: msg, history: chatHistory.slice(-6) });
            const data = await res.json();
            const typingEl = document.getElementById('copilot-typing');
            if (typingEl) typingEl.remove();

            if (!res.ok || data.error) {
                appendMsg('assistant', '❌ Error: ' + (data.error || data.detail || 'Something went wrong'));
            } else {
                const reply = data.reply || 'Sorry, I couldn\'t generate a response.';
                chatHistory.push({ role: 'assistant', content: reply });
                appendMsg('assistant', reply);
            }
        } catch (e) {
            const typingEl = document.getElementById('copilot-typing');
            if (typingEl) typingEl.remove();
            appendMsg('assistant', '⚠️ Connection error. Make sure Groq API key is set in Settings.');
        }

        if (sendBtn) sendBtn.disabled = false;
        if (chatInput) chatInput.focus();
    }

    if (sendBtn) sendBtn.addEventListener('click', sendMessage);
    if (chatInput) {
        chatInput.addEventListener('keydown', e => {
            if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
        });
    }

    // Welcome message
    if (chatMessages && chatMessages.children.length === 0) {
        appendMsg('assistant', 'Hi! I\'m your AI Copilot. 🚀\n\nI can help you:\n• Write cold emails & subject lines\n• Improve your email copy\n• Give campaign strategy advice\n• Generate personalized icebreakers\n\nWhat do you need?');
    }
};

// Auto-init copilot when DOM ready
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('copilot-messages') || document.getElementById('ai-chat-messages')) {
        window.setupAICopilot();
    }
});
