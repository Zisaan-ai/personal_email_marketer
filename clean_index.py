import codecs
import re

with codecs.open('frontend/index.html', 'r', 'utf-8') as f:
    html = f.read()

# Remove the accordions inside about-card
# The pattern starts with <div style="margin-top: auto; padding-top: 16px;">
# and ends with </div></div></div>
html_new = re.sub(r'<div style="margin-top: auto; padding-top: 16px;">.*?<div class="htu-icon".*?</div>\s*</div>\s*<div style="max-height: 0;.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)

with codecs.open('frontend/index.html', 'w', 'utf-8') as f:
    f.write(html_new)
print("Removed old how to use accordions")
