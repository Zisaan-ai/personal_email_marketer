with open('frontend/index.html', encoding='utf-8') as f:
    text = f.read()
    idx = text.find('id="cold-mail-builder"')
    if idx != -1:
        print(text[max(0, idx-50):idx+2500])
