import codecs
import re

html = codecs.open('frontend/index.html', 'r', 'utf-8').read()

# The specific Bengali text we want to write
correct_bengali = '<strong>Bangla:</strong> ডেভেলপার মোনেম রহমান জিসান কর্তৃক তৈরিকৃত। সিস্টেমের সম্পূর্ণ কন্ট্রোল এবং সিকিউরিটির জন্য একটি স্পেশাল অ্যাডমিন ড্যাশবোর্ড রয়েছে, যা শুধুমাত্র ডেভেলপার নিজেই ব্যবহার ও নিয়ন্ত্রণ করতে পারেন।'
new_p_tag = f'                      <p class="about-text bn" style="text-align:center; max-width: 800px; margin: 0 auto;">{correct_bengali}</p>'

# Replace whatever was there (which currently looks like '<strong>Bangla:</strong> ????')
html = re.sub(r'                      <p class="about-text bn" style="text-align:center; max-width: 800px; margin: 0 auto;"><strong>Bangla:</strong>.*?</p>', new_p_tag, html, flags=re.DOTALL)

codecs.open('frontend/index.html', 'w', 'utf-8').write(html)
print('Fixed Bengali Text via normal string replacement')
