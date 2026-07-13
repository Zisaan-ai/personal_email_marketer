import codecs

with codecs.open('frontend/index.html', 'r', 'utf-8') as f:
    html = f.read()

# Insert the navigation item
nav_item = """            <a class="nav-item" data-target="guide-view" onclick="window.navTo('guide-view')">
                <i class="fa-solid fa-circle-question"></i><span>How to Use</span>
            </a>\n"""

nav_idx = html.find('<a class="nav-item" data-target="about-view"')
if nav_idx != -1:
    end_nav = html.find('</a>', nav_idx) + 4
    html = html[:end_nav] + '\n' + nav_item + html[end_nav:]
else:
    print('Could not find about-view nav item')

# Insert the guide-view div
with codecs.open('guide_extracted.html', 'r', 'utf-8') as f:
    guide_html = f.read()

insert_idx = html.find('        <!-- INBOX PREVIEW MODAL -->')
if insert_idx != -1:
    html = html[:insert_idx] + guide_html + '\n' + html[insert_idx:]
else:
    print('Could not find INBOX PREVIEW MODAL')

with codecs.open('frontend/index.html', 'w', 'utf-8') as f:
    f.write(html)
print('Updated index.html')
