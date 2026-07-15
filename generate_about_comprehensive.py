import codecs

features = [
    {
        "title": "1. Multi-Sender & Account Rotation",
        "icon": "fa-users-gear",
        "colors": "--icon-color-1:#10b981; --icon-color-2:#059669; --icon-color-rgb:16,185,129;",
        "en": "Seamlessly integrate multiple SMTP accounts. Choose Automatic Load Balancing (Round-Robin) to let the system dynamically rotate senders, or manually select specific sending accounts for targeted campaigns to protect domain reputation.",
        "bn": "একসাথে অনেকগুলো SMTP অ্যাকাউন্ট যুক্ত করার সুবিধা। আপনি চাইলে অটোমেটিক রোটেশন অন করে রাখতে পারেন (সিস্টেম নিজে থেকে অ্যাকাউন্ট পরিবর্তন করে মেইল পাঠাবে), অথবা ম্যানুয়ালি নির্দিষ্ট কোনো অ্যাকাউন্ট সিলেক্ট করে ক্যাম্পেইন রান করতে পারবেন।",
        "htu_en": "Go to 'Accounts' > 'Add Account' to add SMTPs. In campaigns, select 'Auto-Rotate' or manually pick specific accounts.",
        "htu_bn": "Accounts থেকে SMTP অ্যাড করুন। ক্যাম্পেইন চালানোর সময় Auto-Rotate সিলেক্ট করুন অথবা ম্যানুয়ালি নির্দিষ্ট অ্যাকাউন্ট বেছে নিন।"
    },
    {
        "title": "2. Auto-Warmup vs Manual Warmup",
        "icon": "fa-arrow-trend-up",
        "colors": "--icon-color-1:#3b82f6; --icon-color-2:#2563eb; --icon-color-rgb:59,130,246;",
        "en": "Build domain trust effectively. Enable Smart Auto-Warmup to algorithmically scale your daily sending volume, or set Manual Warmup parameters to strictly control the exact number of emails sent per day.",
        "bn": "ডোমেইন ট্রাস্ট বিল্ড করার জন্য স্মার্ট ওয়ার্মআপ। আপনি 'Auto-Warmup' অন করে দিলে সিস্টেম নিজে থেকেই প্রতিদিন লিমিট বাড়াবে, আর চাইলে ম্যানুয়াল লিমিট সেট করে প্রতিদিন ঠিক কয়টা মেইল যাবে তা নিজে কন্ট্রোল করতে পারবেন।",
        "htu_en": "In Sending Accounts, toggle 'Warmup' for automatic scaling, or manually type your preferred daily limit.",
        "htu_bn": "Sending Accounts পেজ থেকে 'Warmup' টগল অন করুন (অটোমেটিকের জন্য) অথবা ইনপুট বক্সে ম্যানুয়ালি আপনার পছন্দমতো লিমিট বসিয়ে দিন।"
    },
    {
        "title": "3. Delivery-Based System Health Monitor",
        "icon": "fa-heart-pulse",
        "colors": "--icon-color-1:#f59e0b; --icon-color-2:#d97706; --icon-color-rgb:245,158,11;",
        "en": "Dynamic health assessment based on true deliverability metrics. The system auto-calculates health percentage from open/reply rates vs bounces. You can manually pause unhealthy accounts before reputation drops.",
        "bn": "রিয়েল ডেলিভারি ডাটা দিয়ে হেলথ ক্যালকুলেট হয়। বেশি মেইল ওপেন হলে অটোমেটিক্যালি হেলথ বাড়বে, আর বাউন্স হলে হেলথ কমে যাবে। হেলথ কম দেখলে আপনি ম্যানুয়ালি অ্যাকাউন্ট পজ করে দিতে পারবেন।",
        "htu_en": "Monitor the real-time health progress bars. If health drops below 50%, the system flags it—manually pause the account to recover.",
        "htu_bn": "রিয়েল টাইমে অ্যাকাউন্টের হেলথ বার খেয়াল রাখুন। হেলথ খুব কমে গেলে ম্যানুয়ালি পজ বাটনে ক্লিক করে অ্যাকাউন্ট সাময়িকভাবে বন্ধ রাখুন।"
    },
    {
        "title": "4. Pre-Flight Deliverability Optimizer",
        "icon": "fa-shield-check",
        "colors": "--icon-color-1:#a855f7; --icon-color-2:#9333ea; --icon-color-rgb:168,85,247;",
        "en": "Ensure maximum inbox placement. The system automatically performs DNS (SPF/DKIM/DMARC) validation and algorithmic spam-word analysis before launching, while you can manually tweak the content based on its feedback.",
        "bn": "মেইল স্প্যামে যাওয়ার হাত থেকে বাঁচাতে প্রি-ফ্লাইট অপ্টিমাইজার। ক্যাম্পেইন লঞ্চ করার আগে সিস্টেম অটোমেটিক্যালি ডোমেইন রেকর্ড (SPF/DKIM/DMARC) এবং স্প্যাম ওয়ার্ড স্ক্যান করে, এরপর আপনি ম্যানুয়ালি মেইলের টেক্সট পরিবর্তন করে ঠিক করতে পারবেন।",
        "htu_en": "Click 'Launch Campaign'. Review the auto-generated deliverability report, manually fix highlighted spam triggers, and confirm.",
        "htu_bn": "Launch Campaign-এ ক্লিক করলে অটোমেটিক্যালি স্প্যাম রিপোর্ট আসবে। কোনো রেড ফ্ল্যাগ থাকলে তা ম্যানুয়ালি ফিক্স করে তারপর কনফার্ম করুন।"
    },
    {
        "title": "5. Live Inbox & Spam Placement Testing",
        "icon": "fa-inbox",
        "colors": "--icon-color-1:#ef4444; --icon-color-2:#dc2626; --icon-color-rgb:239,68,68;",
        "en": "Never guess your deliverability. Use the manual Inbox Test feature to send a live probe email to any address and instantly verify if it lands in the Inbox, Promotions, or Spam folder.",
        "bn": "আপনার মেইল ইনবক্সে যাচ্ছে নাকি স্প্যামে, তা লাইভ টেস্ট করে দেখুন। মূল ক্যাম্পেইন শুরুর আগে যেকোনো ইমেইল অ্যাড্রেস বসিয়ে ম্যানুয়ালি টেস্ট সেন্ড করে ডেলিভারি স্ট্যাটাস যাচাই করতে পারবেন।",
        "htu_en": "Click the 'Test Inbox' icon next to any sending account, type your test email, and check the inbox placement manually.",
        "htu_bn": "যেকোনো অ্যাকাউন্টের পাশে থাকা 'Test Inbox' আইকনে ক্লিক করে ইমেইল অ্যাড্রেস দিন এবং ম্যানুয়ালি টেস্ট করে দেখুন।"
    },
    {
        "title": "6. Custom Tracking Domains",
        "icon": "fa-link",
        "colors": "--icon-color-1:#14b8a6; --icon-color-2:#0d9488; --icon-color-rgb:20,184,166;",
        "en": "Bypass rigid spam filters by masking click/open tracking links. Set a Custom Tracking Domain manually for each sender to maintain a pristine sender reputation and avoid blacklisted shared domains.",
        "bn": "শেয়ার্ড ট্র্যাকিং ডোমেইন ব্যবহার করলে স্প্যামে যাওয়ার চান্স থাকে। তাই প্রতিটি অ্যাকাউন্টের জন্য ম্যানুয়ালি নিজস্ব 'Custom Tracking Domain' সেট করে ট্র্যাকিং লিংক হাইড করুন এবং ইনবক্স রেট ১০০% নিশ্চিত করুন।",
        "htu_en": "Edit an account, toggle 'Custom Tracking Domain', and manually enter your verified CNAME domain URL.",
        "htu_bn": "অ্যাকাউন্ট এডিট করে Custom Tracking Domain টগল অন করুন এবং ম্যানুয়ালি আপনার ডোমেইন URL টি বসিয়ে সেভ করুন।"
    },
    {
        "title": "7. Audience & Intelligent Auto-Cleaning",
        "icon": "fa-filter-circle-xmark",
        "colors": "--icon-color-1:#f43f5e; --icon-color-2:#e11d48; --icon-color-rgb:244,63,94;",
        "en": "Maintain a pristine lead list. The system auto-detects hard bounces and invalidates them immediately. You can also manually upload CSVs, delete inactive leads, and segment audiences for precision targeting.",
        "bn": "অটোমেটিক অডিয়েন্স ক্লিনিং ফিচার। কোনো মেইল বাউন্স হলে সিস্টেম সাথে সাথেই সেটিকে ইনভ্যালিড করে দেয়। এছাড়া আপনি ম্যানুয়ালি CSV আপলোড করতে পারবেন এবং অব্যবহৃত পুরোনো লিডগুলো ডিলিট করতে পারবেন।",
        "htu_en": "Manually import leads via CSV. The platform's automated chron-jobs handle hard bounce invalidation behind the scenes.",
        "htu_bn": "Audience প্যানেলে ম্যানুয়ালি CSV ফাইল আপলোড করুন। মেইল বাউন্স হলে সিস্টেম ব্যাকগ্রাউন্ডে অটোমেটিক্যালি তা ব্লক করে দেবে।"
    },
    {
        "title": "8. AI Autopilot: Cold Email & Icebreakers",
        "icon": "fa-brain",
        "colors": "--icon-color-1:#6366f1; --icon-color-2:#4f46e5; --icon-color-rgb:99,102,241;",
        "en": "Harness the power of Gemini & Groq AI. Let the AI automatically generate highly-converting cold email drafts and personalized icebreakers, or manually edit and refine the AI's suggestions in the rich text editor.",
        "bn": "Gemini এবং Groq AI-এর মাধ্যমে অটোমেটিক কোল্ড ইমেইল ও আইসব্রেকার জেনারেট করুন। সিস্টেম নিজে থেকেই প্রফেশনাল মেইল লিখে দেবে, যা আপনি এডিটরে ম্যানুয়ালি নিজের মতো করে কাস্টমাইজ করে নিতে পারবেন।",
        "htu_en": "In the Composer, click 'AI Assistant', input your product details, auto-generate the content, and manually refine the text.",
        "htu_bn": "মেইল লেখার সময় 'AI Assistant' এ ক্লিক করে কমান্ড দিন। AI অটোমেটিক্যালি মেইল লিখে দেবে, এরপর ম্যানুয়ালি এডিট করে নিন।"
    },
    {
        "title": "9. AI Auto-Reply & Manual Inbox Management",
        "icon": "fa-reply-all",
        "colors": "--icon-color-1:#0ea5e9; --icon-color-2:#0284c7; --icon-color-rgb:14,165,233;",
        "en": "Manage client responses seamlessly. Let the AI automatically read incoming replies and draft contextual responses, or take manual control to write and send highly personalized follow-ups directly from the dashboard.",
        "bn": "ক্লায়েন্টের রিপ্লাই ম্যানেজ করুন খুব সহজেই। ইনবক্সে আসা মেইলের রিপ্লাই AI দিয়ে অটোমেটিকভাবে ড্রাফট করাতে পারবেন, অথবা ম্যানুয়ালি টাইপ করে নিজের মতো করে প্রফেশনাল রিপ্লাই পাঠাতে পারবেন।",
        "htu_en": "Open any replied email. Click 'Generate AI Reply' for an automated draft, or manually type your response and hit Send.",
        "htu_bn": "যেকোনো রিপ্লাই ওপেন করে 'Generate AI Reply' বাটনে ক্লিক করলে অটোমেটিক রিপ্লাই রেডি হবে, অথবা ম্যানুয়ালি লিখে Send করুন।"
    },
    {
        "title": "10. Anti-Spam Humanized Delays",
        "icon": "fa-clock",
        "colors": "--icon-color-1:#eab308; --icon-color-2:#ca8a04; --icon-color-rgb:234,179,8;",
        "en": "Evade rigorous anti-spam algorithms. The system automatically randomizes sending intervals between your configured boundaries, while you manually define the Min and Max delay ranges to dictate the pacing.",
        "bn": "অ্যান্টি-স্প্যাম বাইপাস করার জন্য হিউম্যানাইজড ডিলে। আপনি ম্যানুয়ালি Min এবং Max গ্যাপ সেট করে দেবেন, আর সিস্টেম অটোমেটিক্যালি সেই গ্যাপের ভেতর র‍্যান্ডম সেকেন্ড পর পর মেইল পাঠাবে, যাতে কোনো রোবটিক প্যাটার্ন ধরা না পড়ে।",
        "htu_en": "Before Campaign launch, manually set Min (e.g. 60s) and Max Delay (e.g. 120s). The engine auto-randomizes delays in between.",
        "htu_bn": "ক্যাম্পেইন চালুর আগে ম্যানুয়ালি Min এবং Max Delay সেকেন্ড সেট করুন। সিস্টেম এর মাঝে অটোমেটিক র‍্যান্ডম টাইম গ্যাপ তৈরি করে মেইল সেন্ড করবে।"
    },
    {
        "title": "11. Background IMAP Sync & Analytics",
        "icon": "fa-chart-line",
        "colors": "--icon-color-1:#22c55e; --icon-color-2:#16a34a; --icon-color-rgb:34,197,94;",
        "en": "True 360-degree analytics. The system automatically syncs via IMAP in the background to securely detect replies without pixel tracking. Meanwhile, you can manually analyze campaign metrics from the visual dashboard.",
        "bn": "থার্ড-পার্টি পিক্সেল ছাড়াই IMAP সিঙ্ক করে ডাইরেক্ট ইনবক্স থেকে ট্র্যাকিং। সিস্টেম ব্যাকগ্রাউন্ডে অটোমেটিক্যালি রিপ্লাই ট্র্যাক করবে, আর আপনি ড্যাশবোর্ড থেকে ম্যানুয়ালি আপনার ক্যাম্পেইনের সম্পূর্ণ পারফরম্যান্স অ্যানালাইজ করতে পারবেন।",
        "htu_en": "Input IMAP details manually when adding an account. The system will automatically fetch open/reply data in the background.",
        "htu_bn": "অ্যাকাউন্ট যোগ করার সময় ম্যানুয়ালি IMAP পোর্ট ও সার্ভার দিয়ে দিন। এরপর সিস্টেম অটোমেটিক্যালি ব্যাকগ্রাউন্ডে ডাটা সিঙ্ক করবে।"
    },
    {
        "title": "12. Campaign Scheduling & Timezone Mastery",
        "icon": "fa-calendar-days",
        "colors": "--icon-color-1:#8b5cf6; --icon-color-2:#7c3aed; --icon-color-rgb:139,92,246;",
        "en": "Precision timing for maximum conversion. The automated chron-job resets all daily limits precisely at midnight Bangladesh Time (BST). You can also manually schedule campaigns to trigger on specific days and times.",
        "bn": "অটোমেটিক ডাটা রিসেট এবং ম্যানুয়াল শিডিউলিং। প্রতিদিন রাত ১২টায় বাংলাদেশ সময় অনুযায়ী সিস্টেম অটোমেটিক সব লিমিট রিসেট করে দেবে। এছাড়া আপনি চাইলে ম্যানুয়ালি নির্দিষ্ট দিন ও সময়ে ক্যাম্পেইন শিডিউল করে রাখতে পারেন।",
        "htu_en": "Limits auto-reset at 12:00 AM BST. Manually select active sending days (Mon-Fri) in the Campaign creation settings.",
        "htu_bn": "রাত ১২টায় লিমিট অটো-রিসেট হবে। ক্যাম্পেইন বানানোর সময় কোন কোন দিন মেইল যাবে, তা ম্যানুয়ালি টিক দিয়ে সিলেক্ট করুন।"
    },
    {
        "title": "13. Spintax & Hyper-Personalization",
        "icon": "fa-wand-magic-sparkles",
        "colors": "--icon-color-1:#f59e0b; --icon-color-2:#d97706; --icon-color-rgb:245,158,11;",
        "en": "Avoid duplicate content penalties. Manually insert Spintax {Hi|Hello|Hey} into your emails, and the engine automatically generates unique variations for every single lead on the fly.",
        "bn": "স্পিনট্যাক্স সাপোর্ট এবং পার্সোনালাইজেশন। আপনি ম্যানুয়ালি {Hi|Hello|Hey} ফরম্যাটে টেক্সট দিয়ে রাখলে, সিস্টেম অটোমেটিক্যালি প্রত্যেকটি লিডের জন্য আলাদা আলাদা ইউনিক ভেরিয়েশন তৈরি করে মেইল পাঠাবে।",
        "htu_en": "Manually write {{FirstName}} or Spintax {A|B} in the editor. The system auto-replaces these variables during sending.",
        "htu_bn": "এডিটরে ম্যানুয়ালি স্পিনট্যাক্স বা ভেরিয়েবল লিখুন। মেইল যাওয়ার সময় সিস্টেম অটোমেটিক্যালি সেগুলো চেঞ্জ করে সেন্ড করবে।"
    },
    {
        "title": "14. State-of-the-Art Visual Template Engine",
        "icon": "fa-laptop-code",
        "colors": "--icon-color-1:#ec4899; --icon-color-2:#db2777; --icon-color-rgb:236,72,153;",
        "en": "Build stunning newsletters instantly. Use 100+ auto-responsive pre-built layouts, or switch to the Advanced Source Code view to manually inject your own highly-customized HTML & CSS.",
        "bn": "ভিজ্যুয়াল নিউজলেটার বিল্ডার। সিস্টেমের ১০০+ অটো-রেস্পন্সিভ টেমপ্লেট দিয়ে নিমিষেই ডিজাইন করতে পারবেন, অথবা Source কোড অন করে ম্যানুয়ালি নিজের মতো HTML ও CSS দিয়ে সম্পূর্ণ কাস্টম ডিজাইন তৈরি করতে পারবেন।",
        "htu_en": "Choose auto-layouts from the Gallery, or click '< >' to manually write HTML/CSS code.",
        "htu_bn": "গ্যালারি থেকে অটো টেমপ্লেট সিলেক্ট করুন অথবা '< >' আইকনে ক্লিক করে ম্যানুয়ালি HTML কোড লিখুন।"
    }
]

html_blocks = []
for idx, feature in enumerate(features):
    block = f'''
<div class="about-card" style="{feature['colors']}">
    <div class="about-icon-wrapper"><i class="fa-solid {feature['icon']}"></i></div>
    <h3 class="about-title">{feature['title']}</h3>
    <p class="about-text"><strong>English:</strong> {feature['en']}</p>
    <p class="about-text bn"><strong>Bangla:</strong> {feature['bn']}</p>

    <div class="htu-container" style="margin-top: auto; padding-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1); perspective: 1000px;">
        <button class="htu-btn" onclick="toggle3DHowToUse(this)" style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: transparent; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.3s; background: rgba(0,0,0,0.02); box-shadow: 0 2px 5px rgba(0,0,0,0.01);">
            <span style="font-weight: 600; color: var(--text); font-size: 15px; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-wand-magic-sparkles" style="color: var(--p);"></i> How to Use (Auto & Manual)</span>
            <i class="fa-solid fa-chevron-down" style="color: var(--text-muted); font-size: 14px; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);"></i>
        </button>
        <div class="htu-content" style="max-height: 0; opacity: 0; transform-origin: top; transform: rotateX(-90deg); transition: max-height 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; background: rgba(var(--icon-color-rgb), 0.05); border-left: 3px solid var(--icon-color-1); border-radius: 0 8px 8px 0; margin-top: 12px;">
            <div style="padding: 16px;">
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 12px;"><strong>English:</strong> {feature['htu_en']}</p>
                <p style="font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 0;"><strong>Bangla:</strong> {feature['htu_bn']}</p>
            </div>
        </div>
    </div>
</div>
'''
    html_blocks.append(block)

# add the creator block at the end
admin_block = f'''
<div class="about-card" style="grid-column: 1 / -1; --icon-color-1:#4f46e5; --icon-color-2:#ec4899; --icon-color-rgb:79,70,229; background: linear-gradient(135deg, rgba(79, 70, 229, 0.05), rgba(236, 72, 153, 0.05)); border: 1px solid rgba(79, 70, 229, 0.2);">
    <div class="about-icon-wrapper" style="margin-left:auto; margin-right:auto; margin-bottom: 16px;"><i class="fa-solid fa-user-shield"></i></div>
    <h3 class="about-title" style="text-align:center;">Engineered & Administered by Monem Rahman Zisan</h3>
    <p class="about-text" style="text-align:center; max-width: 800px; margin: 0 auto 12px;"><strong>English:</strong> Architected and engineered by Monem Rahman Zisan. Includes a Secure Admin Dashboard with JWT token-based authentication and strict RBAC, accessible exclusively by the creator to manage automated jobs and ensure manual overriding capabilities for maximum security.</p>
    <p class="about-text bn" style="text-align:center; max-width: 800px; margin: 0 auto;"><strong>Bangla:</strong> সিস্টেমটি ডিজাইন এবং তৈরি করেছেন মোনেম রহমান জিসান। অটোমেটেড প্রসেস এবং ম্যানুয়াল সিকিউরিটি মেইনটেইন করার জন্য রয়েছে স্পেশাল অ্যাডমিন ড্যাশবোর্ড, যা শুধুমাত্র ক্রিয়েটর অ্যাক্সেস করতে পারবেন।</p>
</div>
'''
html_blocks.append(admin_block)

features_html = "".join(html_blocks)

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

end_grid = html.rfind('</div>', start_grid, end_idx)
end_grid = html.rfind('</div>', start_grid, end_grid)

new_html = html[:start_grid] + '<div class="about-grid">\n' + features_html + '\n</div>\n          </div>\n\n' + html[end_idx:]

with codecs.open('frontend/index.html', 'w', 'utf-8') as f:
    f.write(new_html)

print("About section comprehensively updated!")
