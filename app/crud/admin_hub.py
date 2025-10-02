# app/crud/admin_hub.py
from sqlalchemy.orm import Session
from app.models.admin_hub import AdminHub
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
        for key, value in hub_update.dict(exclude_unset=True).items():
            setattr(db_admin_hub, key, value)
        db.commit()
        db.refresh(db_admin_hub)
    return db_admin_hub

def delete_admin_hub(db: Session, hub_id: UUID):
    db_admin_hub = get_admin_hub(db, hub_id)
    if db_admin_hub:
        db.delete(db_admin_hub)
        db.commit()
        return True
    return False