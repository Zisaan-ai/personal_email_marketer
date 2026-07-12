import json
import random
import re

categories = [
    'Announcement', 'Cold Email', 'E-Commerce', 'Events', 'Minimal',
    'Newsletter', 'Onboarding', 'Retention', 'SaaS', 'Transactional'
]

adjectives = ['Ultimate', 'Pro', 'Elite', 'Starter', 'Premium', 'Modern', 'Sleek', 'Classic', 'Dynamic', 'Bold']
nouns = ['Update', 'Launch', 'Digest', 'Report', 'Welcome', 'Offer', 'Invitation', 'Alert', 'Summary', 'Boost']

colors = ['#4f46e5', '#ef4444', '#10b981', '#f59e0b', '#3b82f6', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#0ea5e9']

images = [
    'https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=600&h=300&q=80',
    'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=600&h=300&q=80',
    'https://images.unsplash.com/photo-1556761175-4b46a572b786?auto=format&fit=crop&w=600&h=300&q=80',
    'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=600&h=300&q=80',
    'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=600&h=300&q=80',
    'https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=600&h=300&q=80',
    'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=600&h=300&q=80'
]

def generate_blocks(cat, color):
    blocks = []
    
    # 50% chance to have a hero image
    if random.random() > 0.5 and cat != 'Cold Email' and cat != 'Minimal':
        blocks.append({
            'type': 'image',
            'content': f'<img src="{random.choice(images)}" style="max-width:100%;height:auto;display:block;border-radius:8px 8px 0 0;">'
        })
        
    blocks.append({
        'type': 'text',
        'content': f'<div style="background:#fff;padding:32px 28px;text-align:center;"><h1 style="font-family:Georgia,serif;font-size:26px;color:#1a1a1a;margin:0 0 12px;">Exclusive {cat} Insight</h1><p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#666;margin:0;line-height:1.6;">Hello {{{{first_name}}}}, we are excited to share our latest updates with you. Discover what is new and how it can help you grow.</p></div>'
    })
    
    # 30% chance to have 2 columns
    if random.random() > 0.7:
        blocks.append({
            'type': 'columns2',
            'content': f'<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#fff;"><tr><td width="50%" valign="top" style="padding:20px;font-family:Helvetica,Arial,sans-serif;"><div style="background:#f8fafc;padding:20px;border-radius:8px;text-align:center;"><h3 style="margin-top:0;color:{color};">Feature 1</h3><p style="font-size:14px;color:#666;margin-bottom:0;">Amazing new capability.</p></div></td><td width="50%" valign="top" style="padding:20px;font-family:Helvetica,Arial,sans-serif;"><div style="background:#f8fafc;padding:20px;border-radius:8px;text-align:center;"><h3 style="margin-top:0;color:{color};">Feature 2</h3><p style="font-size:14px;color:#666;margin-bottom:0;">Enhanced performance.</p></div></td></tr></table>'
        })
        
    blocks.append({
        'type': 'button',
        'content': f'<div style="text-align:center;padding:8px 28px 32px;background:#fff;"><a href="#" style="background:{color};color:#fff;padding:14px 40px;text-decoration:none;display:inline-block;border-radius:6px;font-weight:700;font-family:Helvetica,Arial,sans-serif;font-size:15px;">Read More</a></div>'
    })
    
    return blocks

new_templates = []
for c in categories:
    for i in range(10):
        color = random.choice(colors)
        adj = random.choice(adjectives)
        noun = random.choice(nouns)
        name = f"{adj} {noun} {i+1}"
        
        new_templates.append({
            'id': f"gen_{c.lower().replace(' ', '_').replace('-', '_')}_{i}",
            'name': name,
            'category': c,
            'subject': f"Your {name} inside!",
            'blocks': generate_blocks(c, color)
        })

# Read existing templates.js
with open('frontend/assets/templates.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace `window.EmailTemplates = [` with `window.EmailTemplates = [ ...new_templates... ,`
js_templates = json.dumps(new_templates, indent=4)
# Remove [ and ] from js_templates
js_templates = js_templates[1:-1].strip()

new_content = content.replace("window.EmailTemplates = [", f"window.EmailTemplates = [\n{js_templates},\n")

with open('frontend/assets/templates.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Generated 100 new templates.")
