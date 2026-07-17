import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add CSS
    css = """
    /* How to Use Modal CSS */
    .how-to-use-btn {
        margin-top: 15px;
        background: var(--icon-color-1, #3b82f6);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        transition: opacity 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    .how-to-use-btn:hover {
        opacity: 0.9;
    }
    .htu-modal-overlay {
        display: none;
        position: fixed;
        inset: 0;
        background: rgba(15,23,42,0.8);
        z-index: 20000;
        backdrop-filter: blur(4px);
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    .htu-modal {
        background: var(--surface);
        width: 100%;
        max-width: 600px;
        border-radius: 12px;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
        border: 1px solid var(--border);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        max-height: 90vh;
    }
    .htu-header {
        background: #f1f5f9;
        padding: 16px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid var(--border);
    }
    .htu-title {
        font-weight: 700;
        font-size: 16px;
        color: #0f172a;
    }
    .htu-body {
        padding: 24px;
        overflow-y: auto;
        font-size: 14px;
        color: #334155;
        line-height: 1.6;
    }
    .htu-body h4 {
        margin-top: 0;
        color: #0f172a;
        margin-bottom: 12px;
        font-size: 15px;
    }
    .htu-body p {
        margin-bottom: 16px;
    }
    .htu-body ul {
        padding-left: 20px;
        margin-bottom: 16px;
    }
    .htu-body li {
        margin-bottom: 8px;
    }
    """
    
    if ".htu-modal-overlay" not in content:
        content = content.replace('</style>', css + '\n</style>')

    # 2. Add buttons to each card
    titles = re.findall(r'<h3 class="about-title">(\d+)\.\s+(.*?)</h3>', content)
    
    for i, title_text in titles:
        pattern = r'(<h3 class="about-title">' + i + r'\.\s+' + re.escape(title_text) + r'</h3>.*?)(</div>\s*<div class="about-card"|</div>\s*</div>\s*</div>)'
        
        def repl(m):
            card_inner = m.group(1)
            end_html = m.group(2)
            if "how-to-use-btn" not in card_inner:
                btn = f'\n                    <button class="how-to-use-btn" onclick="openHowToModal({i})"><i class="fa-solid fa-circle-info"></i> How to Use / কীভাবে ব্যবহার করবেন</button>\n                '
                return card_inner + btn + end_html
            return m.group(0)

        content = re.sub(pattern, repl, content, flags=re.DOTALL)


    # 3. Add Modal HTML and JS
    modal_html = """
    <!-- How To Use Modal -->
    <div id="htu-modal-overlay" class="htu-modal-overlay">
        <div class="htu-modal">
            <div class="htu-header">
                <div class="htu-title" id="htu-title">How to Use</div>
                <button onclick="closeHowToModal()" style="background:transparent; border:none; color:var(--text-muted); font-size:18px; cursor:pointer;"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="htu-body" id="htu-body">
                Loading...
            </div>
        </div>
    </div>

    <script>
    const htuData = {
        1: {
            title: "Multi-Sender & Account Rotation",
            body: `
                <h4>English</h4>
                <p><strong>How to use:</strong></p>
                <ul>
                    <li>Go to the <strong>Sending Accounts</strong> tab.</li>
                    <li>Click <strong>+ Add Account</strong> and enter your SMTP details (Gmail, Zoho, etc.).</li>
                    <li>Add multiple accounts (e.g., 3-5 accounts) and make sure they are 'Active'.</li>
                    <li>When you send a campaign, the system will automatically rotate between these active accounts to send emails, keeping your daily limits safe!</li>
                </ul>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>কীভাবে ব্যবহার করবেন:</strong></p>
                <ul>
                    <li>প্রথমে <strong>Sending Accounts</strong> ট্যাবে যান।</li>
                    <li><strong>+ Add Account</strong> এ ক্লিক করে আপনার ইমেইল (Gmail/Webmail) অ্যাড করুন।</li>
                    <li>এভাবে ৩-৫টি বা তার বেশি অ্যাকাউন্ট অ্যাড করে 'Active' রাখুন।</li>
                    <li>ক্যাম্পেইন সেন্ড করার সময় সিস্টেম নিজে থেকেই এই অ্যাকাউন্টগুলোর মধ্যে রোটেট করে (ঘুরিয়ে ঘুরিয়ে) ইমেইল সেন্ড করবে, ফলে কোনো একটি অ্যাকাউন্টে অতিরিক্ত চাপ পড়বে না!</li>
                </ul>
            `
        },
        2: {
            title: "Auto-Warmup & Smart Limits",
            body: `
                <h4>English</h4>
                <p><strong>How to use:</strong></p>
                <ul>
                    <li>In the <strong>Sending Accounts</strong> tab, click the <strong>Edit</strong> (pencil) icon on an account.</li>
                    <li>Turn on the <strong>Warmup</strong> toggle.</li>
                    <li>Set your starting limit (e.g., 5) and Daily Increment (e.g., 2).</li>
                    <li>The system will automatically send warmup emails every day and increase the limit daily at midnight to build your domain reputation!</li>
                </ul>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>কীভাবে ব্যবহার করবেন:</strong></p>
                <ul>
                    <li><strong>Sending Accounts</strong> ট্যাবে গিয়ে যেকোনো অ্যাকাউন্টের <strong>Edit</strong> (পেন্সিল) আইকনে ক্লিক করুন।</li>
                    <li><strong>Warmup</strong> অপশনটি অন করুন।</li>
                    <li>Starting Limit (যেমন: ৫) এবং Daily Increment (যেমন: ২) সেট করে সেভ করুন।</li>
                    <li>সিস্টেম নিজে থেকেই প্রতিদিন ওয়ার্মআপ ইমেইল সেন্ড করবে এবং রাত ১২টায় অটোমেটিক্যালি লিমিট বাড়িয়ে আপনার ডোমেইনের রেপুটেশন বৃদ্ধি করবে!</li>
                </ul>
            `
        },
        3: {
            title: "Advanced Deliverability Check",
            body: `
                <h4>English</h4>
                <p><strong>How to use:</strong></p>
                <ul>
                    <li>Go to the <strong>Deliverability</strong> tab from the sidebar.</li>
                    <li>You will see a Health Score (0-100) for your domain based on bounce rates and inbox placement.</li>
                    <li>Check the <strong>Recommendations</strong> section to see what actions you should take (e.g., pausing campaigns, cleaning lists).</li>
                </ul>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>কীভাবে ব্যবহার করবেন:</strong></p>
                <ul>
                    <li>মেনু থেকে <strong>Deliverability</strong> ট্যাবে যান।</li>
                    <li>এখানে আপনার অ্যাকাউন্টের Health Score (0-100) দেখতে পাবেন, যা বাউন্স রেট এবং ইনবক্স প্লেসমেন্টের উপর ভিত্তি করে তৈরি হয়।</li>
                    <li><strong>Recommendations</strong> অংশটি চেক করুন, সেখানে বলা থাকবে আপনার ডোমেইন সুরক্ষিত রাখতে কী কী পদক্ষেপ নেওয়া উচিত।</li>
                </ul>
            `
        },
        4: {
            title: "Audience & Auto-Cleaning",
            body: `
                <h4>English</h4>
                <p><strong>How to use:</strong></p>
                <ul>
                    <li>Go to the <strong>Audience</strong> tab.</li>
                    <li>Upload your CSV file containing names and emails.</li>
                    <li>The system automatically filters out invalid formats and duplicate emails during upload.</li>
                    <li>When a sent email bounces, the system auto-cleans that contact so you never send to a dead email again!</li>
                </ul>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>কীভাবে ব্যবহার করবেন:</strong></p>
                <ul>
                    <li><strong>Audience</strong> ট্যাবে গিয়ে আপনার কন্টাক্ট লিস্ট (CSV) আপলোড করুন।</li>
                    <li>আপলোড করার সময়ই সিস্টেম ডুপ্লিকেট এবং ভুল ইমেইলগুলো অটোমেটিক বাদ দিয়ে দিবে।</li>
                    <li>এছাড়া কোনো ইমেইল সেন্ড করার পর যদি বাউন্স (Bounce) হয়, তবে সিস্টেম সেটি অটোমেটিক্যালি ক্লিন করে দিবে যাতে পরবর্তীতে আর ওই ডেড ইমেইলে মেইল না যায়!</li>
                </ul>
            `
        },
        5: {
            title: "Cold Email & Spintax",
            body: `
                <h4>English</h4>
                <p><strong>How to use:</strong></p>
                <ul>
                    <li>When writing a campaign email, you can use spintax like this: <code>{Hi|Hello|Hey} {first_name}, how are you?</code></li>
                    <li>The system will randomly select one of the words inside the brackets for each recipient.</li>
                    <li>This makes every email completely unique and drastically lowers your spam score!</li>
                </ul>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>কীভাবে ব্যবহার করবেন:</strong></p>
                <ul>
                    <li>ক্যাম্পেইন ইমেইল লেখার সময় আপনি Spintax ব্যবহার করতে পারেন। যেমন: <code>{Hi|Hello|Hey} {first_name}</code></li>
                    <li>সিস্টেম প্রতিটি ইউজারের কাছে ব্র্যাকেটের ভেতরের যেকোনো একটি শব্দ র‍্যান্ডমলি সিলেক্ট করে পাঠাবে।</li>
                    <li>এর ফলে আপনার প্রতিটি ইমেইল ইউনিক হবে এবং স্প্যামে যাওয়ার চান্স জিরো হয়ে যাবে!</li>
                </ul>
            `
        },
        6: {
            title: "Visual Newsletter Builder",
            body: `
                <h4>English</h4>
                <p><strong>How to use:</strong></p>
                <ul>
                    <li>Go to the <strong>Templates</strong> tab and click <strong>Create Template</strong>.</li>
                    <li>Select <strong>Drag & Drop Builder</strong> instead of Simple Text.</li>
                    <li>Drag text, images, buttons, and columns from the right sidebar onto your canvas.</li>
                    <li>Save it and select this template when creating your Campaign!</li>
                </ul>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>কীভাবে ব্যবহার করবেন:</strong></p>
                <ul>
                    <li><strong>Templates</strong> ট্যাবে গিয়ে <strong>Create Template</strong> এ ক্লিক করুন।</li>
                    <li>Simple Text এর বদলে <strong>Drag & Drop Builder</strong> সিলেক্ট করুন।</li>
                    <li>ডানপাশের প্যানেল থেকে টেক্সট, ইমেজ, বাটন ইত্যাদি টেনে এনে সুন্দর ইমেইল ডিজাইন করুন এবং সেভ করুন!</li>
                </ul>
            `
        },
        7: {
            title: "Next-Gen AI Features",
            body: `
                <h4>English</h4>
                <p><strong>How to use:</strong></p>
                <ul>
                    <li>In the Campaign or Template creator, click the <strong>AI Write</strong> button.</li>
                    <li>Type a short prompt (e.g., "Write a cold email selling web design services").</li>
                    <li>The AI will instantly generate a professional email with subject lines and spintax variations included!</li>
                </ul>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>কীভাবে ব্যবহার করবেন:</strong></p>
                <ul>
                    <li>ক্যাম্পেইন বা টেমপ্লেট বানানোর সময় <strong>AI Write</strong> বাটনে ক্লিক করুন।</li>
                    <li>আপনি কী নিয়ে ইমেইল লিখতে চান তা সংক্ষেপে লিখুন (যেমন: "ওয়েব ডিজাইন সার্ভিস বিক্রির জন্য একটি কোল্ড ইমেইল")।</li>
                    <li>এআই সাথে সাথেই আপনার জন্য প্রফেশনাল ইমেইল, সাবজেক্ট এবং Spintax সহ লিখে দিবে!</li>
                </ul>
            `
        },
        8: {
            title: "Campaign Scheduling",
            body: `
                <h4>English</h4>
                <p><strong>How to use:</strong></p>
                <ul>
                    <li>Go to the <strong>Campaigns</strong> tab and click <strong>Create Campaign</strong>.</li>
                    <li>At the bottom of the form, find the <strong>Schedule Option</strong>.</li>
                    <li>Select a specific date and time for when you want the emails to start sending.</li>
                    <li>The system will automatically start the campaign exactly at your scheduled time!</li>
                </ul>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>কীভাবে ব্যবহার করবেন:</strong></p>
                <ul>
                    <li><strong>Campaigns</strong> থেকে নতুন ক্যাম্পেইন তৈরি করার সময় একদম নিচে <strong>Schedule Option</strong> দেখতে পাবেন।</li>
                    <li>সেখানে আপনার কাঙ্ক্ষিত ডেট এবং টাইম সিলেক্ট করে দিন।</li>
                    <li>সিস্টেম ঠিক ওই সময়েই অটোমেটিক্যালি ইমেইল সেন্ড করা শুরু করে দিবে, আপনার পিসি অন রাখার কোনো প্রয়োজন নেই!</li>
                </ul>
            `
        },
        9: {
            title: "IMAP Processing: Bounces & Replies",
            body: `
                <h4>English</h4>
                <p><strong>How to use:</strong></p>
                <ul>
                    <li>When adding a Sending Account, make sure you provide your <strong>IMAP App Password</strong>.</li>
                    <li>The system's background worker will regularly check your inbox.</li>
                    <li>If it detects a "Bounce" (Delivery Failed), it will mark the contact as bounced. If it detects a human reply, it will mark it as "Replied".</li>
                </ul>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>কীভাবে ব্যবহার করবেন:</strong></p>
                <ul>
                    <li>Sending Account অ্যাড করার সময় অবশ্যই <strong>IMAP Password</strong> দিয়ে সেভ করবেন।</li>
                    <li>সিস্টেম ব্যাকগ্রাউন্ডে রেগুলার আপনার ইনবক্স চেক করতে থাকবে।</li>
                    <li>কেউ রিপ্লাই দিলে বা কোনো ইমেইল বাউন্স করলে সিস্টেম অটোমেটিক্যালি সেটা ডিটেক্ট করে ড্যাশবোর্ডে আপডেট করে দিবে!</li>
                </ul>
            `
        },
        10: {
            title: "Real-time Analytics",
            body: `
                <h4>English</h4>
                <p><strong>How to use:</strong></p>
                <ul>
                    <li>Just go to the <strong>Dashboard</strong> or <strong>Campaigns</strong> tab.</li>
                    <li>Click on a running or completed campaign.</li>
                    <li>You will see beautiful charts showing exactly how many people Opened, Clicked, Replied, and Bounced in real-time.</li>
                </ul>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>কীভাবে ব্যবহার করবেন:</strong></p>
                <ul>
                    <li><strong>Dashboard</strong> বা <strong>Campaigns</strong> ট্যাবে গিয়ে যেকোনো ক্যাম্পেইনের ওপর ক্লিক করুন।</li>
                    <li>সেখানে আপনি লাইভ চার্ট দেখতে পাবেন—কতজন ওপেন করেছে, ক্লিক করেছে বা রিপ্লাই দিয়েছে তার রিয়েল-টাইম স্ট্যাটিস্টিক্স।</li>
                </ul>
            `
        },
        11: {
            title: "AI Reply Management",
            body: `
                <h4>English</h4>
                <p><strong>How to use:</strong></p>
                <ul>
                    <li>Go to the <strong>Inbox</strong> tab to see all replies from your prospects.</li>
                    <li>Click on a reply to open the conversation.</li>
                    <li>You can read their message and use the AI Draft button to instantly generate a professional reply, then send it right from the dashboard!</li>
                </ul>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>কীভাবে ব্যবহার করবেন:</strong></p>
                <ul>
                    <li>কাস্টমারদের সব রিপ্লাই দেখতে <strong>Inbox</strong> ট্যাবে যান।</li>
                    <li>যেকোনো মেসেজে ক্লিক করে চ্যাট ওপেন করুন।</li>
                    <li>মেসেজ পড়ার পর AI বাটনে ক্লিক করে সাথে সাথেই অটোমেটিক প্রফেশনাল রিপ্লাই জেনারেট করে ড্যাশবোর্ড থেকেই সেন্ড করতে পারবেন!</li>
                </ul>
            `
        },
        12: {
            title: "Dynamic Human-like Delays",
            body: `
                <h4>English</h4>
                <p><strong>How to use:</strong></p>
                <ul>
                    <li>You don't need to do anything manually!</li>
                    <li>Whenever the system sends a batch of emails, it automatically waits for a random number of seconds (e.g., 30s to 90s) between each email.</li>
                    <li>This tricks Google and Outlook into thinking a real human is sending the emails, keeping you out of the spam folder.</li>
                </ul>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>কীভাবে ব্যবহার করবেন:</strong></p>
                <ul>
                    <li>এর জন্য আপনাকে ম্যানুয়ালি কিছুই করতে হবে না!</li>
                    <li>সিস্টেম যখন ইমেইল পাঠায়, তখন প্রতিটি ইমেইলের মাঝখানে অটোমেটিক্যালি কিছু সেকেন্ড (যেমন ৩০-৯০ সেকেন্ড) র‍্যান্ডমলি ওয়েট করে।</li>
                    <li>এর ফলে জিমেইল বা আউটলুক বুঝতে পারে না যে এটি কোনো সফটওয়্যার, তারা ভাবে কোনো মানুষ ইমেইল পাঠাচ্ছে। ফলে স্প্যামে যাওয়ার রিস্ক জিরো!</li>
                </ul>
            `
        },
        13: {
            title: "100+ Responsive Layouts",
            body: `
                <h4>English</h4>
                <p><strong>How to use:</strong></p>
                <ul>
                    <li>Go to <strong>Templates</strong> > Create Template > Drag & Drop Builder.</li>
                    <li>Inside the builder, click the <strong>Blocks</strong> or <strong>Templates</strong> section on the right side.</li>
                    <li>You will find hundreds of pre-designed sections. Just drag them into your email and change the text/images!</li>
                </ul>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>কীভাবে ব্যবহার করবেন:</strong></p>
                <ul>
                    <li><strong>Templates</strong> থেকে ড্র্যাগ অ্যান্ড ড্রপ বিল্ডার ওপেন করুন।</li>
                    <li>ডানদিকের মেনু থেকে Blocks বা Templates অপশনে গেলে প্রচুর রেডিমেড ডিজাইন দেখতে পাবেন।</li>
                    <li>সেগুলো টেনে এনে আপনার পছন্দমতো টেক্সট ও ছবি বসিয়ে দিলেই সুন্দর লেআউট রেডি!</li>
                </ul>
            `
        },
        14: {
            title: "Timezone-Aware Auto Reset",
            body: `
                <h4>English</h4>
                <p><strong>How to use:</strong></p>
                <ul>
                    <li>The system is fully automated.</li>
                    <li>Every night at exactly 12:00 AM (Bangladesh Time UTC+6), the system will reset all your "Sent Today" counters back to 0.</li>
                    <li>It will also automatically increase your warmup limits based on your daily increment settings!</li>
                </ul>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>কীভাবে ব্যবহার করবেন:</strong></p>
                <ul>
                    <li>এটি সম্পূর্ণ অটোমেটেড একটি ফিচার।</li>
                    <li>প্রতিদিন ঠিক রাত ১২টায় (বাংলাদেশ সময় অনুযায়ী) সিস্টেম আপনার সব অ্যাকাউন্টের "Sent Today" কাউন্ট জিরো (0) করে দিবে।</li>
                    <li>একই সাথে ওয়ার্মআপের ইনক্রিমেন্ট লিমিটও অটোমেটিক বাড়িয়ে দিবে, আপনাকে ম্যানুয়ালি কিছুই করতে হবে না!</li>
                </ul>
            `
        },
        15: {
            title: "Engineered by Monem Rahman Zisan",
            body: `
                <h4>English</h4>
                <p><strong>About the Developer:</strong></p>
                <p>This software was custom-engineered by Monem Rahman Zisan to solve the biggest challenges in cold email outreach. By utilizing modern architectures, it handles scaling, bypassing spam filters, and maximizing ROI seamlessly.</p>
                <p>For custom features, support, or bug reporting, you can directly contact the developer.</p>
                <hr style="margin:20px 0; border:none; border-top:1px solid var(--border);">
                <h4>বাংলা (Bangla)</h4>
                <p><strong>ডেভেলপার সম্পর্কে:</strong></p>
                <p>কোল্ড ইমেইলের সব ধরনের লিমিটেশন এবং স্প্যাম ফিল্টার বাইপাস করার অত্যাধুনিক প্রযুক্তি ব্যবহার করে সম্পূর্ণ সিস্টেমটি তৈরি করেছেন মোনেম রহমান জিসান।</p>
                <p>যেকোনো ধরনের কাস্টম ফিচার, সাপোর্ট বা বাস্গ ফিক্সিং এর জন্য সরাসরি ডেভেলপারের সাথে যোগাযোগ করতে পারেন।</p>
            `
        }
    };

    function openHowToModal(id) {
        const data = htuData[id];
        if(!data) return;
        document.getElementById('htu-title').innerText = data.title;
        document.getElementById('htu-body').innerHTML = data.body;
        document.getElementById('htu-modal-overlay').style.display = 'flex';
    }

    function closeHowToModal() {
        document.getElementById('htu-modal-overlay').style.display = 'none';
    }

    // Close on outside click
    document.getElementById('htu-modal-overlay').addEventListener('click', function(e) {
        if(e.target === this) closeHowToModal();
    });
    </script>
    """
    
    if "openHowToModal" not in content:
        content = content.replace('</body>', modal_html + '\n</body>')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    main()
