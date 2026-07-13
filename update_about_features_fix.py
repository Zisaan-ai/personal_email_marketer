import codecs
import re

with codecs.open('frontend/index.html', 'r', 'utf-8') as f:
    html = f.read()

# We need to fix the Bengali text (it became ????)
# Since I replaced the entire grid previously, let me just rewrite the grid content properly.

start_grid = html.find('<div class="about-grid">')
end_grid = html.find('</div>\n          </div>', start_grid)
if end_grid == -1:
    # find the last closing div of the grid
    end_grid = html.find('</div>', html.find('19. Engineered by Monem Rahman Zisan'))
    if end_grid != -1:
        end_grid = html.find('</div>', end_grid + 1)
        end_grid = html.find('</div>', end_grid + 1)

new_grid_content = '''
              <div class="about-grid">
                  <div class="about-card" style="--icon-color-1:#10b981; --icon-color-2:#059669; --icon-color-rgb:16,185,129;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-users-gear"></i></div>
                      <h3 class="about-title">1. Multi-Sender & Account Rotation</h3>
                      <p class="about-text"><strong>English:</strong> Seamlessly integrate multiple SMTP accounts. The system intelligently rotates through active senders, distributing the workload and protecting individual account reputation.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> একাধিক SMTP অ্যাকাউন্ট একসাথে ব্যবহার করুন। সিস্টেম নিজে থেকেই অ্যাকাউন্টগুলো ঘুরিয়ে ঘুরিয়ে ইমেইল পাঠায়, যার ফলে স্প্যামে যাওয়ার ঝুঁকি কমে এবং অ্যাকাউন্টের রেপুটেশন ঠিক থাকে।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#3b82f6; --icon-color-2:#2563eb; --icon-color-rgb:59,130,246;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-arrow-trend-up"></i></div>
                      <h3 class="about-title">2. Auto-Warmup & Smart Limits</h3>
                      <p class="about-text"><strong>English:</strong> Establish domain trust automatically. The engine algorithmically increases daily sending limits for new accounts, creating organic sending patterns that ISPs trust.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> ডোমেইনের ট্রাস্ট স্বয়ংক্রিয়ভাবে বাড়ান। সিস্টেম নতুন অ্যাকাউন্টের জন্য প্রতিদিন একটু একটু করে ইমেইল পাঠানোর পরিমাণ বাড়ায়, যা আইএসপি (ISP) এর কাছে একদম স্বাভাবিক মনে হয়।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#8b5cf6; --icon-color-2:#7c3aed; --icon-color-rgb:139,92,246;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-shield-check"></i></div>
                      <h3 class="about-title">3. Advanced Deliverability Check</h3>
                      <p class="about-text"><strong>English:</strong> Prevent campaigns from landing in spam. The pre-flight scanner identifies risky words and validates DNS records (SPF, DKIM, DMARC) prior to launch.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> ইমেইল স্প্যামে যাওয়া রোধ করুন। ইমেইল পাঠানোর আগেই সিস্টেম স্প্যামি ওয়ার্ড এবং ডিএনএস রেকর্ড (SPF, DKIM, DMARC) স্ক্যান করে আপনাকে সতর্ক করবে।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#f59e0b; --icon-color-2:#d97706; --icon-color-rgb:245,158,11;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-address-book"></i></div>
                      <h3 class="about-title">4. Audience & Auto-Cleaning</h3>
                      <p class="about-text"><strong>English:</strong> Upload mass contact lists effortlessly. The system sanitizes your data, removing syntax errors, hard bounces, and strict duplicates to maintain a pristine audience database.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> হাজার হাজার কন্টাক্ট আপলোড করুন সহজেই। সিস্টেম নিজে থেকেই ডুপ্লিকেট, ভুল ফরমেট এবং হার্ড বাউন্স ইমেইলগুলো রিমুভ করে আপনার লিস্টকে একদম ফ্রেশ রাখবে।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#ec4899; --icon-color-2:#db2777; --icon-color-rgb:236,72,153;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-envelope-open-text"></i></div>
                      <h3 class="about-title">5. Cold Email & Spintax</h3>
                      <p class="about-text"><strong>English:</strong> Execute highly personalized cold outreach. Advanced Spintax support {Hello|Hi} combined with precise merge tags {{name}} ensures every recipient gets a unique message.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> কোল্ড ইমেইলের জন্য সেরা ফিচার! স্পিনট্যাক্স {Hello|Hi} এবং ডাইনামিক ট্যাগ {{name}} ব্যবহার করে প্রতিটি মানুষের কাছে একদম আলাদা ইমেইল পৌঁছানো নিশ্চিত করুন।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#14b8a6; --icon-color-2:#0d9488; --icon-color-rgb:20,184,166;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-pen-nib"></i></div>
                      <h3 class="about-title">6. Visual Newsletter Builder</h3>
                      <p class="about-text"><strong>English:</strong> Craft stunning emails without writing a single line of code. The powerful Drag & Drop Visual Builder lets you create, style, and save reusable HTML templates.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> কোনো কোডিং ছাড়াই চমৎকার ইমেইল ডিজাইন করুন। ড্র্যাগ অ্যান্ড ড্রপ (Drag & Drop) ভিজ্যুয়াল বিল্ডার দিয়ে যেকোনো ডিজাইন তৈরি করে সেভ করে রাখতে পারবেন।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#6366f1; --icon-color-2:#4f46e5; --icon-color-rgb:99,102,241;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-microchip"></i></div>
                      <h3 class="about-title">7. Next-Gen Gemini AI Features</h3>
                      <p class="about-text"><strong>English:</strong> Powered by Google's Gemini API, the integrated AI assistant generates compelling subject lines, high-converting email bodies, and optimizes your drafts instantly.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> গুগল জেমিনাই (Gemini) এপিআই যুক্ত করা হয়েছে! এআই অ্যাসিস্ট্যান্ট আপনার জন্য বেস্ট সাবজেক্ট লাইন এবং কনভার্টিং ইমেইল বডি এক ক্লিকেই লিখে দেবে।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#f43f5e; --icon-color-2:#e11d48; --icon-color-rgb:244,63,94;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-calendar-check"></i></div>
                      <h3 class="about-title">8. Campaign Scheduling</h3>
                      <p class="about-text"><strong>English:</strong> Launch campaigns on your terms. Set customized daily operating hours and bypass specific days of the week to maximize user engagement.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> আপনার সুবিধামতো ক্যাম্পেইন শিডিউল করুন। দিনে কখন মেইল যাবে এবং সপ্তাহের কোন দিনগুলোতে মেইল পাঠানো বন্ধ থাকবে, তা আপনিই ঠিক করে দিতে পারবেন।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#eab308; --icon-color-2:#ca8a04; --icon-color-rgb:234,179,8;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-reply-all"></i></div>
                      <h3 class="about-title">9. IMAP Bounces & Replies Processing</h3>
                      <p class="about-text"><strong>English:</strong> The background engine automatically connects to IMAP, detects hard bounces, reads incoming replies, and instantly removes them from active sequences to protect your score.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> ব্যাকগ্রাউন্ড ইঞ্জিন স্বয়ংক্রিয়ভাবে IMAP এর মাধ্যমে হার্ড বাউন্স এবং রিপ্লাই শনাক্ত করে। এরপর তাদের কাছে পরবর্তী মেইল পাঠানো বন্ধ করে দেয়, যা স্প্যাম রেট কমায়।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#8b5cf6; --icon-color-2:#7c3aed; --icon-color-rgb:139,92,246;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-chart-line"></i></div>
                      <h3 class="about-title">10. Real-time Analytics</h3>
                      <p class="about-text"><strong>English:</strong> Track accurate delivery, bounces, and replies in real-time. Link-redirection headers provide complete campaign performance visibility directly inside your dashboard.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> ড্যাশবোর্ডে লাইভ অ্যানালিটিক্স দেখুন। কয়টা সেন্ড হলো, কয়টা ওপেন বা বাউন্স হলো, সব ডেটা একদম রিয়েল-টাইমে দেখতে পাবেন।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#0ea5e9; --icon-color-2:#0284c7; --icon-color-rgb:14,165,233;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-robot"></i></div>
                      <h3 class="about-title">11. AI Reply Management</h3>
                      <p class="about-text"><strong>English:</strong> Gemini AI reads prospect replies and automatically categorizes them as Positive, Negative, or Out-of-Office, allowing you to prioritize high-intent leads.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> জেমিনাই এআই ইনকামিং রিপ্লাইগুলো পড়ে বুঝতে পারে কোনটি পজিটিভ, কোনটি নেগেটিভ বা Out-of-Office, যার ফলে আপনার লিড ম্যানেজমেন্ট অনেক সহজ হয়।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#64748b; --icon-color-2:#475569; --icon-color-rgb:100,116,139;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-hourglass-half"></i></div>
                      <h3 class="about-title">12. Dynamic Human-like Delays</h3>
                      <p class="about-text"><strong>English:</strong> Implement randomized delay intervals between messages to mirror human operational tempos, successfully bypassing pattern-detection firewalls on major mail service providers.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> অ্যান্টি-স্প্যাম ফায়ারওয়াল বাইপাস করতে ইমেইল পাঠানোর মাঝে রেন্ডম ডিলে (Random Delay) ব্যবহার করুন। সিস্টেম মানুষের মতোই স্বাভাবিক বিরতি দিয়ে ইমেইল পাঠায়।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#22c55e; --icon-color-2:#16a34a; --icon-color-rgb:34,197,94;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-layer-group"></i></div>
                      <h3 class="about-title">13. 100+ Responsive Layouts</h3>
                      <p class="about-text"><strong>English:</strong> Instantly utilize a comprehensive suite of pre-configured responsive layouts tailored for newsletters, SaaS platforms, corporate communications, and direct marketing events.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> বিভিন্ন ক্যাটাগরির শতাধিক রেডিমেড রেসপনসিভ টেমপ্লেট ডিজাইন থেকে আপনার পছন্দমতো ডিজাইনটি বেছে নিয়ে সরাসরি ব্যবহার করতে পারবেন।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#ef4444; --icon-color-2:#dc2626; --icon-color-rgb:239,68,68;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-clock-rotate-left"></i></div>
                      <h3 class="about-title">14. Timezone-Aware Auto Reset</h3>
                      <p class="about-text"><strong>English:</strong> Ensure systematic count resets exactly at Bangladesh Midnight (UTC+6) without manual intervention, maintaining your daily quotas seamlessly.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> আপনার ডেইলি ইমেইল লিমিট বাংলাদেশ সময় রাত ১২টা বাজলেই (Midnight) নিজে থেকেই রিসেট হয়ে জিরো হয়ে যায়, কোনো ম্যানুয়াল কাজের প্রয়োজন নেই।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#10b981; --icon-color-2:#059669; --icon-color-rgb:16,185,129;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-arrow-up-right-dots"></i></div>
                      <h3 class="about-title">15. Campaign Limits & Rolling Ramp Up</h3>
                      <p class="about-text"><strong>English:</strong> Calculate Ramp Up dynamically over a 7-day rolling window. Set precise daily limits per campaign, allowing the system to scale your sending safely behind the scenes.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> সিস্টেম আপনার গত ৭ দিনের ক্যাম্পেইন হিস্ট্রি চেক করে অটোমেটিক্যালি র্যাম্প-আপ ক্যালকুলেট করে, যার ফলে ডোমেইনের ট্রাস্ট বৃদ্ধি পায় এবং ইনবক্স রেট ১০০% থাকে।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#3b82f6; --icon-color-2:#2563eb; --icon-color-rgb:59,130,246;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-heart-pulse"></i></div>
                      <h3 class="about-title">16. Real-Time System Health Monitor</h3>
                      <p class="about-text"><strong>English:</strong> Built-in Health Monitor tracks CPU, Memory, Disk usage, and Database connection stability every few seconds, ensuring zero downtime for your server.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> লাইভ সিস্টেম হেলথ মনিটর, যা সার্ভারের CPU, Memory এবং ডাটাবেজ স্ট্যাটাস রিয়েল-টাইমে চেক করে, যাতে সার্ভার কখনো ডাউন না হয়।</p>
                  </div>

                  <div class="about-card" style="--icon-color-1:#a855f7; --icon-color-2:#9333ea; --icon-color-rgb:168,85,247;">
                      <div class="about-icon-wrapper"><i class="fa-solid fa-microchip"></i></div>
                      <h3 class="about-title">17. Smart State Management Engine</h3>
                      <p class="about-text"><strong>English:</strong> Background APScheduler Engine automatically manages campaign states (Draft -> Pending -> Running -> Completed), handling errors and restarts gracefully.</p>
                      <p class="about-text bn"><strong>Bangla:</strong> ব্যাকগ্রাউন্ড এপিএসডিউলার (APScheduler) ইঞ্জিন নিজে থেকেই ক্যাম্পেইন ম্যানেজ করে। ড্রাফট থেকে রানিং বা ফেইল হলে তা অটোমেটিক্যালি আপডেট হয়ে যায়।</p>
                  </div>

                  <div class="about-card" style="grid-column: 1 / -1; --icon-color-1:#4f46e5; --icon-color-2:#ec4899; --icon-color-rgb:79,70,229; background: linear-gradient(135deg, rgba(79, 70, 229, 0.05), rgba(236, 72, 153, 0.05)); border: 1px solid rgba(79, 70, 229, 0.2);">
                      <div class="about-icon-wrapper" style="margin-left:auto; margin-right:auto; margin-bottom: 16px;"><i class="fa-solid fa-user-shield"></i></div>
                      <h3 class="about-title" style="text-align:center;">18. Engineered & Administered by Monem Rahman Zisan</h3>
                      <p class="about-text" style="text-align:center; max-width: 800px; margin: 0 auto 12px;"><strong>English:</strong> Designed and engineered by Monem Rahman Zisan. Includes a Secure Admin Dashboard with JWT token-based authentication and strict RBAC, accessible exclusively by the creator to manage users and ensure maximum security.</p>
                      <p class="about-text bn" style="text-align:center; max-width: 800px; margin: 0 auto;"><strong>Bangla:</strong> ফ্রিল্যান্সার মোনেম রহমান জিসান কর্তৃক তৈরিকৃত। সিস্টেমের সম্পূর্ণ কন্ট্রোল এবং সিকিউরিটির জন্য একটি স্পেশাল অ্যাডমিন ড্যাশবোর্ড রয়েছে, যা শুধুমাত্র ডেভেলপার নিজেই ব্যবহার ও নিয়ন্ত্রণ করতে পারেন।</p>
                  </div>
'''

if start_grid != -1 and end_grid != -1:
    html = html[:start_grid] + new_grid_content + html[end_grid:]
    with codecs.open('frontend/index.html', 'w', 'utf-8') as f:
        f.write(html)
    print("Successfully updated grid and fixed Bengali text.")
else:
    print("Error: Could not find grid bounds.")
