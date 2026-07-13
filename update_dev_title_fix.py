import codecs

with codecs.open('frontend/index.html', 'r', 'utf-8') as f:
    html = f.read()

# Make sure it actually replaces
old = html
html = html.replace('ফ্রিল্যান্সার মোনেম রহমান জিসান', 'ডেভেলপার মোনেম রহমান জিসান')

with codecs.open('frontend/index.html', 'w', 'utf-8') as f:
    f.write(html)

if old != html:
    print("Replaced successfully.")
else:
    print("Did not find the string to replace.")
