window.EmailTemplateCategories = [
    {id: 'all', name: 'All Templates'},
    {id: 'Announcement', name: 'Announcement'},
    {id: 'Cold Email', name: 'Cold Email'},
    {id: 'E-Commerce', name: 'E-Commerce'},
    {id: 'Events', name: 'Events'},
    {id: 'Minimal', name: 'Minimal'},
    {id: 'Newsletter', name: 'Newsletter'},
    {id: 'Onboarding', name: 'Onboarding'},
    {id: 'Retention', name: 'Retention'},
    {id: 'SaaS', name: 'SaaS'},
    {id: 'Transactional', name: 'Transactional'}
];

window.EmailTemplates = [

// =====================================================
// CATEGORY: E-COMMERCE
// =====================================================
{
    id: 'sell_products',
    name: '🛍️ Product Launch',
    category: 'E-Commerce',
    subject: 'New Collection is Here!',
    blocks: [
        { type: 'image', content: '<img src="https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=600&h=300&q=80" style="max-width:100%;height:auto;display:block;border-radius:8px 8px 0 0;">' },
        { type: 'text', content: '<div style="background:#fff;padding:32px 28px;text-align:center;"><h1 style="font-family:Georgia,serif;font-size:28px;color:#1a1a1a;margin:0 0 12px;">Shop Our Newest Arrivals</h1><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#666;margin:0;line-height:1.7;">Discover the latest trends and upgrade your lifestyle today. Limited stock available.</p></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#059669;color:#fff;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;font-size:15px;letter-spacing:0.5px;">Shop Now →</a></div>' }
    ]
},
{
    id: 'flash_sale',
    name: '⚡ Flash Sale',
    category: 'E-Commerce',
    subject: '24 HOURS ONLY: 50% OFF!',
    blocks: [
        { type: 'text', content: '<div style="background:linear-gradient(135deg,#ef4444,#dc2626);padding:48px 24px;text-align:center;border-radius:8px 8px 0 0;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;color:rgba(255,255,255,0.8);letter-spacing:3px;text-transform:uppercase;margin:0 0 8px;">Limited Time Offer</p><h1 style="font-family:Georgia,serif;font-size:48px;color:#fff;margin:0 0 8px;font-weight:900;">50% OFF</h1><p style="font-family:Helvetica,Arial,sans-serif;font-size:18px;color:rgba(255,255,255,0.9);margin:0;">Everything Sitewide</p></div>' },
        { type: 'text', content: '<div style="background:#fff;padding:28px;text-align:center;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#333;margin:0 0 16px;">Hurry! This offer expires in <strong>24 hours</strong>. Use code at checkout:</p><div style="display:inline-block;background:#fef2f2;border:2px dashed #ef4444;border-radius:8px;padding:12px 28px;font-family:monospace;font-size:22px;font-weight:700;color:#ef4444;letter-spacing:3px;">SALE50</div></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#0f172a;color:#fff;padding:16px 48px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;font-size:15px;">SHOP THE SALE</a></div>' }
    ]
},
{
    id: 'abandoned_cart',
    name: '🛒 Abandoned Cart',
    category: 'E-Commerce',
    subject: 'You left something behind...',
    blocks: [
        { type: 'text', content: '<div style="background:#fffbeb;padding:32px;border-left:4px solid #f59e0b;margin-bottom:0;"><h2 style="font-family:Helvetica,Arial,sans-serif;font-size:22px;color:#92400e;margin:0 0 8px;">Your cart misses you! 🛒</h2><p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#78350f;margin:0;">Hi {{first_name}}, you left something amazing in your cart.</p></div>' },
        { type: 'image', content: '<img src="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=600&h=250&q=80" style="max-width:100%;height:auto;display:block;">' },
        { type: 'text', content: '<div style="padding:28px;background:#fff;text-align:center;"><h3 style="font-family:Helvetica,Arial,sans-serif;font-size:18px;color:#1a1a1a;margin:0 0 8px;">Still thinking about it?</h3><p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#666;margin:0;">Complete your purchase before items run out. <strong>Use code SAVE10 for an extra 10% off!</strong></p></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#f59e0b;color:#fff;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">Complete Purchase →</a></div>' }
    ]
},
{
    id: 'new_arrival',
    name: '✨ New Arrival Alert',
    category: 'E-Commerce',
    subject: 'Just dropped: New {{product_name}} is here!',
    blocks: [
        { type: 'text', content: '<div style="background:#0f172a;padding:20px 28px;text-align:center;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;letter-spacing:4px;text-transform:uppercase;color:#94a3b8;margin:0;">NEW ARRIVAL</p></div>' },
        { type: 'image', content: '<img src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&h=400&q=80" style="max-width:100%;height:auto;display:block;">' },
        { type: 'text', content: '<div style="padding:32px;background:#fff;text-align:center;"><h1 style="font-family:Georgia,serif;font-size:30px;color:#0f172a;margin:0 0 12px;">The Perfect Timepiece</h1><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#64748b;margin:0 0 20px;">Handcrafted precision. Built to last a lifetime.</p><p style="font-family:Georgia,serif;font-size:28px;color:#0f172a;font-weight:700;margin:0;">$299.00</p></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#0f172a;color:#fff;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:0;font-weight:700;font-family:Helvetica,Arial,sans-serif;letter-spacing:2px;font-size:13px;text-transform:uppercase;">SHOP NOW</a></div>' }
    ]
},
{
    id: 'seasonal_promo',
    name: '🎁 Seasonal Promo',
    category: 'E-Commerce',
    subject: 'Our biggest sale of the year is here!',
    blocks: [
        { type: 'image', content: '<img src="https://images.unsplash.com/photo-1512389142860-9c449e58a543?auto=format&fit=crop&w=600&h=280&q=80" style="max-width:100%;height:auto;display:block;">' },
        { type: 'text', content: '<div style="background:#fff;padding:32px;text-align:center;"><h1 style="font-family:Georgia,serif;font-size:32px;color:#0f172a;margin:0 0 8px;">🎄 Holiday Sale</h1><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#64748b;margin:0 0 20px;">Up to 40% off on select items. Gift the best, for less.</p><div style="display:inline-flex;gap:20px;justify-content:center;margin-top:16px;"><div style="text-align:center;"><div style="font-family:Georgia,serif;font-size:32px;font-weight:700;color:#ef4444;">40%</div><div style="font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:1px;">Off Apparel</div></div><div style="text-align:center;"><div style="font-family:Georgia,serif;font-size:32px;font-weight:700;color:#2563eb;">30%</div><div style="font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:1px;">Off Electronics</div></div><div style="text-align:center;"><div style="font-family:Georgia,serif;font-size:32px;font-weight:700;color:#059669;">25%</div><div style="font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:1px;">Off Home</div></div></div></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;padding:16px 48px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;font-size:16px;">Shop Holiday Sale 🎁</a></div>' }
    ]
},

// =====================================================
// CATEGORY: ONBOARDING & WELCOME
// =====================================================
{
    id: 'welcome_email',
    name: '👋 Welcome Series',
    category: 'Onboarding',
    subject: 'Welcome to the Family! 🎁',
    blocks: [
        { type: 'text', content: '<div style="background:linear-gradient(135deg,#4f46e5,#7c3aed);padding:48px 28px;text-align:center;border-radius:8px 8px 0 0;"><div style="width:64px;height:64px;background:rgba(255,255,255,0.15);border-radius:50%;margin:0 auto 16px;display:flex;align-items:center;justify-content:center;font-size:28px;">👋</div><h1 style="font-family:Georgia,serif;font-size:28px;color:#fff;margin:0 0 8px;">Welcome Aboard, {{first_name}}!</h1><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:rgba(255,255,255,0.85);margin:0;">We\'re so glad you\'re here.</p></div>' },
        { type: 'text', content: '<div style="background:#fff;padding:32px 28px;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#475569;line-height:1.7;margin:0 0 24px;">Thank you for joining us! Here\'s how to get started:</p><div style="margin-bottom:20px;padding:16px;background:#f8fafc;border-radius:8px;"><div style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#0f172a;"><span style="display:inline-block;width:24px;height:24px;background:#4f46e5;color:#fff;border-radius:50%;text-align:center;line-height:24px;font-weight:700;margin-right:10px;">1</span><strong>Complete your profile</strong> — it takes 2 minutes</div></div><div style="margin-bottom:20px;padding:16px;background:#f8fafc;border-radius:8px;"><div style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#0f172a;"><span style="display:inline-block;width:24px;height:24px;background:#4f46e5;color:#fff;border-radius:50%;text-align:center;line-height:24px;font-weight:700;margin-right:10px;">2</span><strong>Explore the dashboard</strong> — everything is right there</div></div><div style="padding:16px;background:#f8fafc;border-radius:8px;"><div style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#0f172a;"><span style="display:inline-block;width:24px;height:24px;background:#4f46e5;color:#fff;border-radius:50%;text-align:center;line-height:24px;font-weight:700;margin-right:10px;">3</span><strong>Send your first campaign</strong> — reach your audience</div></div></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">Get Started →</a></div>' }
    ]
},
{
    id: 'onboarding_day1',
    name: '🚀 Onboarding Day 1',
    category: 'Onboarding',
    subject: 'Your first step to success, {{first_name}}',
    blocks: [
        { type: 'image', content: '<img src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=600&h=280&q=80" style="max-width:100%;height:auto;display:block;">' },
        { type: 'text', content: '<div style="padding:32px;background:#fff;"><h2 style="font-family:Georgia,serif;font-size:24px;color:#0f172a;margin:0 0 16px;">Day 1: Let\'s set you up for success 🎯</h2><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#475569;line-height:1.7;margin:0 0 20px;">Hi {{first_name}}, the first 24 hours are crucial. Here\'s what we recommend you do today:</p><ul style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#475569;line-height:2;padding-left:20px;"><li>✅ Complete your account setup</li><li>✅ Connect your email provider</li><li>✅ Import your first contacts</li><li>✅ Send a test email to yourself</li></ul></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#059669;color:#fff;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">Continue Setup →</a></div>' }
    ]
},
{
    id: 'trial_expiry',
    name: '⏰ Trial Expiry Warning',
    category: 'Onboarding',
    subject: 'Your trial ends in 3 days, {{first_name}}',
    blocks: [
        { type: 'text', content: '<div style="background:#fffbeb;border-bottom:4px solid #f59e0b;padding:32px;text-align:center;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;letter-spacing:2px;text-transform:uppercase;color:#92400e;margin:0 0 8px;">Action Required</p><h1 style="font-family:Georgia,serif;font-size:28px;color:#78350f;margin:0 0 8px;">Your trial ends in 3 days ⏰</h1><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#92400e;margin:0;">Don\'t lose your data and progress</p></div>' },
        { type: 'text', content: '<div style="padding:32px;background:#fff;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#475569;line-height:1.7;margin:0 0 24px;">Hi {{first_name}}, your free trial of <strong>our Pro plan</strong> expires on <strong>{{expiry_date}}</strong>. Upgrade now to keep all your:</p><div style="padding:20px;background:#f0fdf4;border-radius:8px;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#166534;margin:0;line-height:2;">✅ Saved campaigns &amp; templates<br>✅ Contact lists &amp; segments<br>✅ Analytics &amp; reports<br>✅ Automations</p></div></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#f59e0b;color:#fff;padding:16px 48px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;font-size:16px;">Upgrade Now — Keep Everything</a></div>' }
    ]
},

// =====================================================
// CATEGORY: NEWSLETTERS
// =====================================================
{
    id: 'newsletter',
    name: '📰 Weekly Digest',
    category: 'Newsletter',
    subject: 'Your Weekly Digest — Top Stories',
    blocks: [
        { type: 'text', content: '<div style="background:#0f172a;padding:20px 28px;display:flex;align-items:center;justify-content:space-between;"><span style="font-family:Georgia,serif;font-size:20px;color:#fff;font-weight:700;">The Weekly</span><span style="font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#94a3b8;">Issue #42</span></div>' },
        { type: 'image', content: '<img src="https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=600&h=250&q=80" style="max-width:100%;height:auto;display:block;">' },
        { type: 'text', content: '<div style="padding:28px;background:#fff;"><h2 style="font-family:Georgia,serif;font-size:22px;color:#0f172a;margin:0 0 12px;">This Week\'s Top Story</h2><p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#475569;line-height:1.7;margin:0 0 20px;">Lorem ipsum dolor sit amet consectetur. Proin in venenatis massa. Sed vulputate lorem ut posuere interdum. Maecenas id lorem at diam laoreet rutrum.</p></div>' },
        { type: 'divider', content: '<hr style="border:0;border-top:1px solid #e2e8f0;margin:0 28px;">' },
        { type: 'text', content: '<div style="padding:28px;background:#fff;"><h3 style="font-family:Georgia,serif;font-size:18px;color:#0f172a;margin:0 0 8px;">Also This Week</h3><ul style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#475569;line-height:2;padding-left:20px;margin:0;"><li><a href="#" style="color:#4f46e5;text-decoration:none;font-weight:600;">Story headline #2 →</a></li><li><a href="#" style="color:#4f46e5;text-decoration:none;font-weight:600;">Story headline #3 →</a></li><li><a href="#" style="color:#4f46e5;text-decoration:none;font-weight:600;">Story headline #4 →</a></li></ul></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#0f172a;color:#fff;padding:12px 32px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">Read Full Issue</a></div>' }
    ]
},
{
    id: 'curated_content',
    name: '📌 Curated Content',
    category: 'Newsletter',
    subject: '5 things you shouldn\'t miss this week',
    blocks: [
        { type: 'text', content: '<div style="background:#4f46e5;padding:32px;text-align:center;"><h1 style="font-family:Georgia,serif;font-size:26px;color:#fff;margin:0 0 8px;">5 Things You Shouldn\'t Miss</h1><p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:rgba(255,255,255,0.75);margin:0;">Curated by us, just for you</p></div>' },
        { type: 'text', content: '<div style="padding:28px;background:#fff;"><div style="margin-bottom:24px;padding-bottom:24px;border-bottom:1px solid #f1f5f9;"><div style="display:flex;gap:16px;align-items:flex-start;"><span style="font-family:Georgia,serif;font-size:32px;color:#e2e8f0;line-height:1;min-width:40px;">01</span><div><h3 style="font-family:Georgia,serif;font-size:17px;color:#0f172a;margin:0 0 6px;">Article Title Goes Here</h3><p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#64748b;margin:0;line-height:1.6;">A quick summary of why this matters to your audience.</p></div></div></div><div style="margin-bottom:24px;padding-bottom:24px;border-bottom:1px solid #f1f5f9;"><div style="display:flex;gap:16px;align-items:flex-start;"><span style="font-family:Georgia,serif;font-size:32px;color:#e2e8f0;line-height:1;min-width:40px;">02</span><div><h3 style="font-family:Georgia,serif;font-size:17px;color:#0f172a;margin:0 0 6px;">Second Article Title Here</h3><p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#64748b;margin:0;line-height:1.6;">Another quick summary for your readers.</p></div></div></div><div><div style="display:flex;gap:16px;align-items:flex-start;"><span style="font-family:Georgia,serif;font-size:32px;color:#e2e8f0;line-height:1;min-width:40px;">03</span><div><h3 style="font-family:Georgia,serif;font-size:17px;color:#0f172a;margin:0 0 6px;">Third Great Read</h3><p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#64748b;margin:0;line-height:1.6;">Keep your readers engaged with great content.</p></div></div></div></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#4f46e5;color:#fff;padding:12px 32px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">See All Articles →</a></div>' }
    ]
},

// =====================================================
// CATEGORY: COLD EMAIL
// =====================================================
{
    id: 'cold_email',
    name: '❄️ Classic Cold Outreach',
    category: 'Cold Email',
    subject: 'Quick question about {{company}}',
    blocks: [
        { type: 'text', content: '<div style="padding:32px;background:#fff;max-width:560px;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0 0 16px;">Hi {{first_name}},</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0 0 16px;">I noticed {{company}} is doing impressive work in the {{industry}} space — specifically your recent work on <strong>[specific detail]</strong>.</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0 0 16px;">I help companies like yours <strong>[specific outcome, e.g., "reduce churn by 30%"]</strong> without changing your current workflow.</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0 0 16px;">Would you be open to a 10-minute call this week to see if it\'s a fit?</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0;">Best,<br><strong>{{sender_name}}</strong></p></div>' }
    ]
},
{
    id: 'cold_value_first',
    name: '💎 Value-First Outreach',
    category: 'Cold Email',
    subject: 'I made something for {{company}}',
    blocks: [
        { type: 'text', content: '<div style="padding:32px;background:#fff;max-width:560px;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0 0 16px;">Hi {{first_name}},</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0 0 16px;">I spent 20 minutes researching {{company}} and put together a quick audit of your <strong>[website/email/ads]</strong> — I found 3 things that could be improved immediately.</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0 0 20px;">Would it be okay if I sent it over? It\'s free, no strings attached.</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0;">— {{sender_name}}</p></div>' }
    ]
},
{
    id: 'cold_follow_up',
    name: '🔄 Follow-Up Email',
    category: 'Cold Email',
    subject: 'Re: Quick question about {{company}}',
    blocks: [
        { type: 'text', content: '<div style="padding:32px;background:#fff;max-width:560px;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0 0 16px;">Hi {{first_name}},</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0 0 16px;">Just bumping this to the top of your inbox in case my last email got buried.</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0 0 16px;">To recap — I help <strong>[type of companies]</strong> achieve <strong>[specific result]</strong>. Given what {{company}} is doing, I thought there could be a real fit.</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0 0 16px;">If now isn\'t a good time, just let me know when to circle back.</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0;">Best,<br><strong>{{sender_name}}</strong></p></div>' }
    ]
},
{
    id: 'cold_breakup',
    name: '👋 Break-Up Email',
    category: 'Cold Email',
    subject: 'Should I stay or should I go?',
    blocks: [
        { type: 'text', content: '<div style="padding:32px;background:#fff;max-width:560px;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0 0 16px;">Hi {{first_name}},</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0 0 16px;">I\'ve reached out a couple of times about helping {{company}} with <strong>[problem/opportunity]</strong> and haven\'t heard back — and that\'s completely fine!</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0 0 16px;">I\'ll assume the timing isn\'t right and won\'t reach out again. But if things change and you\'d like to revisit this conversation, my door is always open.</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;margin:0;">Wishing you and the {{company}} team all the best,<br><strong>{{sender_name}}</strong></p></div>' }
    ]
},

// =====================================================
// CATEGORY: EVENTS & WEBINARS
// =====================================================
{
    id: 'webinar_invite',
    name: '🎥 Webinar Invite',
    category: 'Events',
    subject: 'You\'re invited: Free Masterclass on {{topic}}',
    blocks: [
        { type: 'text', content: '<div style="background:linear-gradient(135deg,#1e1b4b,#4f46e5);padding:48px 28px;text-align:center;border-radius:8px 8px 0 0;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,0.6);margin:0 0 16px;">Free Live Webinar</p><h1 style="font-family:Georgia,serif;font-size:28px;color:#fff;margin:0 0 16px;">Mastering Email Marketing in 2026</h1><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:rgba(255,255,255,0.8);margin:0;">Join 500+ marketers learning the strategies that actually work</p></div>' },
        { type: 'text', content: '<div style="background:#f8fafc;padding:28px;display:flex;gap:24px;justify-content:center;text-align:center;"><div style="flex:1;"><div style="font-family:Georgia,serif;font-size:24px;font-weight:700;color:#0f172a;">📅</div><div style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#0f172a;margin-top:4px;">Thursday, Nov 12</div></div><div style="flex:1;"><div style="font-family:Georgia,serif;font-size:24px;font-weight:700;color:#0f172a;">⏰</div><div style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#0f172a;margin-top:4px;">2:00 PM EST</div></div><div style="flex:1;"><div style="font-family:Georgia,serif;font-size:24px;font-weight:700;color:#0f172a;">🆓</div><div style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#0f172a;margin-top:4px;">100% Free</div></div></div>' },
        { type: 'text', content: '<div style="padding:28px;background:#fff;"><h3 style="font-family:Georgia,serif;font-size:18px;color:#0f172a;margin:0 0 12px;">What you\'ll learn:</h3><ul style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#475569;line-height:2;padding-left:20px;margin:0;"><li>The #1 mistake killing your open rates</li><li>How to write subject lines that get clicks</li><li>Automation sequences that convert</li><li>Live Q&A with our experts</li></ul></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;padding:16px 48px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;font-size:15px;">Reserve My Free Seat →</a></div>' }
    ]
},
{
    id: 'event_reminder',
    name: '🔔 Event Reminder',
    category: 'Events',
    subject: 'Reminder: {{event_name}} starts tomorrow!',
    blocks: [
        { type: 'text', content: '<div style="background:#eff6ff;border-left:4px solid #2563eb;padding:28px;margin-bottom:0;text-align:center;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;letter-spacing:2px;text-transform:uppercase;color:#1d4ed8;margin:0 0 8px;">Reminder</p><h2 style="font-family:Georgia,serif;font-size:24px;color:#1e3a8a;margin:0;">Your event starts tomorrow! 🎉</h2></div>' },
        { type: 'image', content: '<img src="https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=600&h=250&q=80" style="max-width:100%;height:auto;display:block;">' },
        { type: 'text', content: '<div style="padding:28px;background:#fff;text-align:center;"><h3 style="font-family:Georgia,serif;font-size:22px;color:#0f172a;margin:0 0 12px;">{{event_name}}</h3><p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#64748b;margin:0 0 8px;"><strong>📅 Date:</strong> {{event_date}}</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#64748b;margin:0 0 8px;"><strong>⏰ Time:</strong> {{event_time}}</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#64748b;margin:0;"><strong>📍 Location:</strong> {{event_location}}</p></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#2563eb;color:#fff;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">Add to Calendar 📅</a></div>' }
    ]
},

// =====================================================
// CATEGORY: TRANSACTIONAL
// =====================================================
{
    id: 'thank_you',
    name: '💖 Order Confirmation',
    category: 'Transactional',
    subject: 'Order #{{order_id}} Confirmed! Thank you 🎉',
    blocks: [
        { type: 'text', content: '<div style="background:#f0fdf4;padding:40px;text-align:center;border-bottom:3px solid #10b981;"><div style="width:56px;height:56px;background:#10b981;border-radius:50%;margin:0 auto 16px;font-size:24px;display:flex;align-items:center;justify-content:center;color:#fff;">✓</div><h1 style="font-family:Georgia,serif;font-size:26px;color:#065f46;margin:0 0 8px;">Order Confirmed!</h1><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#047857;margin:0;">Thank you for your purchase, {{first_name}}</p></div>' },
        { type: 'text', content: '<div style="padding:28px;background:#fff;"><h3 style="font-family:Georgia,serif;font-size:18px;color:#0f172a;margin:0 0 16px;">Order Summary</h3><table style="width:100%;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;"><tr style="border-bottom:1px solid #f1f5f9;"><td style="padding:12px 0;font-size:14px;color:#64748b;">Order #</td><td style="padding:12px 0;font-size:14px;color:#0f172a;font-weight:600;text-align:right;">{{order_id}}</td></tr><tr style="border-bottom:1px solid #f1f5f9;"><td style="padding:12px 0;font-size:14px;color:#64748b;">Items</td><td style="padding:12px 0;font-size:14px;color:#0f172a;font-weight:600;text-align:right;">{{item_count}}</td></tr><tr style="border-bottom:1px solid #f1f5f9;"><td style="padding:12px 0;font-size:14px;color:#64748b;">Shipping</td><td style="padding:12px 0;font-size:14px;color:#0f172a;font-weight:600;text-align:right;">{{shipping_cost}}</td></tr><tr><td style="padding:12px 0;font-size:16px;font-weight:700;color:#0f172a;">Total</td><td style="padding:12px 0;font-size:16px;font-weight:700;color:#059669;text-align:right;">{{order_total}}</td></tr></table></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#0f172a;color:#fff;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">Track Your Order →</a></div>' }
    ]
},
{
    id: 'review_request',
    name: '⭐ Review Request',
    category: 'Transactional',
    subject: 'How was your experience with us?',
    blocks: [
        { type: 'text', content: '<div style="padding:40px;background:#fff;text-align:center;"><div style="font-size:48px;margin-bottom:16px;">😊</div><h2 style="font-family:Georgia,serif;font-size:24px;color:#0f172a;margin:0 0 12px;">How did we do?</h2><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#64748b;margin:0 0 24px;">Your feedback means the world to us, {{first_name}}. It takes just 30 seconds.</p><div style="display:flex;gap:8px;justify-content:center;font-size:36px;cursor:pointer;">⭐⭐⭐⭐⭐</div><p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#94a3b8;margin:12px 0 0;">Click to rate your experience</p></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#f59e0b;color:#fff;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">Write a Review →</a></div>' }
    ]
},

// =====================================================
// CATEGORY: ANNOUNCEMENTS
// =====================================================
{
    id: 'make_announcement',
    name: '📢 Company Announcement',
    category: 'Announcement',
    subject: 'Big News from {{company_name}}!',
    blocks: [
        { type: 'text', content: '<div style="background:#0f172a;padding:32px;text-align:center;"><h1 style="font-family:Georgia,serif;font-size:28px;color:#fff;margin:0 0 8px;">We have some exciting news!</h1><p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#94a3b8;margin:0;">A message from the {{company_name}} team</p></div>' },
        { type: 'image', content: '<img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=600&h=300&q=80" style="max-width:100%;height:auto;display:block;">' },
        { type: 'text', content: '<div style="padding:32px;background:#fff;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#475569;line-height:1.7;margin:0 0 16px;">After months of hard work, we are thrilled to announce that we are expanding our services. This means more features, better support, and lower prices for you.</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#475569;line-height:1.7;margin:0;">As a valued customer, you\'re among the first to hear this news.</p></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#2563eb;color:#fff;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">Read the Full Story →</a></div>' }
    ]
},
{
    id: 'product_update',
    name: '🆕 Product Update',
    category: 'Announcement',
    subject: 'We just released something big 🎉',
    blocks: [
        { type: 'text', content: '<div style="background:linear-gradient(135deg,#059669,#047857);padding:40px;text-align:center;border-radius:8px 8px 0 0;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,0.7);margin:0 0 12px;">Product Update</p><h1 style="font-family:Georgia,serif;font-size:28px;color:#fff;margin:0 0 8px;">Introducing [Feature Name] 🚀</h1><p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:rgba(255,255,255,0.85);margin:0;">The update you\'ve been waiting for</p></div>' },
        { type: 'text', content: '<div style="padding:32px;background:#fff;"><h3 style="font-family:Georgia,serif;font-size:20px;color:#0f172a;margin:0 0 16px;">What\'s new:</h3><div style="margin-bottom:16px;padding:16px;background:#f0fdf4;border-radius:8px;border-left:3px solid #059669;"><h4 style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#0f172a;margin:0 0 4px;">✨ Feature One</h4><p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#64748b;margin:0;">A short description of this feature and why it\'s awesome.</p></div><div style="margin-bottom:16px;padding:16px;background:#f0fdf4;border-radius:8px;border-left:3px solid #059669;"><h4 style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#0f172a;margin:0 0 4px;">⚡ Feature Two</h4><p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#64748b;margin:0;">A short description of this feature and why it\'s awesome.</p></div><div style="padding:16px;background:#f0fdf4;border-radius:8px;border-left:3px solid #059669;"><h4 style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#0f172a;margin:0 0 4px;">🔥 Feature Three</h4><p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#64748b;margin:0;">A short description of this feature and why it\'s awesome.</p></div></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#059669;color:#fff;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">Try It Now →</a></div>' }
    ]
},

// =====================================================
// CATEGORY: ENGAGEMENT & RETENTION
// =====================================================
{
    id: 'win_back',
    name: '💔 Win-Back Campaign',
    category: 'Retention',
    subject: 'We miss you, {{first_name}} 💙',
    blocks: [
        { type: 'image', content: '<img src="https://images.unsplash.com/photo-1516585427167-9f4af9627e6c?auto=format&fit=crop&w=600&h=280&q=80" style="max-width:100%;height:auto;display:block;">' },
        { type: 'text', content: '<div style="padding:32px;background:#fff;text-align:center;"><h2 style="font-family:Georgia,serif;font-size:26px;color:#0f172a;margin:0 0 12px;">It\'s been a while... 👋</h2><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#64748b;line-height:1.7;margin:0 0 20px;">Hi {{first_name}}, we noticed you haven\'t been around for a while. We\'ve been busy adding new features and would love to show you what\'s changed.</p><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#64748b;margin:0;">To celebrate your return, here\'s <strong>30% off your next purchase</strong>. Just because we missed you. 💙</p></div>' },
        { type: 'text', content: '<div style="text-align:center;padding:0 28px 24px;background:#fff;"><div style="display:inline-block;background:#fef3c7;border:2px dashed #f59e0b;border-radius:8px;padding:12px 28px;font-family:monospace;font-size:22px;font-weight:700;color:#92400e;letter-spacing:3px;">MISSYOU30</div></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#0f172a;color:#fff;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">Claim My 30% Off →</a></div>' }
    ]
},
{
    id: 'educational',
    name: '📚 Educational / Tips',
    category: 'Retention',
    subject: '3 tips to get more from {{product_name}}',
    blocks: [
        { type: 'image', content: '<img src="https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=600&h=250&q=80" style="max-width:100%;height:auto;display:block;">' },
        { type: 'text', content: '<div style="padding:32px;background:#fff;"><h2 style="font-family:Georgia,serif;font-size:24px;color:#0f172a;margin:0 0 8px;">3 Tips to Get More Results</h2><p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#64748b;margin:0 0 24px;">Here\'s what top performers are doing differently.</p><div style="margin-bottom:20px;padding:20px;background:#f8fafc;border-radius:8px;"><h4 style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#0f172a;margin:0 0 6px;">💡 Tip #1: Subject Line A/B Testing</h4><p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#64748b;margin:0;line-height:1.6;">Users who test 2+ subject lines see 23% higher open rates on average.</p></div><div style="margin-bottom:20px;padding:20px;background:#f8fafc;border-radius:8px;"><h4 style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#0f172a;margin:0 0 6px;">⚡ Tip #2: Send at the Right Time</h4><p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#64748b;margin:0;line-height:1.6;">Tuesday-Thursday, 9-11 AM in your recipient\'s timezone.</p></div><div style="padding:20px;background:#f8fafc;border-radius:8px;"><h4 style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#0f172a;margin:0 0 6px;">🎯 Tip #3: Segment Your List</h4><p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#64748b;margin:0;line-height:1.6;">Segmented campaigns see 14.31% higher open rates than non-segmented.</p></div></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#4f46e5;color:#fff;padding:12px 32px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">Read Full Guide →</a></div>' }
    ]
},
{
    id: 'referral',
    name: '🎁 Referral Program',
    category: 'Retention',
    subject: 'Earn $20 for every friend you refer!',
    blocks: [
        { type: 'text', content: '<div style="background:linear-gradient(135deg,#7c3aed,#a855f7);padding:48px 28px;text-align:center;border-radius:8px 8px 0 0;"><h1 style="font-family:Georgia,serif;font-size:32px;color:#fff;margin:0 0 12px;">Give $20, Get $20 🎁</h1><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:rgba(255,255,255,0.85);margin:0;">Share with a friend. You both win.</p></div>' },
        { type: 'text', content: '<div style="padding:32px;background:#fff;"><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#475569;line-height:1.7;text-align:center;margin:0 0 28px;">Hi {{first_name}}, love using our product? Share it with a friend and you\'ll both get $20 credit.</p><div style="display:flex;gap:20px;justify-content:center;text-align:center;"><div style="flex:1;padding:20px;background:#f5f3ff;border-radius:8px;"><div style="font-size:28px;margin-bottom:8px;">1️⃣</div><div style="font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#6d28d9;font-weight:600;">Share your link</div></div><div style="flex:1;padding:20px;background:#f5f3ff;border-radius:8px;"><div style="font-size:28px;margin-bottom:8px;">2️⃣</div><div style="font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#6d28d9;font-weight:600;">Friend signs up</div></div><div style="flex:1;padding:20px;background:#f5f3ff;border-radius:8px;"><div style="font-size:28px;margin-bottom:8px;">3️⃣</div><div style="font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#6d28d9;font-weight:600;">You both get $20</div></div></div></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:linear-gradient(135deg,#7c3aed,#a855f7);color:#fff;padding:16px 48px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">Share Your Referral Link →</a></div>' }
    ]
},

// =====================================================
// CATEGORY: SAAS / B2B
// =====================================================
{
    id: 'app_download',
    name: '📱 App Download',
    category: 'SaaS',
    subject: 'Take us anywhere — New mobile app is live!',
    blocks: [
        { type: 'image', content: '<img src="https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&w=600&h=300&q=80" style="max-width:100%;height:auto;display:block;">' },
        { type: 'text', content: '<div style="background:#fff;padding:32px;text-align:center;"><h2 style="font-family:Georgia,serif;font-size:26px;color:#0f172a;margin:0 0 12px;">The Mobile App is Here</h2><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#64748b;margin:0 0 20px;line-height:1.7;">Manage campaigns, track analytics, and reach your audience from anywhere.</p><div style="display:flex;gap:12px;justify-content:center;"><div style="display:inline-block;background:#000;border-radius:8px;padding:10px 20px;"><span style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#fff;font-weight:600;">🍎 App Store</span></div><div style="display:inline-block;background:#000;border-radius:8px;padding:10px 20px;"><span style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#fff;font-weight:600;">▶ Google Play</span></div></div></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:#000;color:#fff;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:24px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">Download Now → Free</a></div>' }
    ]
},
{
    id: 'saas_upsell',
    name: '📈 Upgrade / Upsell',
    category: 'SaaS',
    subject: '{{first_name}}, you\'re almost at your limit',
    blocks: [
        { type: 'text', content: '<div style="background:#fff;padding:32px;border-top:4px solid #4f46e5;"><h2 style="font-family:Georgia,serif;font-size:22px;color:#0f172a;margin:0 0 16px;">You\'re using 80% of your plan 📊</h2><p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#64748b;line-height:1.7;margin:0 0 20px;">Hi {{first_name}}, you\'ve been growing fast! You\'ve used <strong>800 of your 1,000 contacts</strong> this month. Upgrade to unlock unlimited contacts + more features.</p><div style="background:#f1f5f9;border-radius:8px;padding:4px;margin-bottom:20px;"><div style="background:linear-gradient(90deg,#4f46e5,#7c3aed);height:12px;border-radius:8px;width:80%;"></div></div><div style="font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#64748b;text-align:right;">800 / 1,000 contacts used</div></div>' },
        { type: 'text', content: '<div style="padding:24px 32px;background:#f8fafc;"><h3 style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#0f172a;margin:0 0 12px;">Pro Plan includes:</h3><ul style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#475569;line-height:2;padding-left:20px;margin:0;"><li>✅ Unlimited contacts</li><li>✅ Advanced analytics</li><li>✅ Priority support</li><li>✅ A/B testing</li></ul></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:24px 28px 32px;background:#fff;"><a href="#" style="background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;">Upgrade to Pro →</a></div>' }
    ]
},

// =====================================================
// CATEGORY: MINIMAL / PLAIN
// =====================================================
{
    id: 'plain_text',
    name: '✉️ Plain Text (Clean)',
    category: 'Minimal',
    subject: 'A personal note from me',
    blocks: [
        { type: 'text', content: '<div style="padding:40px;background:#fff;max-width:560px;font-family:Georgia,serif;"><p style="font-size:16px;color:#333;line-height:1.8;margin:0 0 16px;">Hi {{first_name}},</p><p style="font-size:16px;color:#333;line-height:1.8;margin:0 0 16px;">I wanted to reach out personally to share something important with you.</p><p style="font-size:16px;color:#333;line-height:1.8;margin:0 0 16px;">[Your main message goes here. Keep it conversational, genuine, and focused on one clear goal.]</p><p style="font-size:16px;color:#333;line-height:1.8;margin:0 0 16px;">I hope this helps. As always, feel free to reply directly to this email — I read every message.</p><p style="font-size:16px;color:#333;line-height:1.8;margin:0;">Warmly,<br><br><strong>{{sender_name}}</strong><br><span style="font-size:14px;color:#888;">Founder, {{company_name}}</span></p></div>' }
    ]
},
{
    id: 'minimal_announcement',
    name: '⬜ Minimal Clean',
    category: 'Minimal',
    subject: 'Something new is coming',
    blocks: [
        { type: 'text', content: '<div style="padding:60px 40px;background:#fff;text-align:center;"><h1 style="font-family:Georgia,serif;font-size:32px;color:#0f172a;font-weight:400;margin:0 0 16px;letter-spacing:-0.5px;">Something new is coming.</h1><div style="width:40px;height:2px;background:#0f172a;margin:0 auto 24px;"></div><p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#64748b;line-height:1.7;margin:0 auto;max-width:420px;">We\'ve been working on something we think you\'ll love. We\'ll share more details very soon.</p></div>' },
        { type: 'button', content: '<div style="text-align:center;padding:0 40px 60px;background:#fff;"><a href="#" style="border:2px solid #0f172a;color:#0f172a;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:0;font-weight:600;font-family:Helvetica,Arial,sans-serif;font-size:14px;letter-spacing:2px;text-transform:uppercase;">Learn More</a></div>' }
    ]
}

];

// Categories for sidebar grouping
window.EmailTemplateCategories = [
    { id: 'all', name: 'All Templates', icon: '📋' },
    { id: 'E-Commerce', name: 'E-Commerce', icon: '🛍️' },
    { id: 'Newsletter', name: 'Newsletter', icon: '📰' },
    { id: 'Cold Email', name: 'Cold Email', icon: '❄️' },
    { id: 'Onboarding', name: 'Onboarding', icon: '🚀' },
    { id: 'Events', name: 'Events', icon: '🎥' },
    { id: 'Transactional', name: 'Transactional', icon: '🧾' },
    { id: 'Announcement', name: 'Announcements', icon: '📢' },
    { id: 'Retention', name: 'Retention', icon: '💙' },
    { id: 'SaaS', name: 'SaaS / B2B', icon: '📈' },
    { id: 'Minimal', name: 'Minimal', icon: '⬜' },
];
