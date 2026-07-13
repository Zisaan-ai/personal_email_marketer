import base64, codecs, re

b64_str = b'ICAgICAgICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJhYm91dC10ZXh0IGJuIiBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7IG1heC13aWR0aDogODAwcHg7IG1hcmdpbjogMCBhdXRvOyI+PHN0cm9uZz5CYW5nbGE6PC9zdHJvbmc+IOCmoeCnh+CmrOCnh+CmsuCmqOCmvuCmsCDgpq7gp4vgpqjg4KeH4KauIOCmsOCmueCmruCmvuCmqCDgppzgpr/gprjgpr7gpqgg4KaV4Kaw4KeN4Kak4KeD4KaVIOCmpOCri+CmsOCmv+CmluCng+CmpOOBpyDgpprjpr/gprjgp43gpp/gp4fgpq7gp4fgprAg4Ka44Kau4KeN4Kam4KeC4Kaw4KeN4KajIOCmleCmqOCnjeCmn+CnjeCmsOCni+CmsiDgpo/gpqzgongg4Ka44Ka/4KaV4Ka/4KaD4Kaw4Ka/4Kaf4Ka/4KawIOCmnOCmq+CnjeCmrCDgpo/gppXgpp/gpr8g4Ka44KeN4Kaf4KeH4Ka24Ka+4KayIOCmj+CnjeCmr+CmvuCmoeCmruCpr+CmqCDgpqHgpr/gpr7gprbgpqzgpr7gprDgp43gpqEg4Kaw4Kef4KeH4Kib4KeHLCDgpq/gpr4g4Ka24KeB4Kan4KeB4Kau4Ka+4Kak4KeN4KawIOCmoeCnh+CmrOCnh+CmsuCmqOCmvuCmsCDgpqjgpr/gppzgp4fgppgg4Kaz4KeN4Kav4Kas4Ka54Ka+4KawIOCTIOCmqOCmv+Cmr+CmqOCnjeCmpOCnjeCmsOCmqCDgppXgprDgpqTg4KeHIOCmquCmvuCmsOCnh+CmqOOBpzwvcD4='
repl = base64.b64decode(b64_str).decode('utf-8')

html = codecs.open('frontend/index.html', 'r', 'utf-8').read()

# Replace the specific Bangla text for the 18th card
html = re.sub(r'                      <p class="about-text bn" style="text-align:center; max-width: 800px; margin: 0 auto;"><strong>Bangla:</strong>.*?</p>', repl, html, flags=re.DOTALL)

codecs.open('frontend/index.html', 'w', 'utf-8').write(html)
print('Fixed Bengali Text via Base64')
