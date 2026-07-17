import sys
import os
sys.path.append(os.path.abspath('/home/terapkco/xcomic_backend'))
os.environ['DATABASE_URL'] = 'sqlite:////home/terapkco/sql_app.db'
try:
    import main
    from database import SessionLocal, User
    import auth
    db = SessionLocal()
    user = db.query(User).filter(User.email == "zmonemrahman@gmail.com").first()
    res = main.get_sending_accounts(current_user=user, db=db)
    print("Success! Type:", type(res))
    if isinstance(res, dict) and "debug_error" in res:
        print("CAUGHT ERROR:", res["debug_error"])
        print(res["traceback"])
    else:
        print("First item:", res[0] if res else "empty")
except Exception as e:
    import traceback
    print("FATAL:", traceback.format_exc())
