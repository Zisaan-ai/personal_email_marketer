import codecs

with codecs.open('frontend/index.html', 'r', 'utf-8') as f:
    html = f.read()

bad_str = "this.innerHTML=el.type==='password'?'<i class='fa-regular fa-eye'></i>':'<i class='fa-regular fa-eye-slash'></i>'"
good_str = "this.innerHTML=el.type==='password'?'<i class=\"fa-regular fa-eye\"></i>':'<i class=\"fa-regular fa-eye-slash\"></i>'"

html = html.replace(bad_str, good_str)

with codecs.open('frontend/index.html', 'w', 'utf-8') as f:
    f.write(html)
