with open('xcomic.xyz/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
new_content = re.sub(r'assets/app\.js(\?v=\d+)?', 'assets/app.js?v=3', content)

with open('xcomic.xyz/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Updated index.html cache buster')
