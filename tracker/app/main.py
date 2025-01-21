from fastapi import FastAPI
from .db import create_db_and_tables
from app.api.api_card import cards_router
from app.api.api_pick import picks_router
from app.api.api_users import users_router
from app.api.api_fights import fights_router
from app.api.api_fighers import fighters_router


app = FastAPI()
app.include_router(cards_router, prefix="/api", tags=["API Cards"])
app.include_router(picks_router, prefix="/api", tags=["API Picks"])
app.include_router(users_router, prefix="/api", tags=["API Users"])
app.include_router(fights_router, prefix="/api", tags=["API Fights"])
app.include_router(fighters_router, prefix="/api", tags=["API Fighters"])


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def home():
    return {"Hello": "World"}
