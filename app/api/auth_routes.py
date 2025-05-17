from app.core.security import get_current_user
from app.db.base import get_db
from app.models import User
from app.schemas import Token, UserCreate, UserOut
from app.services.user_service import (handle_login, handle_logout,
                                       handle_signup, handle_token_refresh)
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Reusable dependencies
get_db_dep = Depends(get_db)
get_current_user_dep = Depends(get_current_user)


@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = get_db_dep):
    return handle_signup(user, db)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = get_db_dep):
    return JSONResponse(content=handle_login(form_data.username, form_data.password, db))


@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = get_db_dep):
    return handle_token_refresh(refresh_token, db)


@router.post("/logout")
def logout(
    current_user: User = get_current_user_dep,
    db: Session = get_db_dep,
    token: str = Security(oauth2_scheme),
):
    return handle_logout(current_user, db)
