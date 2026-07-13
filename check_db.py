import ftplib
import io
import sqlite3

ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')

with open('sql_app.db', 'wb') as f:
    ftp.retrbinary('RETR xcomic_backend/sql_app.db', f.write)

ftp.quit()

conn = sqlite3.connect('sql_app.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM campaigns ORDER BY created_at DESC LIMIT 1")
row = cursor.fetchone()
if row:
    print('Campaign DB values:')
    for key in row.keys():
        print(f'{key}: {row[key]}')
else:
    print('No campaigns found.')
conn.close()
