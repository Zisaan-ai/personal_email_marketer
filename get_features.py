import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract all about-title and about-text to see the features
titles = re.findall(r'<h3 class="about-title">(.*?)</h3>', html)
print("Found", len(titles), "features:")
for i, t in enumerate(titles, 1):
    print(f"{i}. {t}")
