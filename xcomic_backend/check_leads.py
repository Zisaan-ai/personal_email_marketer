
import sqlite3
conn = sqlite3.connect('sql_app.db')
cur = conn.cursor()
cur.execute('SELECT campaign_id, status FROM campaign_leads')
print(cur.fetchall())
conn.close()

