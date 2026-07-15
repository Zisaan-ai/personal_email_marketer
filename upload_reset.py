import ftplib, io

ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')
ftp.cwd('xcomic_backend')

script = b"import sys, os\nsys.path.insert(0, os.path.dirname(os.path.abspath('__file__')))\nimport warmup_service\nwarmup_service.reset_daily_warmup_counts()\nprint('RESET DONE')\n"

ftp.storbinary('STOR run_reset_now.py', io.BytesIO(script))
print('Script uploaded to server')
ftp.quit()
