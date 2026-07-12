with open('frontend/assets/app.js', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "['paused', 'completed', 'failed'].includes(st)",
    "['paused', 'completed', 'failed', 'draft', 'pending'].includes(st)"
)

# And I also need to update the version buster in index.html to ensure it loads
with open('frontend/index.html', encoding='utf-8') as f:
    idx_text = f.read()
    
idx_text = idx_text.replace('app.js?v=3004', 'app.js?v=3005')

with open('frontend/assets/app.js', 'w', encoding='utf-8') as f:
    f.write(text)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(idx_text)

print('Updated app.js and index.html')
