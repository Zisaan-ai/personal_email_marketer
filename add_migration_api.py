import sys

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

migration_code = """
@app.get("/api/migrate-db")
def migrate_db_endpoint(db: Session = Depends(database.get_db)):
    try:
        from sqlalchemy import text
        queries = [
            "ALTER TABLE campaigns ADD COLUMN paused_reason VARCHAR",
            "ALTER TABLE campaigns ADD COLUMN sending_days VARCHAR",
            "ALTER TABLE campaigns ADD COLUMN start_hour INTEGER",
            "ALTER TABLE campaigns ADD COLUMN end_hour INTEGER",
            "ALTER TABLE sending_accounts ADD COLUMN smart_limit_enabled BOOLEAN"
        ]
        results = []
        for q in queries:
            try:
                db.execute(text(q))
                results.append(f"Success: {q}")
            except Exception as ex:
                results.append(f"Failed: {q} - {str(ex)}")
        db.commit()
        return {"status": "done", "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}

"""

if "/api/migrate-db" not in content:
    # Insert before the preflight endpoint
    content = content.replace('@app.post("/api/preflight")', migration_code + '@app.post("/api/preflight")')
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Migration endpoint added.")
else:
    print("Migration endpoint already exists.")
