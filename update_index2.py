import codecs

with codecs.open('frontend/index.html', 'r', 'utf-8') as f:
    html = f.read()

# Remove the guide-view from sidebar
html = html.replace('''            <a class="nav-item" data-target="guide-view" onclick="window.navTo('guide-view')">
                <i class="fa-solid fa-circle-question"></i><span>How to Use</span>
            </a>\n''', '')

# We will add a premium "How to Use" card at the end of the about-grid
about_grid_end = html.find('</div>', html.rfind('class="about-card"'))

premium_box = '''
              <div class="about-card" style="grid-column: 1 / -1; margin-top: 32px; background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(236, 72, 153, 0.1)); border: 1px solid rgba(79, 70, 229, 0.2); cursor: pointer;" onclick="window.navTo('guide-view')">
                  <div style="display:flex; align-items:center; justify-content:space-between;">
                      <div style="display:flex; align-items:center; gap:24px;">
                          <div style="width: 64px; height: 64px; border-radius: 16px; background: linear-gradient(135deg, #4f46e5, #ec4899); color: white; display: flex; align-items: center; justify-content: center; font-size: 28px; box-shadow: 0 10px 25px -5px rgba(236, 72, 153, 0.5);">
                              <i class="fa-solid fa-book-open-reader"></i>
                          </div>
                          <div>
                              <h3 style="font-size: 24px; font-weight: 800; color: var(--text); margin-bottom: 8px;">How to Use (?????? ??????? ?????)</h3>
                              <p style="font-size: 15px; color: var(--text-muted); margin: 0;">Click here to read the complete step-by-step guide / ???????? ???? ???? ????? ????? ????</p>
                          </div>
                      </div>
                      <div style="width: 48px; height: 48px; border-radius: 50%; background: #fff; display: flex; align-items: center; justify-content: center; color: #4f46e5; font-size: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                          <i class="fa-solid fa-arrow-right"></i>
                      </div>
                  </div>
              </div>
'''

if about_grid_end != -1:
    # the end of about-grid is the closing div of the last about-card + its parent closing div
    # let's find the exact place
    idx = html.find('</div>', html.find('16. Engineered by'))
    idx = html.find('</div>', idx + 1) # end of p
    idx = html.find('</div>', idx + 1) # end of about-card
    if idx != -1:
        html = html[:idx+6] + premium_box + html[idx+6:]

with codecs.open('frontend/index.html', 'w', 'utf-8') as f:
    f.write(html)
print('Updated index.html')
