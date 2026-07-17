import sqlite3

conn = sqlite3.connect(r"C:\Users\higan\.gemini\antigravity\scratch\xcomic_sync\xcomic_backend\sql_app.db")
cursor = conn.cursor()

cursor.execute("SELECT id, email FROM users")
users = cursor.fetchall()
print("All users:")
for u in users:
    print(u)

cursor.execute("SELECT DISTINCT user_id FROM sending_accounts")
sending_account_user_ids = cursor.fetchall()
print("\nUnique user_ids in sending_accounts:")
for sa in sending_account_user_ids:
    print(sa)
    
conn.close()
