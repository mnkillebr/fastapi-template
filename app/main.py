from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, login
from app.core.db import init_db
from app.dependencies import get_session
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, Action
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.services.user_service import fetch_all_users
from typing import List

app = FastAPI()

# Add CORS middleware to allow requests from your Next.js app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

async def get_all_users():
    users = await fetch_all_users()
    return users

sdk = CopilotKitRemoteEndpoint(
    actions=[
        Action(
            name="get_all_users",
            handler=get_all_users,
            description="Get all the users",
            parameters=None
        )
    ]
)

add_fastapi_endpoint(app, sdk, "/copilotkit")

app.include_router(login.router)
app.include_router(users.router)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI server"}