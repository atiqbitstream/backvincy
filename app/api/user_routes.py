from app.core.security import get_current_user
from app.db.base import get_db
from app.models import User
from app.schemas.user import UserOut, UserUpdate
from fastapi import  APIRouter, Depends, HTTPException, status
from app.core.security import require_role, get_current_user
from app.models.user import UserRole
from sqlalchemy.orm import Session
from uuid import UUID
from app.crud.user import (
    get_user_by_id, list_users, update_user, delete_user_and_related
)

router = APIRouter(tags=["users"])


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# --- Admin-only endpoints ---
admin_dep = Depends(require_role([UserRole.admin]))

@router.get("", response_model=list[UserOut], dependencies=[admin_dep])
def admin_list_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return list_users(db, skip, limit)

@router.get("/{user_id}", response_model=UserOut, dependencies=[admin_dep])
def admin_get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut, dependencies=[admin_dep])
def admin_update_user(
    user_id: UUID,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_user),
):
    data = payload.dict(exclude_unset=True)

    # If front-end sends {"status": "Inactive"}, map it to the model's user_status field
    if "status" in data:
        data["user_status"] = data.pop("status")

    data["updated_by"] = admin.email
    updated = update_user(db, user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[admin_dep])
def admin_delete_user(user_id: UUID, db: Session = Depends(get_db)):
    success = delete_user_and_related(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return