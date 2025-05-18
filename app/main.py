from app.api import  auth_routes, user_routes,device_controls_routes, health_monitoring_routes
from app.db.base import Base, engine

from fastapi import FastAPI
from app.models import * 
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FortiFund Backend",
    description="Backend API for FortiFund platform",
    version="1.0.0",
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount your routers
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(device_controls_routes.router, tags=["device-controls"])
app.include_router(health_monitoring_routes.router, tags=["health-monitoring"])