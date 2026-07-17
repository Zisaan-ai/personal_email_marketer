import sys
from ftplib import FTP

php_script = '<?php\n'
php_script += '\ = shell_exec("cd /home/terapkco/xcomic_backend && /home/terapkco/virtualenv/xcomic_backend/3.11/bin/python test_followup.py 2>&1");\n'
php_script += 'echo "<pre>\</pre>";\n'
php_script += '?>\n'

php_script = php_script.replace('\$', '$')

with open('test_followup.php', 'w') as f:
    f.write(php_script)

ftp = FTP('xcomic.xyz', timeout=10)
ftp.login('terapkco', '(3#JCk2Vyn94hY')
ftp.cwd('xcomic.xyz')
with open('test_followup.php', 'rb') as f:
    ftp.storbinary('STOR test_followup.php', f)
ftp.cwd('/xcomic_backend')
with open('test_followup.py', 'rb') as f:
    ftp.storbinary('STOR test_followup.py', f)
ftp.quit()
print("PHP script and Python test script uploaded.")
