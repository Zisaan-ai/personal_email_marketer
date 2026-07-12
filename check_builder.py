with open('frontend/index.html', encoding='utf-8') as f:
    text = f.read()
    idx = text.find('id="campaigns-builder"')
    print(text[max(0, idx-50):idx+1500])
