import sqlite3
import os

db_path = 'backend/sql_app.db'
if not os.path.exists(db_path):
    print("sql_app.db not found!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def add_column(table, column, col_type):
    try:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
        print(f"Added {column} to {table}")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print(f"Column {column} already exists in {table}")
        else:
            print(f"Error adding {column}: {e}")

add_column("campaigns", "paused_reason", "VARCHAR")
add_column("campaigns", "sending_days", "VARCHAR")
add_column("campaigns", "start_hour", "INTEGER")
add_column("campaigns", "end_hour", "INTEGER")
add_column("campaigns", "timezone", "VARCHAR")
add_column("campaigns", "delay_min", "INTEGER")
add_column("campaigns", "delay_max", "INTEGER")
add_column("sending_accounts", "warmup_daily_limit", "INTEGER")
add_column("sending_accounts", "smart_limit_enabled", "BOOLEAN")

conn.commit()
conn.close()
print("Migrations complete")
