# app/api/admin_user_hub.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from app.core.security import require_role
from app.db.base import get_db
from app.schemas.user_hub import UserHubCreate, UserHubUpdate, UserHubOut
from app.crud.user_hub import (
    create_user_hub, get_user_hub, get_all_user_hubs, 
    update_user_hub, delete_user_hub, toggle_user_hub_status,
    get_user_hubs_by_category, get_user_hub_by_email
)

router = APIRouter(
    prefix="/admin/user-hub",
    tags=["admin-user-hub"],
    dependencies=[Depends(require_role(["Admin"]))]
)

@router.post("/", response_model=UserHubOut)
def admin_create_user_hub(payload: UserHubCreate, db: Session = Depends(get_db)):
    """Create a new user hub entry"""
    # Check if email already exists
    existing_hub = get_user_hub_by_email(db, payload.email)
    if existing_hub:
        raise HTTPException(
            status_code=400, 
            detail="User with this email already exists in hub"
        )
    
    return create_user_hub(db, payload)

@router.get("/", response_model=List[UserHubOut])
def admin_list_user_hubs(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all user hub entries with optional status filter"""
    return get_all_user_hubs(db, skip=skip, limit=limit, status_filter=status)

@router.get("/category/{category}", response_model=List[UserHubOut])
def admin_get_user_hubs_by_category(
    category: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get user hub entries by category"""
    return get_user_hubs_by_category(db, category, skip=skip, limit=limit)

@router.get("/{hub_id}", response_model=UserHubOut)
def admin_get_user_hub(hub_id: UUID, db: Session = Depends(get_db)):
    """Get a specific user hub entry by ID"""
    hub = get_user_hub(db, hub_id)
    if not hub:
        raise HTTPException(status_code=404, detail="User hub entry not found")
    return hub

@router.put("/{hub_id}", response_model=UserHubOut)
def admin_update_user_hub(hub_id: UUID, payload: UserHubUpdate, db: Session = Depends(get_db)):
    """Update a user hub entry"""
    # Check if email is being changed and if it already exists
    if payload.email:
        existing_hub = get_user_hub_by_email(db, payload.email)
        if existing_hub and existing_hub.id != hub_id:
            raise HTTPException(
                status_code=400, 
                detail="User with this email already exists in hub"
            )
    
    hub = update_user_hub(db, hub_id, payload)
    if not hub:
        raise HTTPException(status_code=404, detail="User hub entry not found")
    return hub

@router.patch("/{hub_id}/toggle-status", response_model=UserHubOut)
def admin_toggle_user_hub_status(hub_id: UUID, db: Session = Depends(get_db)):
    """Toggle the status of a user hub entry"""
    hub = toggle_user_hub_status(db, hub_id)
    if not hub:
        raise HTTPException(status_code=404, detail="User hub entry not found")
    return hub

@router.delete("/{hub_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_user_hub(hub_id: UUID, db: Session = Depends(get_db)):
    """Delete a user hub entry"""
    if not delete_user_hub(db, hub_id):
        raise HTTPException(status_code=404, detail="User hub entry not found")