import codecs

with codecs.open('frontend/index.html', 'r', 'utf-8') as f:
    html = f.read()

# The broken string has class="fa-regular fa-eye"
broken_str = "this.innerHTML=el.type==='password'?'<i class=\"fa-regular fa-eye\"></i>':'<i class=\"fa-regular fa-eye-slash\"></i>'"
fixed_str = "this.innerHTML=el.type==='password'?'<i class=&quot;fa-regular fa-eye&quot;></i>':'<i class=&quot;fa-regular fa-eye-slash&quot;></i>'"

html = html.replace(broken_str, fixed_str)

with codecs.open('frontend/index.html', 'w', 'utf-8') as f:
    f.write(html)
