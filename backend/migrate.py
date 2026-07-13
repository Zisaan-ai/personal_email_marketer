from database import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE campaigns ADD COLUMN selected_sender_ids TEXT"))
        conn.commit()
    print("Column added successfully.")
except Exception as e:
    print("Migration failed (column might already exist):", e)
