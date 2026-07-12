with open('backend/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

test_reply_code = '''
@app.get('/api/track/test_reply/{campaign_id}/{contact_id}')
def track_test_reply(campaign_id: str, contact_id: str, db: Session = Depends(database.get_db)):
    campaign = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
    lead = db.query(database.CampaignLead).filter(database.CampaignLead.id == contact_id).first()
    if campaign and lead:
        reply = database.Reply(
            account_id="test_account",
            sender_email=lead.email,
            subject="Re: " + (campaign.subject or "Test"),
            body="This is a test reply",
            sentiment="Interested"
        )
        db.add(reply)
        if lead.status != 'replied':
            lead.status = 'replied'
        db.commit()
    return {"status": "Reply injected"}
'''

if 'test_reply' not in text:
    text = text.replace('# --- REPLIES ENDPOINT ---', test_reply_code + '\n# --- REPLIES ENDPOINT ---')
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Added test reply endpoint')
