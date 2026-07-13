import codecs
import re

html = codecs.open('frontend/index.html', 'r', 'utf-8').read()

features_data = [
    {
        "en": "Go to \"Accounts\" > \"Add Account\" to add multiple SMTPs. The system automatically rotates them during campaigns.",
        "bn": "\"Accounts\" মেনু থেকে \"Add Account\" এ গিয়ে আপনার একাধিক SMTP যুক্ত করুন। ক্যাম্পেইন চলাকালীন সিস্টেম নিজে থেকেই এগুলো ঘুরিয়ে ঘুরিয়ে ব্যবহার করবে।"
    },
    {
        "en": "Set your initial \"Daily Limit\" when adding an account. Enable \"Auto Warmup\" so the system gradually increases it daily.",
        "bn": "অ্যাকাউন্ট যুক্ত করার সময় \"Daily Limit\" সেট করুন এবং \"Auto Warmup\" অন করে দিন। সিস্টেম প্রতিদিন একটু একটু করে ইমেইল পাঠানোর পরিমাণ বাড়াবে।"
    },
    {
        "en": "Before sending, use the \"Spam Checker\" tool in the dashboard to scan your email copy for spam trigger words.",
        "bn": "ইমেইল পাঠানোর আগে ড্যাশবোর্ডের \"Spam Checker\" টুল দিয়ে আপনার ইমেইল কপিটি স্ক্যান করে নিন, যাতে কোনো স্প্যামি শব্দ না থাকে।"
    },
    {
        "en": "Navigate to \"Audience\" > \"Import\". Upload your CSV file and the system will automatically remove duplicates and bad formats.",
        "bn": "\"Audience\" মেনু থেকে \"Import\" এ গিয়ে আপনার কন্টাক্ট লিস্ট (CSV) আপলোড করুন। সিস্টেম নিজে থেকেই ডুপ্লিকেট এবং ভুল ইমেইলগুলো ডিলিট করে দেবে।"
    },
    {
        "en": "In your email editor, type <code>{Hi|Hello|Hey}</code> to rotate greetings, and use <code>{{name}}</code> to dynamically insert the recipient's name.",
        "bn": "ইমেইল লেখার সময় <code>{Hi|Hello|Hey}</code> ব্যবহার করলে একেকজনের কাছে একেকটি শব্দ যাবে। আর <code>{{name}}</code> লিখলে সেখানে প্রাপকের নাম বসে যাবে।"
    },
    {
        "en": "Create a Campaign and select the \"Visual Builder\". Simply drag and drop text, images, and buttons to design your layout.",
        "bn": "নতুন ক্যাম্পেইন খোলার সময় \"Visual Builder\" সিলেক্ট করুন। এরপর বামপাশ থেকে টেক্সট, ছবি বা বাটন টেনে এনে সহজেই ডিজাইন তৈরি করুন।"
    },
    {
        "en": "Click the \"AI Assistant\" button in the email editor. Enter a short prompt and let Gemini generate or improve your email copy.",
        "bn": "ইমেইল এডিটরে থাকা \"AI Assistant\" বাটনে ক্লিক করুন। আপনি কী নিয়ে ইমেইল লিখতে চান তা লিখে দিলেই এআই আপনার জন্য ইমেইল লিখে দেবে।"
    },
    {
        "en": "Go to Campaign Settings to set your timezone, select working days, and specify the daily start and end times for sending.",
        "bn": "ক্যাম্পেইন সেটিংসে গিয়ে আপনার টাইমজোন, সপ্তাহের কোন দিনগুলোতে মেইল যাবে এবং প্রতিদিন কখন শুরু ও শেষ হবে তা সেট করে দিন।"
    },
    {
        "en": "Provide your IMAP credentials in Account Settings. The background engine will automatically track replies and hard bounces.",
        "bn": "অ্যাকাউন্ট সেটিংসে আপনার IMAP ডিটেইলস দিয়ে দিন। এরপর থেকে সিস্টেম নিজে থেকেই হার্ড বাউন্স এবং রিপ্লাই ট্র্যাক করে প্রয়োজনীয় ব্যবস্থা নেবে।"
    },
    {
        "en": "Click on any active or completed campaign from the dashboard to view live charts of sent, opened, and clicked emails.",
        "bn": "ড্যাশবোর্ড থেকে যেকোনো ক্যাম্পেইনের ওপর ক্লিক করলেই আপনি রিয়েল-টাইমে দেখতে পারবেন কতগুলো মেইল সেন্ট, ওপেন এবং ক্লিক হয়েছে।"
    },
    {
        "en": "Visit the \"Inbox\" tab. Gemini AI will automatically read your incoming replies and tag them as Positive, Negative, or OOO.",
        "bn": "\"Inbox\" ট্যাবে গেলে দেখতে পাবেন এআই নিজে থেকেই ইনকামিং রিপ্লাইগুলো পড়ে সেগুলোকে পজিটিভ, নেগেটিভ বা OOO (Out of office) হিসেবে ট্যাগ করে দিয়েছে।"
    },
    {
        "en": "In Campaign Settings, configure the minimum and maximum delay (e.g., 60-120 seconds). Emails will be sent with random intervals.",
        "bn": "ক্যাম্পেইন সেটিংসে গিয়ে মিনিমাম এবং ম্যাক্সিমাম ডিলে (যেমন: ৬০ থেকে ১২০ সেকেন্ড) সেট করুন। সিস্টেম এর মাঝে রেন্ডম সময় পর পর মেইল পাঠাবে।"
    },
    {
        "en": "When creating a campaign, click \"Templates\" to browse and select from hundreds of pre-designed responsive email layouts.",
        "bn": "নতুন ক্যাম্পেইন বানানোর সময় \"Templates\" এ ক্লিক করে শতাধিক রেডিমেড রেসপনসিভ ডিজাইন থেকে আপনার পছন্দের টেমপ্লেটটি বেছে নিন।"
    },
    {
        "en": "Simply set your local timezone in Settings. The system takes care of resetting your daily quotas automatically at midnight.",
        "bn": "সেটিংসে গিয়ে শুধু আপনার লোকাল টাইমজোন সেট করে দিন। এরপর প্রতিদিন রাত ১২টা বাজলেই সিস্টেম আপনার ডেইলি লিমিট রিসেট করে দেবে।"
    },
    {
        "en": "Enable \"Ramp Up\" in your campaign and set a daily increment amount. The system will safely scale up based on the last 7 days.",
        "bn": "ক্যাম্পেইনে \"Ramp Up\" অপশনটি চালু করে দিন। সিস্টেম আপনার গত ৭ দিনের পারফরম্যান্স অনুযায়ী প্রতিদিন একটু একটু করে ইমেইল সেন্ডিং বাড়াবে।"
    },
    {
        "en": "As an admin, go to the \"Health\" tab to view live graphs of CPU, RAM, and Database status to ensure smooth operation.",
        "bn": "অ্যাডমিন হিসেবে \"Health\" ট্যাবে গেলে আপনি রিয়েল-টাইমে সার্ভারের CPU, RAM এবং ডাটাবেজ কানেকশন স্ট্যাটাস দেখতে পারবেন।"
    },
    {
        "en": "The background APScheduler engine runs automatically. Just change a campaign state to \"Running\" and it handles the rest safely.",
        "bn": "ব্যাকগ্রাউন্ড ইঞ্জিনটি অটোমেটিক চলে। আপনি শুধু ক্যাম্পেইনটিকে \"Running\" করে দিন, বাকি কাজ (যেমন: এরর হ্যান্ডেলিং) সিস্টেম নিজেই করে নেবে।"
    }
]

# Find all about-card elements
card_pattern = r'(<div class="about-card"[^>]*>.*?)(</div>\s*</div>\s*(?:<!--|<div class="about-card"|</div>))'
matches = list(re.finditer(r'<div class="about-card".*?(?=</div>\s*</div>\s*</div>|</div>\s*<div class="about-card"|</div>\s*</div>\s*<!--)', html, re.DOTALL))

# We need a more reliable way to inject into the first 17 cards.
# Let's split by <div class="about-card"
parts = html.split('<div class="about-card"')
# parts[0] is everything before the first card
# parts[1] to parts[18] are the cards (18 total)
# We want to modify parts[1] through parts[17]

if len(parts) >= 19:
    for i in range(1, 18): # 1 to 17
        data = features_data[i-1]
        
        injection = f'''
                      <div class="htu-container" style="margin-top: auto; padding-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1); perspective: 1000px;">
                          <button class="htu-btn" onclick="toggle3DHowToUse(this)" style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: transparent; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.3s; background: rgba(0,0,0,0.02); box-shadow: 0 2px 5px rgba(0,0,0,0.01);">
                              <span style="font-weight: 600; color: var(--text); font-size: 15px; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-wand-magic-sparkles" style="color: var(--p);"></i> How to Use</span>
                              <i class="fa-solid fa-chevron-down" style="color: var(--text-muted); font-size: 14px; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);"></i>
                          </button>
                          <div class="htu-content" style="max-height: 0; opacity: 0; transform-origin: top; transform: rotateX(-90deg); transition: max-height 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; background: rgba(var(--icon-color-rgb), 0.05); border-left: 3px solid var(--icon-color-1); border-radius: 0 8px 8px 0; margin-top: 12px;">
                              <div style="padding: 16px;">
                                  <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 12px;"><strong>English:</strong> {data['en']}</p>
                                  <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 0;"><strong>Bangla:</strong> {data['bn']}</p>
                              </div>
                          </div>
                      </div>
'''
        # We need to insert this right before the last closing </div> of the card content
        # parts[i] ends with </div> which closes the card. Wait, let's look at the card structure.
        # It's:
        # <div class="about-card" ...>
        #   <div class="about-icon-wrapper">...</div>
        #   <h3>...</h3>
        #   <p>...</p>
        #   <p>...</p>
        # </div>
        # So we just need to append our injection right before the last </div>
        
        last_div_idx = parts[i].rfind('</div>')
        if last_div_idx != -1:
            parts[i] = parts[i][:last_div_idx] + injection + parts[i][last_div_idx:]

    new_html = '<div class="about-card"'.join(parts)
    
    # Now add the javascript to the bottom if not exists
    js_code = '''
<script>
function toggle3DHowToUse(btn) {
    const content = btn.nextElementSibling;
    const icon = btn.querySelector('.fa-chevron-down');
    
    if (content.style.maxHeight === '0px' || content.style.maxHeight === '') {
        content.style.maxHeight = content.scrollHeight + 'px';
        content.style.opacity = '1';
        content.style.transform = 'rotateX(0)';
        icon.style.transform = 'rotate(180deg)';
        btn.style.background = 'rgba(0,0,0,0.06)';
    } else {
        content.style.maxHeight = '0px';
        content.style.opacity = '0';
        content.style.transform = 'rotateX(-90deg)';
        icon.style.transform = 'rotate(0)';
        btn.style.background = 'rgba(0,0,0,0.02)';
    }
}
</script>
'''
    if 'toggle3DHowToUse' not in new_html:
        new_html = new_html.replace('</body>', js_code + '\n</body>')

    codecs.open('frontend/index.html', 'w', 'utf-8').write(new_html)
    print("Successfully added 3D How To Use boxes to 17 features.")
else:
    print(f"Error: Found only {len(parts)-1} features.")
