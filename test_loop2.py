import sys
import os
sys.path.append(os.path.abspath('C:/Users/higan/.gemini/antigravity/scratch/xcomic_sync/xcomic_backend'))
os.environ['DATABASE_URL'] = 'sqlite:///C:/Users/higan/.gemini/antigravity/scratch/xcomic_sync/sql_app_live.db'

from sqlalchemy.orm import Session
import database
import main_live

def test():
    db = database.SessionLocal()
    # Mock current_user
    current_user = db.query(database.User).filter(database.User.email == 'zmonemrahman@gmail.com').first()
    try:
        res = main_live.get_sending_accounts(current_user=current_user, db=db)
        print('Success, got', len(res))
    except Exception as e:
        import traceback
        traceback.print_exc()

test()
