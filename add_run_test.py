with open('backend/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

run_test_code = '''
@app.get('/api/run_test')
def run_test_endpoint(db: Session = Depends(database.get_db)):
    # Find any user
    user = db.query(database.User).first()
    if not user:
        return {"status": "error", "message": "No user found"}
    
    # 1. Create Newsletter Campaign
    news_camp = database.Campaign(
        subject="Test Newsletter Open Click Reply",
        body="<p>Test <a href='https://google.com'>Link</a></p>",
        type="newsletter",
        user_id=user.id,
        status="completed",
        sent_count=1,
        opens=1,
        clicks=1
    )
    db.add(news_camp)
    db.commit()
    
    # Add a reply for Newsletter
    db.add(database.Reply(
        account_id="test",
        sender_email="test@newsletter.com",
        subject="Re: Test Newsletter Open Click Reply",
        body="Reply to newsletter",
        sentiment="Interested"
    ))
    db.commit()

    # 2. Create Cold Mail Campaign
    cold_camp = database.Campaign(
        subject="Test Cold Mail Open Click Reply",
        body="<p>Test <a href='https://google.com'>Link</a></p>",
        type="cold_mail",
        user_id=user.id,
        status="completed",
        sent_count=1,
        opens=1,
        clicks=1
    )
    db.add(cold_camp)
    db.commit()
    
    # Add a reply for Cold Mail
    db.add(database.Reply(
        account_id="test",
        sender_email="test@coldmail.com",
        subject="Re: Test Cold Mail Open Click Reply",
        body="Reply to cold mail",
        sentiment="Interested"
    ))
    db.commit()
    
    return {"status": "success", "message": "Test campaigns with opens, clicks, replies created"}
'''

if 'run_test_endpoint' not in text:
    text = text.replace('# --- REPLIES ENDPOINT ---', run_test_code + '\n# --- REPLIES ENDPOINT ---')
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Added /api/run_test endpoint')
