import codecs

with codecs.open('frontend/index.html', 'r', 'utf-8') as f:
    html = f.read()

new_cards = """
                    <!-- OpenAI -->
                    <div style="background:var(--bg); border:1px solid var(--border); border-radius:12px; padding:20px; margin-bottom:20px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
                            <div style="display:flex; align-items:center; gap:10px;">
                                <div style="width:32px;height:32px;border-radius:8px;background:#10a37f;display:flex;align-items:center;justify-content:center;">
                                    <i class="fa-solid fa-bolt" style="color:#fff;font-size:14px;"></i>
                                </div>
                                <div>
                                    <div style="display:flex; align-items:center; gap:8px;">
                                        <span style="font-size:14px;font-weight:700;">OpenAI (ChatGPT)</span>
                                    </div>
                                    <div style="font-size:12px;color:var(--text-muted);">Industry standard AI models</div>
                                </div>
                            </div>
                            <a href="https://platform.openai.com/api-keys" target="_blank" style="font-size:12px;color:var(--p);font-weight:600;text-decoration:none;"><i class="fa-solid fa-arrow-up-right-from-square" style="margin-right:4px;"></i>Get Key</a>
                        </div>
                        <div style="position:relative;">
                            <input type="password" id="openai-api-key" placeholder="sk-..." style="padding-right:44px;">
                            <button type="button" onclick="var el=document.getElementById('openai-api-key'); el.type=el.type==='password'?'text':'password'; this.innerHTML=el.type==='password'?'<i class=\'fa-regular fa-eye\'></i>':'<i class=\'fa-regular fa-eye-slash\'></i>'" style="position:absolute;right:14px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:var(--text-muted);">
                                <i class="fa-regular fa-eye"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Anthropic -->
                    <div style="background:var(--bg); border:1px solid var(--border); border-radius:12px; padding:20px; margin-bottom:20px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
                            <div style="display:flex; align-items:center; gap:10px;">
                                <div style="width:32px;height:32px;border-radius:8px;background:#d97757;display:flex;align-items:center;justify-content:center;">
                                    <i class="fa-solid fa-cube" style="color:#fff;font-size:14px;"></i>
                                </div>
                                <div>
                                    <div style="display:flex; align-items:center; gap:8px;">
                                        <span style="font-size:14px;font-weight:700;">Anthropic (Claude)</span>
                                    </div>
                                    <div style="font-size:12px;color:var(--text-muted);">Excellent for writing & coding</div>
                                </div>
                            </div>
                            <a href="https://console.anthropic.com/settings/keys" target="_blank" style="font-size:12px;color:var(--p);font-weight:600;text-decoration:none;"><i class="fa-solid fa-arrow-up-right-from-square" style="margin-right:4px;"></i>Get Key</a>
                        </div>
                        <div style="position:relative;">
                            <input type="password" id="anthropic-api-key" placeholder="sk-ant-..." style="padding-right:44px;">
                            <button type="button" onclick="var el=document.getElementById('anthropic-api-key'); el.type=el.type==='password'?'text':'password'; this.innerHTML=el.type==='password'?'<i class=\'fa-regular fa-eye\'></i>':'<i class=\'fa-regular fa-eye-slash\'></i>'" style="position:absolute;right:14px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:var(--text-muted);">
                                <i class="fa-regular fa-eye"></i>
                            </button>
                        </div>
                    </div>

                    <!-- DeepSeek -->
                    <div style="background:var(--bg); border:1px solid var(--border); border-radius:12px; padding:20px; margin-bottom:20px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
                            <div style="display:flex; align-items:center; gap:10px;">
                                <div style="width:32px;height:32px;border-radius:8px;background:#4d6bfe;display:flex;align-items:center;justify-content:center;">
                                    <i class="fa-solid fa-water" style="color:#fff;font-size:14px;"></i>
                                </div>
                                <div>
                                    <div style="display:flex; align-items:center; gap:8px;">
                                        <span style="font-size:14px;font-weight:700;">DeepSeek</span>
                                    </div>
                                    <div style="font-size:12px;color:var(--text-muted);">Cost-effective & powerful</div>
                                </div>
                            </div>
                            <a href="https://platform.deepseek.com/api_keys" target="_blank" style="font-size:12px;color:var(--p);font-weight:600;text-decoration:none;"><i class="fa-solid fa-arrow-up-right-from-square" style="margin-right:4px;"></i>Get Key</a>
                        </div>
                        <div style="position:relative;">
                            <input type="password" id="deepseek-api-key" placeholder="sk-..." style="padding-right:44px;">
                            <button type="button" onclick="var el=document.getElementById('deepseek-api-key'); el.type=el.type==='password'?'text':'password'; this.innerHTML=el.type==='password'?'<i class=\'fa-regular fa-eye\'></i>':'<i class=\'fa-regular fa-eye-slash\'></i>'" style="position:absolute;right:14px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:var(--text-muted);">
                                <i class="fa-regular fa-eye"></i>
                            </button>
                        </div>
                    </div>
"""

if 'id="deepseek-api-key"' not in html:
    html = html.replace('<button id="save-gemini-btn"', new_cards + '\n                    <button id="save-gemini-btn"')

with codecs.open('frontend/index.html', 'w', 'utf-8') as f:
    f.write(html)
