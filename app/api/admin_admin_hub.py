# app/api/admin_admin_hub.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
import os
import uuid
from pathlib import Path

from app.core.security import require_role
from app.db.base import get_db
from app.schemas.admin_hub import AdminHubCreate, AdminHubUpdate, AdminHubOut
from app.crud.admin_hub import create_admin_hub, get_admin_hub, get_all_admin_hubs, update_admin_hub, delete_admin_hub

router = APIRouter(
    prefix="/admin/hub",
    tags=["admin-hub"],
    dependencies=[Depends(require_role(["Admin"]))]
)

# Upload directory for hub images
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def is_allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

@router.post("/", response_model=AdminHubOut)
def admin_create_hub(payload: AdminHubCreate, db: Session = Depends(get_db)):
    """Create a new hub category"""
    return create_admin_hub(db, payload)

@router.post("/with-image", response_model=AdminHubOut)
async def admin_create_hub_with_image(
    category: str = Form(...),
    page_heading: Optional[str] = Form("Hub"),
    page_subtext: Optional[str] = Form("Explore Categories of Interest"),
    description: Optional[str] = Form(None),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Create a new hub category with image upload"""
    
    # Check if file is provided and valid
    if not image.filename:
        raise HTTPException(status_code=400, detail="No image file provided")
    
    if not is_allowed_file(image.filename):
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size (5MB limit)
    content = await image.read()
    if len(content) > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(status_code=400, detail="File size too large. Maximum 5MB allowed")
    
    # Generate unique filename
    file_extension = Path(image.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Create hub with image URL
    image_url = f"/uploads/{unique_filename}"
    hub_data = AdminHubCreate(
        page_heading=page_heading,
        page_subtext=page_subtext,
        category=category,
        description=description,
        image_url=image_url
    )
    
    return create_admin_hub(db, hub_data)

@router.get("/", response_model=List[AdminHubOut])
def admin_list_hubs(db: Session = Depends(get_db)):
    """Get all hub categories"""
    return get_all_admin_hubs(db)

@router.get("/{hub_id}", response_model=AdminHubOut)
def admin_get_hub(hub_id: UUID, db: Session = Depends(get_db)):
    """Get a specific hub category by ID"""
    hub = get_admin_hub(db, hub_id)
    if not hub:
        raise HTTPException(status_code=404, detail="Hub category not found")
    return hub

@router.put("/{hub_id}", response_model=AdminHubOut)
def admin_update_hub(hub_id: UUID, payload: AdminHubUpdate, db: Session = Depends(get_db)):
    """Update a hub category"""
    hub = update_admin_hub(db, hub_id, payload)
    if not hub:
        raise HTTPException(status_code=404, detail="Hub category not found")
    return hub

@router.put("/{hub_id}/with-image", response_model=AdminHubOut)
async def admin_update_hub_with_image(
    hub_id: UUID,
    category: str = Form(...),
    page_heading: Optional[str] = Form("Hub"),
    page_subtext: Optional[str] = Form("Explore Categories of Interest"),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Update a hub category with optional image upload"""
    
    # Check if hub exists
    existing_hub = get_admin_hub(db, hub_id)
    if not existing_hub:
        raise HTTPException(status_code=404, detail="Hub category not found")
    
    image_url = existing_hub.image_url  # Keep existing image by default
    
    # Process new image if provided
    if image and image.filename:
        if not is_allowed_file(image.filename):
            raise HTTPException(
                status_code=400, 
                detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Check file size (5MB limit)
        content = await image.read()
        if len(content) > 5 * 1024 * 1024:  # 5MB
            raise HTTPException(status_code=400, detail="File size too large. Maximum 5MB allowed")
        
        # Generate unique filename
        file_extension = Path(image.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save file
        try:
            with open(file_path, "wb") as buffer:
                buffer.write(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
        # Update image URL
        image_url = f"/uploads/{unique_filename}"
        
        # Optional: Delete old image file
        if existing_hub.image_url and existing_hub.image_url.startswith("/uploads/"):
            old_filename = existing_hub.image_url.replace("/uploads/", "")
            old_file_path = UPLOAD_DIR / old_filename
            if old_file_path.exists():
                try:
                    os.remove(old_file_path)
                except OSError:
                    pass  # Continue even if deletion fails
    
    # Update hub
    hub_data = AdminHubUpdate(
        page_heading=page_heading,
        page_subtext=page_subtext,
        category=category,
        description=description,
        image_url=image_url
    )
    
    return update_admin_hub(db, hub_id, hub_data)

@router.delete("/{hub_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_hub(hub_id: UUID, db: Session = Depends(get_db)):
    """Delete a hub category"""
    
    # Get hub to check for image
    hub = get_admin_hub(db, hub_id)
    if not hub:
        raise HTTPException(status_code=404, detail="Hub category not found")
    
    # Delete associated image file if exists
    if hub.image_url and hub.image_url.startswith("/uploads/"):
        filename = hub.image_url.replace("/uploads/", "")
        file_path = UPLOAD_DIR / filename
        if file_path.exists():
            try:
                os.remove(file_path)
            except OSError:
                pass  # Continue even if deletion fails
    
    # Delete hub from database
    if not delete_admin_hub(db, hub_id):
        raise HTTPException(status_code=404, detail="Hub category not found")