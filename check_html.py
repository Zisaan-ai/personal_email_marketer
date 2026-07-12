with open('frontend/index.html', encoding='utf-8') as f:
    text = f.read()
    idx = text.find('id="campaign-builder"')
    if idx != -1:
        print(text[max(0, idx-100):idx+2500])
