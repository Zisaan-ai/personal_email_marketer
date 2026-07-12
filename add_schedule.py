import sys
with open('backend/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_endpoint = """
class ScheduleUpdate(BaseModel):
    sending_days: Optional[str] = None
    start_hour: Optional[int] = None
    end_hour: Optional[int] = None
    timezone: Optional[str] = None

@app.post("/api/campaigns/{campaign_id}/schedule")
def save_campaign_schedule(campaign_id: str, schedule: ScheduleUpdate, db: Session = Depends(database.get_db)):
    camp = db.query(database.Campaign).filter(database.Campaign.id == campaign_id).first()
    if not camp:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    camp.sending_days = schedule.sending_days
    camp.start_hour = schedule.start_hour
    camp.end_hour = schedule.end_hour
    camp.timezone = schedule.timezone
    db.commit()
    return {"status": "success"}

@app.get("/api/campaigns")"""

text = text.replace('@app.get("/api/campaigns")', new_endpoint)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Added save_schedule endpoint")
