# app/api/user_user_hub.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.core.security import get_current_user
from app.db.base import get_db
from app.schemas.user_hub import UserHubCreate, UserHubUpdate, UserHubOut
from app.crud.user_hub import (
    create_user_hub, get_user_hub, get_all_user_hubs, 
    update_user_hub, delete_user_hub, get_user_hubs_by_category, 
    get_user_hub_by_email
)

router = APIRouter(
    prefix="/user-hub",
    tags=["user-hub"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=UserHubOut)
def create_user_hub_entry(
    payload: UserHubCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new user hub entry"""
    # Add the logged-in user's name to created_by field
    payload.created_by = current_user.full_name or current_user.email
    
    return create_user_hub(db, payload)

@router.get("/", response_model=List[UserHubOut])
def list_active_user_hubs(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all active user hub entries (status=True only)"""
    return get_all_user_hubs(db, skip=skip, limit=limit, status_filter=True)

@router.get("/category/{category}", response_model=List[UserHubOut])
def get_user_hubs_by_category_public(
    category: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get active user hub entries by category"""
    return get_user_hubs_by_category(db, category, skip=skip, limit=limit)

@router.get("/{hub_id}", response_model=UserHubOut)
def get_user_hub_entry(
    hub_id: UUID, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific user hub entry by ID"""
    hub = get_user_hub(db, hub_id)
    if not hub:
        raise HTTPException(status_code=404, detail="User hub entry not found")
    
    # Only show active entries to regular users
    if not hub.status:
        raise HTTPException(status_code=404, detail="User hub entry not found")
    
    return hub

@router.put("/{hub_id}", response_model=UserHubOut)
def update_user_hub_entry(
    hub_id: UUID, 
    payload: UserHubUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a user hub entry"""
    # Check if the hub exists first
    existing_hub = get_user_hub(db, hub_id)
    if not existing_hub:
        raise HTTPException(status_code=404, detail="User hub entry not found")
    
    # Check if email is being changed and if it already exists
    if payload.email:
        email_hub = get_user_hub_by_email(db, payload.email)
        if email_hub and email_hub.id != hub_id:
            raise HTTPException(
                status_code=400, 
                detail="User with this email already exists in hub"
            )
    
    hub = update_user_hub(db, hub_id, payload)
    return hub

@router.delete("/{hub_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_hub_entry(
    hub_id: UUID, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a user hub entry"""
    if not delete_user_hub(db, hub_id):
        raise HTTPException(status_code=404, detail="User hub entry not found")