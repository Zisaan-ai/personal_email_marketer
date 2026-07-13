import codecs
import re

with codecs.open('frontend/index.html', 'r', 'utf-8') as f:
    html = f.read()

# Remove the accordion box we just added
html = re.sub(r'<div class="about-card" style="grid-column: 1 / -1; margin-top: 32px; padding: 0;.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)

# Re-read the extracted guide_extracted.html to parse the 7 steps
with codecs.open('guide_extracted.html', 'r', 'utf-8') as f:
    guide_html = f.read()

# We want the 7 steps inside the glass div
start = guide_html.find('<div class="glass"')
content_start = guide_html.find('>', start) + 1
content_end = guide_html.rfind('</div>')
inner_guide = guide_html[content_start:content_end].strip()

# Create a beautiful wrapper for the Guide section
guide_section = f'''
              <div style="margin-top: 60px; padding-top: 40px; border-top: 1px solid rgba(0,0,0,0.05);">
                  <div class="page-header" style="text-align: center; margin-bottom: 40px;">
                      <div style="display:inline-flex; align-items:center; justify-content:center; width:56px; height:56px; border-radius:16px; background:linear-gradient(135deg, #10b981, #3b82f6); color:white; font-size:24px; margin-bottom:16px; box-shadow:0 10px 20px -5px rgba(16,185,129,0.4);">
                          <i class="fa-solid fa-chalkboard-user"></i>
                      </div>
                      <h2 style="font-size: 32px; font-weight: 800; color: var(--text); margin-bottom: 12px;">How to Use (?????? ??????? ?????)</h2>
                      <p style="font-size: 16px; color: var(--text-muted); max-width: 600px; margin: 0 auto;">Simple step-by-step guide for MailClone / ????????? ????????? ??? ????</p>
                  </div>
                  
                  <div style="display: flex; flex-direction: column; gap: 24px; padding: 0 20px;">
                      {inner_guide}
                  </div>
              </div>
'''

# Insert guide_section at the end of the about-view (after the about-grid)
about_grid_end = html.find('</div>', html.find('16. Engineered by'))
about_grid_end = html.find('</div>', about_grid_end + 1)
about_grid_end = html.find('</div>', about_grid_end + 1)

if about_grid_end != -1:
    html = html[:about_grid_end+6] + guide_section + html[about_grid_end+6:]

with codecs.open('frontend/index.html', 'w', 'utf-8') as f:
    f.write(html)

print("Updated index.html with separate How to Use boxes")
