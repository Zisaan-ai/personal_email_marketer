import codecs

with codecs.open('frontend/index.html', 'r', 'utf-8') as f:
    html = f.read()

# First, remove the premium_box we just added
import re
html = re.sub(r'<div class="about-card" style="grid-column: 1 / -1.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)

# Also grab the content of guide-view and make it the accordion content
guide_content = ""
start = html.find('<div id="guide-view" class="view">')
if start != -1:
    content_start = html.find('<div class="glass"', start)
    if content_start != -1:
        content_end = html.find('</div>\n        </div>', content_start)
        guide_content = html[content_start:content_end]

# Now, we insert the accordion box at the end of the about-grid
accordion_html = f'''
              <div class="about-card" style="grid-column: 1 / -1; margin-top: 32px; padding: 0; background: linear-gradient(135deg, rgba(79, 70, 229, 0.05), rgba(236, 72, 153, 0.05)); border: 1px solid rgba(79, 70, 229, 0.2); overflow: hidden;">
                  <div onclick="const content = document.getElementById('how-to-use-content'); const icon = document.getElementById('how-to-use-icon'); if(content.style.maxHeight){{content.style.maxHeight = null; icon.style.transform = 'rotate(0deg)';}}else{{content.style.maxHeight = content.scrollHeight + 'px'; icon.style.transform = 'rotate(180deg)';}}" style="display:flex; align-items:center; justify-content:space-between; padding: 24px 32px; cursor: pointer; background: rgba(255,255,255,0.5);">
                      <div style="display:flex; align-items:center; gap:24px;">
                          <div style="width: 56px; height: 56px; border-radius: 14px; background: linear-gradient(135deg, #4f46e5, #ec4899); color: white; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 8px 20px -4px rgba(236, 72, 153, 0.4);">
                              <i class="fa-solid fa-book-open-reader"></i>
                          </div>
                          <div>
                              <h3 style="font-size: 22px; font-weight: 800; color: var(--text); margin-bottom: 4px;">How to Use (?????? ??????? ?????)</h3>
                              <p style="font-size: 14.5px; color: var(--text-muted); margin: 0;">Click to expand the complete step-by-step guide / ???? ???? ????? ????</p>
                          </div>
                      </div>
                      <div id="how-to-use-icon" style="width: 40px; height: 40px; border-radius: 50%; background: #fff; display: flex; align-items: center; justify-content: center; color: #4f46e5; font-size: 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); transition: transform 0.3s ease;">
                          <i class="fa-solid fa-chevron-down"></i>
                      </div>
                  </div>
                  <div id="how-to-use-content" style="max-height: 0; overflow: hidden; transition: max-height 0.5s ease-out; background: #fff;">
                      <div style="padding: 32px; border-top: 1px solid rgba(0,0,0,0.05);">
                          {guide_content}
                      </div>
                  </div>
              </div>
'''

idx = html.find('</div>', html.find('16. Engineered by'))
idx = html.find('</div>', idx + 1)
idx = html.find('</div>', idx + 1)
if idx != -1:
    html = html[:idx+6] + accordion_html + html[idx+6:]

with codecs.open('frontend/index.html', 'w', 'utf-8') as f:
    f.write(html)
print('Updated accordion box!')
