from fastapi import FastAPI
from app.routers import users, login
from app.core.db import init_db

app = FastAPI()

app.include_router(login.router)
app.include_router(users.router)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI server"}