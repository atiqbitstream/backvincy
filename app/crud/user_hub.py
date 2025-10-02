# app/crud/user_hub.py
from sqlalchemy.orm import Session
from app.models.user_hub import UserHub
from app.schemas.user_hub import UserHubCreate, UserHubUpdate
from uuid import UUID

def create_user_hub(db: Session, user_hub: UserHubCreate) -> UserHub:
    db_user_hub = UserHub(**user_hub.dict())
    db.add(db_user_hub)
    db.commit()
    db.refresh(db_user_hub)
    return db_user_hub

def get_user_hub(db: Session, hub_id: UUID) -> UserHub:
    return db.query(UserHub).filter(UserHub.id == hub_id).first()

def get_user_hub_by_email(db: Session, email: str) -> UserHub:
    return db.query(UserHub).filter(UserHub.email == email).first()

def get_all_user_hubs(db: Session, skip: int = 0, limit: int = 100, status_filter: bool = None):
    query = db.query(UserHub)
    if status_filter is not None:
        query = query.filter(UserHub.status == status_filter)
    return query.order_by(UserHub.created_at.desc()).offset(skip).limit(limit).all()

def get_user_hubs_by_category(db: Session, category: str, skip: int = 0, limit: int = 100):
    return db.query(UserHub).filter(
        UserHub.category == category,
        UserHub.status == True
    ).order_by(UserHub.created_at.desc()).offset(skip).limit(limit).all()

def update_user_hub(db: Session, hub_id: UUID, hub_update: UserHubUpdate) -> UserHub:
    db_user_hub = get_user_hub(db, hub_id)
    if db_user_hub:
        for key, value in hub_update.dict(exclude_unset=True).items():
            setattr(db_user_hub, key, value)
        db.commit()
        db.refresh(db_user_hub)
    return db_user_hub

def delete_user_hub(db: Session, hub_id: UUID):
    db_user_hub = get_user_hub(db, hub_id)
    if db_user_hub:
        db.delete(db_user_hub)
        db.commit()
        return True
    return False

def toggle_user_hub_status(db: Session, hub_id: UUID):
    db_user_hub = get_user_hub(db, hub_id)
    if db_user_hub:
        db_user_hub.status = not db_user_hub.status
        db.commit()
        db.refresh(db_user_hub)
    return db_user_hub