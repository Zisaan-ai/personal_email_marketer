import codecs
import re

with codecs.open('frontend/index.html', 'r', 'utf-8') as f:
    html = f.read()

# Delete guide-view
html = re.sub(r'<!-- GUIDE -->\s*<div id="guide-view" class="view">.*?</div>\s*</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)

with codecs.open('frontend/index.html', 'w', 'utf-8') as f:
    f.write(html)
print("Deleted old guide-view")
