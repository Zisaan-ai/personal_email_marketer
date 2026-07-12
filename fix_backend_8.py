import sys

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_endpoint = """class ScheduleUpdate(BaseModel):
    sending_days: Optional[str] = None
    start_hour: Optional[int] = None
    end_hour: Optional[int] = None
    timezone: Optional[str] = None

@app.post("/api/campaigns/{campaign_id}/save-schedule")
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

@app.post("/api/campaigns/{campaign_id}/pause")"""

if "/api/campaigns/{campaign_id}/save-schedule" not in content:
    content = content.replace('@app.post("/api/campaigns/{campaign_id}/pause")', new_endpoint)
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added save-schedule API")
else:
    print("save-schedule API already exists")
