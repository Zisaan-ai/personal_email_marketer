import sqlite3

def application(environ, start_response):
    conn = sqlite3.connect('sql_app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email='zmonemrahman@gmail.com'")
    admin = cursor.fetchone()
    
    if admin:
        cursor.execute("SELECT email FROM sending_accounts WHERE user_id=?", (admin[0],))
        accounts = cursor.fetchall()
        output = f"Admin ID: {admin[0]}\nAccounts: {accounts}".encode('utf-8')
    else:
        output = b"Admin not found"
        
    conn.close()
    
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [output]
