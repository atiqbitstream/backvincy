# app/crud/admin_hub.py
from sqlalchemy.orm import Session
from app.models.admin_hub import AdminHub
from app.models.user_hub import UserHub
from app.schemas.admin_hub import AdminHubCreate, AdminHubUpdate
from uuid import UUID

def create_admin_hub(db: Session, admin_hub: AdminHubCreate) -> AdminHub:
    db_admin_hub = AdminHub(**admin_hub.dict())
    db.add(db_admin_hub)
    db.commit()
    db.refresh(db_admin_hub)
    return db_admin_hub

def get_admin_hub(db: Session, hub_id: UUID) -> AdminHub:
    return db.query(AdminHub).filter(AdminHub.id == hub_id).first()

def get_all_admin_hubs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AdminHub).order_by(AdminHub.created_at.desc()).offset(skip).limit(limit).all()

def update_admin_hub(db: Session, hub_id: UUID, hub_update: AdminHubUpdate) -> AdminHub:
    db_admin_hub = get_admin_hub(db, hub_id)
    if db_admin_hub:
        # Store old category name for syncing
        old_category = db_admin_hub.category
        
        # Update admin hub
        for key, value in hub_update.dict(exclude_unset=True).items():
            setattr(db_admin_hub, key, value)
        
        # If category name changed, update all user_hub records with the old category
        if hub_update.category and hub_update.category != old_category:
            db.query(UserHub).filter(UserHub.category == old_category).update(
                {UserHub.category: hub_update.category}
            )
        
        db.commit()
        db.refresh(db_admin_hub)
    return db_admin_hub

def delete_admin_hub(db: Session, hub_id: UUID):
    db_admin_hub = get_admin_hub(db, hub_id)
    if db_admin_hub:
        # Store category name for cleanup
        category_name = db_admin_hub.category
        
        # Delete the admin hub
        db.delete(db_admin_hub)
        
        # Optional: Delete all user_hub records with this category
        # or you could set them to a different status/category
        db.query(UserHub).filter(UserHub.category == category_name).delete()
        
        db.commit()
        return True
    return False