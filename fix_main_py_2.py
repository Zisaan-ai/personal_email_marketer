with open('backend/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_func_body = '''    db = database.SessionLocal()
    try:
        now = datetime.utcnow()
        scheduled_camps = db.query(database.Campaign).filter(
            database.Campaign.status == 'scheduled',
            database.Campaign.scheduled_at <= now
        ).all()
        for camp in scheduled_camps:
            print(f"[scheduler] Auto-starting scheduled campaign {camp.id}")
            camp.status = 'processing'
            db.commit()
            threading.Thread(
                target=process_isolated_campaign,
                args=(str(camp.id),),
                daemon=True
            ).start()
    except Exception as e:
        print(f"[scheduler] Start scheduled error: {e}")
    finally:
        db.close()'''

new_func_body = '''    db = database.SessionLocal()
    try:
        scheduled_camps = db.query(database.Campaign).filter(
            database.Campaign.status == 'scheduled',
            database.Campaign.scheduled_at != None
        ).all()
        for camp in scheduled_camps:
            try:
                tz = pytz.timezone(camp.timezone or "UTC")
                run_date = camp.scheduled_at
                if run_date.tzinfo is None:
                    run_date = tz.localize(run_date)
                
                now = datetime.now(tz)
                if run_date <= now:
                    print(f"[scheduler] Auto-starting scheduled campaign {camp.id}")
                    camp.status = 'processing'
                    db.commit()
                    threading.Thread(
                        target=process_isolated_campaign,
                        args=(str(camp.id),),
                        daemon=True
                    ).start()
            except Exception as inner_e:
                print(f"[scheduler] Error parsing time for camp {camp.id}: {inner_e}")
    except Exception as e:
        print(f"[scheduler] Start scheduled error: {e}")
    finally:
        db.close()'''

if old_func_body in text:
    text = text.replace(old_func_body, new_func_body)

startup_old = '''        now = datetime.utcnow()
        stuck = db.query(database.Campaign).filter(
            database.Campaign.status.in_(['processing', 'scheduled'])
        ).all()
        # Only resume scheduled if their time has come
        stuck = [c for c in stuck if c.status == 'processing' or (c.status == 'scheduled' and c.scheduled_at and c.scheduled_at <= now)]'''

startup_new = '''        stuck = db.query(database.Campaign).filter(
            database.Campaign.status.in_(['processing', 'scheduled'])
        ).all()
        
        valid_stuck = []
        for c in stuck:
            if c.status == 'processing':
                valid_stuck.append(c)
            elif c.status == 'scheduled' and c.scheduled_at:
                try:
                    tz = pytz.timezone(c.timezone or "UTC")
                    run_date = c.scheduled_at
                    if run_date.tzinfo is None:
                        run_date = tz.localize(run_date)
                    now = datetime.now(tz)
                    if run_date <= now:
                        valid_stuck.append(c)
                except Exception:
                    pass
        stuck = valid_stuck'''

if startup_old in text:
    text = text.replace(startup_old, startup_new)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Success')
