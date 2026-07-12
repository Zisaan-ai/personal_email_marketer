with open('frontend/index.html', encoding='utf-8') as f:
    text = f.read()
    idx = text.find('id="cold-tab-analytics"')
    end_idx = text.find('<!-- LEADS TAB -->', idx)
    print(text[max(0, idx-50):end_idx])
