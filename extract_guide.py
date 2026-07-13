import re

with open('old_index.html', 'r', encoding='utf-16') as f:
    html = f.read()

start = html.find('<!-- GUIDE -->')
end = html.find('<!-- INBOX PREVIEW MODAL -->', start)

if start != -1 and end != -1:
    guide_html = html[start:end]
    print('Found guide-view. Length:', len(guide_html))
    with open('guide_extracted.html', 'w', encoding='utf-8') as f:
        f.write(guide_html)
else:
    print('Could not extract')
