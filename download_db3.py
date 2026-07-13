import ftplib
import io
import sqlite3

ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')

with open('sql_app.db', 'wb') as f:
    ftp.retrbinary('RETR xcomic_backend/sql_app.db', f.write)

ftp.quit()
print('Downloaded DB!')

conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()
cursor.execute("UPDATE users SET is_approved=1, is_admin=1 WHERE email='zonemrahman@gmail.com'")
conn.commit()
print('Activated user.')
conn.close()

ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')
with open('sql_app.db', 'rb') as f:
    ftp.storbinary('STOR xcomic_backend/sql_app.db', f)
ftp.storbinary('STOR xcomic_backend/tmp/restart.txt', io.BytesIO(b''))
ftp.quit()
print('Uploaded modified DB!')

