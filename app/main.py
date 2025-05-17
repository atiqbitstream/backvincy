from app.api import  auth_routes, user_routes
from app.db.base import Base, engine
from fastapi import FastAPI
from app.models import * 

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FortiFund Backend",
    description="Backend API for FortiFund platform",
    version="1.0.0",
)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)

