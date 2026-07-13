import codecs
import re

with codecs.open('frontend/index.html', 'r', 'utf-8') as f:
    html = f.read()

# Remove the 7 boxes section
html = re.sub(r'<div style="margin-top: 60px; padding-top: 40px; border-top: 1px solid rgba\(0,0,0,0\.05\);">\s*<div class="page-header".*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)

# Let's see if there are any other 'How to Use'
html = re.sub(r'<div style="margin-top: auto; padding-top: 16px;">.*?<div class="htu-icon".*?</div>\s*</div>\s*<div style="max-height: 0;.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)

# If it is still there, let's just find and replace the whole block manually
start_marker = '<div style="margin-top: 60px; padding-top: 40px; border-top: 1px solid rgba(0,0,0,0.05);">'
idx1 = html.find(start_marker)
if idx1 != -1:
    # find where this block ends. It's the end of the guide section
    # The last block inside has '7. Analytics (?????????????)'
    idx2 = html.find('7. Analytics', idx1)
    if idx2 != -1:
        idx_end = html.find('</div>\n              </div>', idx2) + 29
        html = html[:idx1] + html[idx_end:]

with codecs.open('frontend/index.html', 'w', 'utf-8') as f:
    f.write(html)
print("Cleaned up everything!")
