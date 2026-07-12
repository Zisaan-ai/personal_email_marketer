import sys
import os

with open('backend/main.py', encoding='utf-8') as f:
    text = f.read()

# Add imports
if 'UploadFile' not in text:
    text = text.replace('from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks', 'from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, UploadFile, File')

if 'import shutil' not in text:
    text = 'import shutil\n' + text

# Add gallery endpoints
gallery_endpoints = '''
# ============================================================
# MEDIA GALLERY ENDPOINTS
# ============================================================
import uuid
from fastapi import UploadFile, File

@app.post("/api/gallery/upload")
async def upload_image(file: UploadFile = File(...), current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    ext = file.filename.split('.')[-1] if '.' in file.filename else 'png'
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", new_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    url = f"/uploads/{new_filename}"
    
    media = database.Media(
        user_id=str(current_user.id),
        filename=new_filename,
        original_name=file.filename,
        url=url
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    
    return {"status": "success", "media": {"id": media.id, "url": media.url, "name": media.original_name}}

@app.get("/api/gallery")
def get_gallery(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    media_files = db.query(database.Media).filter(database.Media.user_id == str(current_user.id)).order_by(database.Media.created_at.desc()).all()
    return [{"id": m.id, "url": m.url, "name": m.original_name, "created_at": m.created_at} for m in media_files]

@app.delete("/api/gallery/{media_id}")
def delete_media(media_id: str, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    media = db.query(database.Media).filter(database.Media.id == media_id, database.Media.user_id == str(current_user.id)).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
        
    file_path = os.path.join("uploads", media.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        
    db.delete(media)
    db.commit()
    return {"status": "success"}
'''

if '/api/gallery' not in text:
    text += gallery_endpoints

# Mount static uploads
if 'name="uploads"' not in text:
    mount_str = 'app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")\napp.mount("/",'
    text = text.replace('app.mount("/",', mount_str)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated main.py with gallery endpoints")
