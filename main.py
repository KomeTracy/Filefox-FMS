from fastapi import FastAPI, HTTPException, Depends, status, Body, File, UploadFile
from pydantic import BaseModel
from typing import List, Annotated
from secrets import token_hex
import models, json
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import File, Permission

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    return {"message": "File uploaded successfully"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_extension = file.filename.split(".").pop()
    file_name = token_hex(12)
    file_path = f"{file_name}.{file_extension}"
    with open (file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    # new_file = File(name=file.filename, path=file_path)  
    # db.add(new_file)
    # db.commit()
    # db.refresh(new_file)  # Refresh the object to get the generated ID
    return {"success":True, "file_path":file_path, "message":"File successfully uploaded" }

@app.delete("/files/{file_id}")
async def delete_file(file_id: int, db: Session = Depends(get_db)):
    file_to_delete = db.query(File).filter(File.id == file_id).first()
    if not file_to_delete:
        raise HTTPException(status_code=404, detail="File not found")
    
@app.post("/files/{file_id}/permissions")
async def grant_file_permission(file_id: int, user_id: int, permission_level: str, db: Session = Depends(get_db)):
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    permission = Permission(file_id=file_id, user_id=user_id)
    if permission_level == "read":
        permission.can_read = True
    elif permission_level == "write":
        permission.can_write = True
    elif permission_level == "readwrite":
        permission.can_read = True
        permission.can_write = True
    else:
        raise HTTPException(status_code=400, detail="Invalid permission level")
    db.add(permission)
    db.commit()

    return {"message": "Permission granted successfully"}

@app.post("/folder/{folder_id}/file")
async def add_file_to_folder(folder_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    if folder:
        folder.last_updated = datetime.datetime.now()
        db.commit()

    return {"success": True, "message": "File uploaded successfully and added to folder",}

@app.delete("/folders/{folder_id}")
async def delete_folder(folder_id: int, db: Session = Depends(get_db)):
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    db.delete(folder)
    db.commit()

    return {"message": "Folder deleted successfully"}

@app.post("/folders/{folder_id}/permissions")
async def grant_folder_permission(folder_id: int, user_id: int, permission_level: str, db: Session = Depends(get_db)):
    permission = Permission(folder_id=folder_id, user_id=user_id)
    if permission_level == "read":
        permission.can_read = True
    elif permission_level == "write":
        permission.can_write = True
    elif permission_level == "readwrite":
        permission.can_read = True
        permission.can_write = True
    else:
        raise HTTPException(status_code=400, detail="Invalid permission level")
    db.add(permission)
    db.commit()

    return {"message": "Permission granted successfully"}


