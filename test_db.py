import sys, json
sys.path.append('backend')
import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///backend/data.db')
Session = sessionmaker(bind=engine)
db = Session()
leads = db.query(database.CampaignLead).all()
print(json.dumps([{'email': l.email, 'status': l.status, 'campaign_id': l.campaign_id} for l in leads]))

campaigns = db.query(database.Campaign).all()
print(json.dumps([{'id': c.id, 'sent_count': c.sent_count, 'sent_count_a': c.sent_count_a, 'sent_count_b': c.sent_count_b} for c in campaigns]))
