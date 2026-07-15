import codecs

features_html = """
<div class="about-card" style="--icon-color-1:#10b981; --icon-color-2:#059669; --icon-color-rgb:16,185,129;">
    <div class="about-icon-wrapper"><i class="fa-solid fa-users-gear"></i></div>
    <h3 class="about-title">1. Multi-Sender & Account Rotation</h3>
    <p class="about-text"><strong>English:</strong> Seamlessly integrate multiple SMTP accounts. The system intelligently rotates through active senders, distributing the workload and protecting individual account reputation.</p>
    <p class="about-text bn"><strong>Bangla:</strong> একসাথে অনেকগুলো SMTP অ্যাকাউন্ট যুক্ত করতে পারবেন। সিস্টেম স্বয়ংক্রিয়ভাবে একটির পর একটি অ্যাকাউন্ট দিয়ে মেইল পাঠাবে, যাতে কোনো একটি অ্যাকাউন্টের ওপর চাপ না পড়ে এবং রেপুটেশন সুরক্ষিত থাকে।</p>

    <div class="htu-container" style="margin-top: auto; padding-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1); perspective: 1000px;">
        <button class="htu-btn" onclick="toggle3DHowToUse(this)" style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: transparent; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.3s; background: rgba(0,0,0,0.02); box-shadow: 0 2px 5px rgba(0,0,0,0.01);">
            <span style="font-weight: 600; color: var(--text); font-size: 15px; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-wand-magic-sparkles" style="color: var(--p);"></i> How to Use</span>
            <i class="fa-solid fa-chevron-down" style="color: var(--text-muted); font-size: 14px; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);"></i>
        </button>
        <div class="htu-content" style="max-height: 0; opacity: 0; transform-origin: top; transform: rotateX(-90deg); transition: max-height 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; background: rgba(var(--icon-color-rgb), 0.05); border-left: 3px solid var(--icon-color-1); border-radius: 0 8px 8px 0; margin-top: 12px;">
            <div style="padding: 16px;">
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 12px;"><strong>English:</strong> Go to "Accounts" &gt; "Add Account" to add multiple SMTPs. The system automatically rotates them during campaigns.</p>
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 0;"><strong>Bangla:</strong> "Accounts" পেজ থেকে "Add Account" এ ক্লিক করে একাধিক SMTP অ্যাকাউন্ট যুক্ত করুন। ক্যাম্পেইন চালানোর সময় সিস্টেম নিজে থেকেই অ্যাকাউন্ট পরিবর্তন করে মেইল পাঠাবে।</p>
            </div>
        </div>
    </div>
</div>

<div class="about-card" style="--icon-color-1:#3b82f6; --icon-color-2:#2563eb; --icon-color-rgb:59,130,246;">
    <div class="about-icon-wrapper"><i class="fa-solid fa-arrow-trend-up"></i></div>
    <h3 class="about-title">2. Auto-Warmup & Smart Limits</h3>
    <p class="about-text"><strong>English:</strong> Establish domain trust automatically. The engine gradually warms up new accounts and suggests optimal daily limits based on inbox performance to avoid spam traps.</p>
    <p class="about-text bn"><strong>Bangla:</strong> নতুন অ্যাকাউন্টগুলোকে ইনবক্সে যাওয়ার উপযোগী করতে সিস্টেম স্বয়ংক্রিয়ভাবে ওয়ার্মআপ করে এবং ইনবক্স ডেলিভারি পারফরম্যান্সের ওপর ভিত্তি করে প্রতিদিনের জন্য সেফ সেন্ট লিমিট সেট করে দেয়।</p>

    <div class="htu-container" style="margin-top: auto; padding-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1); perspective: 1000px;">
        <button class="htu-btn" onclick="toggle3DHowToUse(this)" style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: transparent; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.3s; background: rgba(0,0,0,0.02); box-shadow: 0 2px 5px rgba(0,0,0,0.01);">
            <span style="font-weight: 600; color: var(--text); font-size: 15px; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-wand-magic-sparkles" style="color: var(--p);"></i> How to Use</span>
            <i class="fa-solid fa-chevron-down" style="color: var(--text-muted); font-size: 14px; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);"></i>
        </button>
        <div class="htu-content" style="max-height: 0; opacity: 0; transform-origin: top; transform: rotateX(-90deg); transition: max-height 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; background: rgba(var(--icon-color-rgb), 0.05); border-left: 3px solid var(--icon-color-1); border-radius: 0 8px 8px 0; margin-top: 12px;">
            <div style="padding: 16px;">
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 12px;"><strong>English:</strong> Enable "Smart Active" and "Warmup" toggles on your Sending Accounts page. The system will handle the rest.</p>
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 0;"><strong>Bangla:</strong> অ্যাকাউন্টস পেজ থেকে "Smart Limit" এবং "Warmup" টগল অন করে দিন। বাকি সব সিস্টেম নিজে থেকেই হ্যান্ডেল করবে।</p>
            </div>
        </div>
    </div>
</div>

<div class="about-card" style="--icon-color-1:#f59e0b; --icon-color-2:#d97706; --icon-color-rgb:245,158,11;">
    <div class="about-icon-wrapper"><i class="fa-solid fa-heart-pulse"></i></div>
    <h3 class="about-title">3. Delivery-Based Health Monitor</h3>
    <p class="about-text"><strong>English:</strong> Account health is calculated dynamically based on real performance: total emails sent, open rates, and reply rates. High opens increase health, while bounces drop it rapidly.</p>
    <p class="about-text bn"><strong>Bangla:</strong> অ্যাকাউন্টের হেলথ স্কোর রিয়েল পারফরম্যান্স (যেমন: মোট সেন্ড, ওপেন রেট, রিপ্লাই রেট) অনুযায়ী ক্যালকুলেট হয়। বেশি মেইল ওপেন হলে স্কোর বাড়বে, আর বাউন্স হলে স্কোর কমে যাবে।</p>

    <div class="htu-container" style="margin-top: auto; padding-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1); perspective: 1000px;">
        <button class="htu-btn" onclick="toggle3DHowToUse(this)" style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: transparent; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.3s; background: rgba(0,0,0,0.02); box-shadow: 0 2px 5px rgba(0,0,0,0.01);">
            <span style="font-weight: 600; color: var(--text); font-size: 15px; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-wand-magic-sparkles" style="color: var(--p);"></i> How to Use</span>
            <i class="fa-solid fa-chevron-down" style="color: var(--text-muted); font-size: 14px; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);"></i>
        </button>
        <div class="htu-content" style="max-height: 0; opacity: 0; transform-origin: top; transform: rotateX(-90deg); transition: max-height 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; background: rgba(var(--icon-color-rgb), 0.05); border-left: 3px solid var(--icon-color-1); border-radius: 0 8px 8px 0; margin-top: 12px;">
            <div style="padding: 16px;">
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 12px;"><strong>English:</strong> View real-time health progress bars and bounce statistics on the Sending Accounts page.</p>
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 0;"><strong>Bangla:</strong> অ্যাকাউন্টের হেলথ বার এবং বাউন্স রেট সরাসরি Sending Accounts পেজে রিয়েল টাইমে দেখা যাবে।</p>
            </div>
        </div>
    </div>
</div>

<div class="about-card" style="--icon-color-1:#a855f7; --icon-color-2:#9333ea; --icon-color-rgb:168,85,247;">
    <div class="about-icon-wrapper"><i class="fa-solid fa-shield-check"></i></div>
    <h3 class="about-title">4. Advanced Deliverability Check</h3>
    <p class="about-text"><strong>English:</strong> Pre-flight checks ensure your campaigns land in the inbox. It verifies MX records, evaluates SPF/DKIM/DMARC compliance, and analyzes email content for spam triggers.</p>
    <p class="about-text bn"><strong>Bangla:</strong> ক্যাম্পেইন চালু করার আগে প্রি-ফ্লাইট চেকের মাধ্যমে স্প্যাম ওয়ার্ড, লিংক, এবং ডোমেইনের (SPF/DKIM/DMARC) রেপুটেশন যাচাই করা হয়, যাতে মেইল সরাসরি ইনবক্সে যায়।</p>

    <div class="htu-container" style="margin-top: auto; padding-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1); perspective: 1000px;">
        <button class="htu-btn" onclick="toggle3DHowToUse(this)" style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: transparent; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.3s; background: rgba(0,0,0,0.02); box-shadow: 0 2px 5px rgba(0,0,0,0.01);">
            <span style="font-weight: 600; color: var(--text); font-size: 15px; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-wand-magic-sparkles" style="color: var(--p);"></i> How to Use</span>
            <i class="fa-solid fa-chevron-down" style="color: var(--text-muted); font-size: 14px; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);"></i>
        </button>
        <div class="htu-content" style="max-height: 0; opacity: 0; transform-origin: top; transform: rotateX(-90deg); transition: max-height 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; background: rgba(var(--icon-color-rgb), 0.05); border-left: 3px solid var(--icon-color-1); border-radius: 0 8px 8px 0; margin-top: 12px;">
            <div style="padding: 16px;">
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 12px;"><strong>English:</strong> Click "Launch Campaign". The system will automatically perform a Pre-flight Deliverability check before sending.</p>
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 0;"><strong>Bangla:</strong> ক্যাম্পেইন Launch করার সময় সিস্টেম নিজে থেকেই স্প্যাম চেক এবং ডোমেইন হেলথ যাচাই করে নিবে।</p>
            </div>
        </div>
    </div>
</div>

<div class="about-card" style="--icon-color-1:#ef4444; --icon-color-2:#dc2626; --icon-color-rgb:239,68,68;">
    <div class="about-icon-wrapper"><i class="fa-solid fa-inbox"></i></div>
    <h3 class="about-title">5. Inbox & Spam Placement Test</h3>
    <p class="about-text"><strong>English:</strong> Real-time inbox placement testing. Send a live test email to see exactly where your email lands (Inbox, Spam, or Promotions) before starting your main campaign.</p>
    <p class="about-text bn"><strong>Bangla:</strong> ক্যাম্পেইন পাঠানোর আগেই রিয়েল টাইমে টেস্ট করে দেখে নিতে পারবেন যে আপনার মেইল ইনবক্সে যাচ্ছে, নাকি স্প্যাম বা প্রমোশন ট্যাবে ঢুকছে।</p>

    <div class="htu-container" style="margin-top: auto; padding-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1); perspective: 1000px;">
        <button class="htu-btn" onclick="toggle3DHowToUse(this)" style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: transparent; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.3s; background: rgba(0,0,0,0.02); box-shadow: 0 2px 5px rgba(0,0,0,0.01);">
            <span style="font-weight: 600; color: var(--text); font-size: 15px; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-wand-magic-sparkles" style="color: var(--p);"></i> How to Use</span>
            <i class="fa-solid fa-chevron-down" style="color: var(--text-muted); font-size: 14px; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);"></i>
        </button>
        <div class="htu-content" style="max-height: 0; opacity: 0; transform-origin: top; transform: rotateX(-90deg); transition: max-height 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; background: rgba(var(--icon-color-rgb), 0.05); border-left: 3px solid var(--icon-color-1); border-radius: 0 8px 8px 0; margin-top: 12px;">
            <div style="padding: 16px;">
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 12px;"><strong>English:</strong> In Sending Accounts, click the "Test Inbox" icon, enter a test email, and check where it lands.</p>
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 0;"><strong>Bangla:</strong> Sending Accounts পেজে "Test Inbox" আইকনে ক্লিক করে যেকোনো ইমেইলে টেস্ট সেন্ড করে ডেলিভারি স্ট্যাটাস চেক করুন।</p>
            </div>
        </div>
    </div>
</div>

<div class="about-card" style="--icon-color-1:#14b8a6; --icon-color-2:#0d9488; --icon-color-rgb:20,184,166;">
    <div class="about-icon-wrapper"><i class="fa-solid fa-link"></i></div>
    <h3 class="about-title">6. Custom Tracking Domains</h3>
    <p class="about-text"><strong>English:</strong> Mask your open and click tracking links with a custom domain to bypass spam filters and improve sender reputation by avoiding shared tracking servers.</p>
    <p class="about-text bn"><strong>Bangla:</strong> মেইল ট্র্যাকিংয়ের জন্য নিজস্ব কাস্টম ডোমেইন ব্যবহার করুন। এতে স্প্যাম ফিল্টার বাইপাস হবে এবং ইনবক্সে মেইল যাওয়ার সম্ভাবনা কয়েক গুণ বেড়ে যাবে।</p>

    <div class="htu-container" style="margin-top: auto; padding-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1); perspective: 1000px;">
        <button class="htu-btn" onclick="toggle3DHowToUse(this)" style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: transparent; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.3s; background: rgba(0,0,0,0.02); box-shadow: 0 2px 5px rgba(0,0,0,0.01);">
            <span style="font-weight: 600; color: var(--text); font-size: 15px; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-wand-magic-sparkles" style="color: var(--p);"></i> How to Use</span>
            <i class="fa-solid fa-chevron-down" style="color: var(--text-muted); font-size: 14px; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);"></i>
        </button>
        <div class="htu-content" style="max-height: 0; opacity: 0; transform-origin: top; transform: rotateX(-90deg); transition: max-height 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; background: rgba(var(--icon-color-rgb), 0.05); border-left: 3px solid var(--icon-color-1); border-radius: 0 8px 8px 0; margin-top: 12px;">
            <div style="padding: 16px;">
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 12px;"><strong>English:</strong> Edit any sending account and assign a specific custom tracking domain URL.</p>
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 0;"><strong>Bangla:</strong> Sending Account এডিট করে সেখানে "Custom Tracking Domain" সেট করতে পারবেন।</p>
            </div>
        </div>
    </div>
</div>

<div class="about-card" style="--icon-color-1:#6366f1; --icon-color-2:#4f46e5; --icon-color-rgb:99,102,241;">
    <div class="about-icon-wrapper"><i class="fa-solid fa-brain"></i></div>
    <h3 class="about-title">7. AI Autopilot & AI Reply</h3>
    <p class="about-text"><strong>English:</strong> Leverage Gemini & Groq AI to automatically draft contextual replies, generate cold emails, optimize subject lines, and generate hyper-personalized icebreakers for leads.</p>
    <p class="about-text bn"><strong>Bangla:</strong> Gemini ও Groq AI ব্যবহার করে ইনবক্সে আসা মেইলের অটোমেটিক রিপ্লাই লেখা, সাবজেক্ট অপ্টিমাইজ করা এবং কোল্ড ইমেইলের জন্য কাস্টম আইসব্রেকার জেনারেট করার দারুণ সব ফিচার রয়েছে।</p>

    <div class="htu-container" style="margin-top: auto; padding-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1); perspective: 1000px;">
        <button class="htu-btn" onclick="toggle3DHowToUse(this)" style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: transparent; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.3s; background: rgba(0,0,0,0.02); box-shadow: 0 2px 5px rgba(0,0,0,0.01);">
            <span style="font-weight: 600; color: var(--text); font-size: 15px; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-wand-magic-sparkles" style="color: var(--p);"></i> How to Use</span>
            <i class="fa-solid fa-chevron-down" style="color: var(--text-muted); font-size: 14px; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);"></i>
        </button>
        <div class="htu-content" style="max-height: 0; opacity: 0; transform-origin: top; transform: rotateX(-90deg); transition: max-height 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; background: rgba(var(--icon-color-rgb), 0.05); border-left: 3px solid var(--icon-color-1); border-radius: 0 8px 8px 0; margin-top: 12px;">
            <div style="padding: 16px;">
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 12px;"><strong>English:</strong> Add your AI API Keys in Settings. Use AI tools in Campaign creation, or click "AI Reply" in the Inbox.</p>
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 0;"><strong>Bangla:</strong> Settings এ API Key বসান। এরপর ক্যাম্পেইন বানানোর সময় অথবা ইনবক্সে "Generate AI Reply" বাটনে ক্লিক করে AI ব্যবহার করতে পারবেন।</p>
            </div>
        </div>
    </div>
</div>

<div class="about-card" style="--icon-color-1:#f43f5e; --icon-color-2:#e11d48; --icon-color-rgb:244,63,94;">
    <div class="about-icon-wrapper"><i class="fa-solid fa-filter-circle-xmark"></i></div>
    <h3 class="about-title">8. Audience & Auto-Cleaning</h3>
    <p class="about-text"><strong>English:</strong> Advanced lead management with built-in bounce detection. The system automatically marks bouncing leads as invalid and auto-cleans old inactive leads over 90 days.</p>
    <p class="about-text bn"><strong>Bangla:</strong> অ্যাডভান্সড অডিয়েন্স ম্যানেজমেন্ট, যা বাউন্স হওয়া মেইলগুলোকে অটোমেটিকভাবে ইনভ্যালিড মার্ক করে। এবং ৯০ দিনের পুরোনো ইনঅ্যাকটিভ লিডগুলোকে মুছে ফেলে ডাটাবেস পরিষ্কার রাখে।</p>

    <div class="htu-container" style="margin-top: auto; padding-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1); perspective: 1000px;">
        <button class="htu-btn" onclick="toggle3DHowToUse(this)" style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: transparent; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.3s; background: rgba(0,0,0,0.02); box-shadow: 0 2px 5px rgba(0,0,0,0.01);">
            <span style="font-weight: 600; color: var(--text); font-size: 15px; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-wand-magic-sparkles" style="color: var(--p);"></i> How to Use</span>
            <i class="fa-solid fa-chevron-down" style="color: var(--text-muted); font-size: 14px; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);"></i>
        </button>
        <div class="htu-content" style="max-height: 0; opacity: 0; transform-origin: top; transform: rotateX(-90deg); transition: max-height 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; background: rgba(var(--icon-color-rgb), 0.05); border-left: 3px solid var(--icon-color-1); border-radius: 0 8px 8px 0; margin-top: 12px;">
            <div style="padding: 16px;">
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 12px;"><strong>English:</strong> Upload CSV files in Audience. Auto-cleaning runs automatically in the background to keep lists fresh.</p>
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 0;"><strong>Bangla:</strong> Audience পেজে আপনার লিডগুলো CSV হিসেবে আপলোড করুন। সিস্টেম নিজে থেকেই বাউন্স হওয়া মেইলগুলো ব্লক করে দেবে।</p>
            </div>
        </div>
    </div>
</div>

<div class="about-card" style="--icon-color-1:#eab308; --icon-color-2:#ca8a04; --icon-color-rgb:234,179,8;">
    <div class="about-icon-wrapper"><i class="fa-solid fa-clock"></i></div>
    <h3 class="about-title">9. Anti-Spam Humanized Delay</h3>
    <p class="about-text"><strong>English:</strong> Add random wait times (Min & Max Delay) between sending each email in a campaign to mimic human behavior and protect your sender reputation from strict spam filters.</p>
    <p class="about-text bn"><strong>Bangla:</strong> স্প্যাম ফিল্টার থেকে বাঁচতে প্রতিটা মেইল সেন্ড করার মাঝে র‍্যান্ডম গ্যাপ (Min & Max Delay) সেট করার সুবিধা রয়েছে। এতে মেইল পাঠানো একদম ন্যাচারাল মনে হবে।</p>

    <div class="htu-container" style="margin-top: auto; padding-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1); perspective: 1000px;">
        <button class="htu-btn" onclick="toggle3DHowToUse(this)" style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: transparent; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.3s; background: rgba(0,0,0,0.02); box-shadow: 0 2px 5px rgba(0,0,0,0.01);">
            <span style="font-weight: 600; color: var(--text); font-size: 15px; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-wand-magic-sparkles" style="color: var(--p);"></i> How to Use</span>
            <i class="fa-solid fa-chevron-down" style="color: var(--text-muted); font-size: 14px; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);"></i>
        </button>
        <div class="htu-content" style="max-height: 0; opacity: 0; transform-origin: top; transform: rotateX(-90deg); transition: max-height 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; background: rgba(var(--icon-color-rgb), 0.05); border-left: 3px solid var(--icon-color-1); border-radius: 0 8px 8px 0; margin-top: 12px;">
            <div style="padding: 16px;">
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 12px;"><strong>English:</strong> Before launching a campaign, adjust the Min and Max Delay sliders in the Campaign settings.</p>
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 0;"><strong>Bangla:</strong> ক্যাম্পেইন Launch করার আগে অপশন থেকে Min Delay এবং Max Delay সেকেন্ডে সেট করে দিন।</p>
            </div>
        </div>
    </div>
</div>

<div class="about-card" style="--icon-color-1:#22c55e; --icon-color-2:#16a34a; --icon-color-rgb:34,197,94;">
    <div class="about-icon-wrapper"><i class="fa-solid fa-chart-line"></i></div>
    <h3 class="about-title">10. IMAP Replies Processing</h3>
    <p class="about-text"><strong>English:</strong> Advanced IMAP synchronization safely reads your inbox to track opens, clicks, and replies without triggering third-party pixel blocks. Perfect for true cold email analytics.</p>
    <p class="about-text bn"><strong>Bangla:</strong> IMAP সিঙ্ক করে ডাইরেক্ট ইনবক্স থেকে মেইল ওপেন এবং রিপ্লাই ট্র্যাক করার সুবিধা, যার ফলে ট্র্যাকিং পিক্সেল ব্লক হয়ে যাওয়ার কোনো সম্ভাবনা নেই।</p>

    <div class="htu-container" style="margin-top: auto; padding-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1); perspective: 1000px;">
        <button class="htu-btn" onclick="toggle3DHowToUse(this)" style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: transparent; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.3s; background: rgba(0,0,0,0.02); box-shadow: 0 2px 5px rgba(0,0,0,0.01);">
            <span style="font-weight: 600; color: var(--text); font-size: 15px; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-wand-magic-sparkles" style="color: var(--p);"></i> How to Use</span>
            <i class="fa-solid fa-chevron-down" style="color: var(--text-muted); font-size: 14px; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);"></i>
        </button>
        <div class="htu-content" style="max-height: 0; opacity: 0; transform-origin: top; transform: rotateX(-90deg); transition: max-height 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; background: rgba(var(--icon-color-rgb), 0.05); border-left: 3px solid var(--icon-color-1); border-radius: 0 8px 8px 0; margin-top: 12px;">
            <div style="padding: 16px;">
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 12px;"><strong>English:</strong> Add your IMAP server details along with SMTP. The system checks replies in the background automatically.</p>
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 0;"><strong>Bangla:</strong> অ্যাকাউন্ট যোগ করার সময় IMAP সার্ভারের তথ্য দিন। সিস্টেম ব্যাকগ্রাউন্ডে চেক করে সব ট্র্যাকিং ডাটা আপডেট করবে।</p>
            </div>
        </div>
    </div>
</div>

<div class="about-card" style="--icon-color-1:#64748b; --icon-color-2:#475569; --icon-color-rgb:100,116,139;">
    <div class="about-icon-wrapper"><i class="fa-solid fa-calendar-check"></i></div>
    <h3 class="about-title">11. BD Timezone Auto Reset</h3>
    <p class="about-text"><strong>English:</strong> All daily limits, warmup targets, and sending statistics automatically reset exactly at midnight (12:00 AM) according to the Bangladesh Timezone (BST).</p>
    <p class="about-text bn"><strong>Bangla:</strong> প্রতিটি অ্যাকাউন্টের ডেইলি লিমিট, সেন্ড কাউন্ট এবং ওয়ার্মআপ ডাটা বাংলাদেশ সময় ঠিক রাত ১২টায় অটোমেটিকভাবে রিসেট হয়ে যায়।</p>

    <div class="htu-container" style="margin-top: auto; padding-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1); perspective: 1000px;">
        <button class="htu-btn" onclick="toggle3DHowToUse(this)" style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: transparent; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.3s; background: rgba(0,0,0,0.02); box-shadow: 0 2px 5px rgba(0,0,0,0.01);">
            <span style="font-weight: 600; color: var(--text); font-size: 15px; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-wand-magic-sparkles" style="color: var(--p);"></i> How to Use</span>
            <i class="fa-solid fa-chevron-down" style="color: var(--text-muted); font-size: 14px; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);"></i>
        </button>
        <div class="htu-content" style="max-height: 0; opacity: 0; transform-origin: top; transform: rotateX(-90deg); transition: max-height 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; background: rgba(var(--icon-color-rgb), 0.05); border-left: 3px solid var(--icon-color-1); border-radius: 0 8px 8px 0; margin-top: 12px;">
            <div style="padding: 16px;">
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 12px;"><strong>English:</strong> No action required. The internal scheduler manages timezone differences and resets limits seamlessly.</p>
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 0;"><strong>Bangla:</strong> এর জন্য কিছুই করতে হবে না। সিস্টেম ব্যাকগ্রাউন্ডে বাংলাদেশ টাইম জোন অনুযায়ী নিজে থেকেই লিমিট রিসেট করে দিবে।</p>
            </div>
        </div>
    </div>
</div>

<div class="about-card" style="grid-column: 1 / -1; --icon-color-1:#4f46e5; --icon-color-2:#ec4899; --icon-color-rgb:79,70,229; background: linear-gradient(135deg, rgba(79, 70, 229, 0.05), rgba(236, 72, 153, 0.05)); border: 1px solid rgba(79, 70, 229, 0.2);">
    <div class="about-icon-wrapper" style="margin-left:auto; margin-right:auto; margin-bottom: 16px;"><i class="fa-solid fa-user-shield"></i></div>
    <h3 class="about-title" style="text-align:center;">Engineered & Administered by Monem Rahman Zisan</h3>
    <p class="about-text" style="text-align:center; max-width: 800px; margin: 0 auto 12px;"><strong>English:</strong> Designed and engineered by Monem Rahman Zisan. Includes a Secure Admin Dashboard with JWT token-based authentication and strict RBAC, accessible exclusively by the creator to manage users and ensure maximum security.</p>
    <p class="about-text bn" style="text-align:center; max-width: 800px; margin: 0 auto;"><strong>Bangla:</strong> সিস্টেমটি ডিজাইন এবং তৈরি করেছেন মোনেম রহমান জিসান। এর সিকিউরিটি মেইনটেইন করার জন্য রয়েছে স্পেশাল অ্যাডমিন ড্যাশবোর্ড, যা শুধুমাত্র ক্রিয়েটর অ্যাক্সেস করতে পারবেন।</p>
</div>
"""

with codecs.open('frontend/index.html', 'r', 'utf-8') as f:
    html = f.read()

start_grid = html.find('<div class="about-grid">')
if start_grid == -1:
    print("Could not find about-grid")
    exit()

end_marker = '<!-- INBOX PREVIEW MODAL -->'
end_idx = html.find(end_marker, start_grid)
if end_idx == -1:
    print("Could not find end marker")
    exit()

# The structure before end_marker has closing divs for about-grid and about-page.
# Instead of guessing the closing tags, let's look for the closing div of about-grid directly.
# The original html had:
# </div> <!-- about-card -->
# </div> <!-- about-grid -->
# </div> <!-- some wrapper -->
# <!-- INBOX PREVIEW MODAL -->
# Wait, let's see exactly what's between the last about-card and INBOX PREVIEW MODAL.
# It is just:
#   </div>
# </div>
#               
#         
#         <!-- INBOX PREVIEW MODAL -->

# We can replace everything between <div class="about-grid"> and the </div> just before INBOX PREVIEW MODAL.
end_grid = html.rfind('</div>', start_grid, end_idx) # finds the very last </div> before INBOX PREVIEW MODAL
end_grid = html.rfind('</div>', start_grid, end_grid) # finds the one before that (which closes about-grid)

new_html = html[:start_grid] + '<div class="about-grid">\n' + features_html + '\n</div>\n          </div>\n\n' + html[end_idx:]

with codecs.open('frontend/index.html', 'w', 'utf-8') as f:
    f.write(new_html)

print("About section updated with new features.")
