from app.models import User
from app.schemas import UserCreate
from passlib.context import CryptContext
from app.models.user import UserStatus
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email,
        password_hash=hashed_password,
        role=user.role,
        full_name=user.full_name,
        gender=user.gender,
        dob=user.dob,
        nationality=user.nationality,
        phone=user.phone,
        city=user.city,
        country=user.country,
        occupation=user.occupation,
        marital_status=user.marital_status,
        sleep_hours=user.sleep_hours,
        exercise_frequency=user.exercise_frequency,
        smoking_status=user.smoking_status,
        alcohol_consumption=user.alcohol_consumption,
        user_status=UserStatus.active,  # Default to "Active"
        created_by=user.email,  # Set created_by to the user's email
        updated_by=user.email,  # Set updated_by to the user's email)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def set_refresh_token(db: Session, user: User, token: str):
    user.refresh_token = token
    db.commit()
    db.refresh(user)
