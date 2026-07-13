import codecs
import re

html = codecs.open('frontend/index.html', 'r', 'utf-8').read()

html = re.sub(r'assets/app\.js\?v=\d+', 'assets/app.js?v=4018', html)

codecs.open('frontend/index.html', 'w', 'utf-8').write(html)
print('Updated app.js version to bust cache.')
