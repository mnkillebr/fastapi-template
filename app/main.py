from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, login
from app.core.db import init_db
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, Action

app = FastAPI()

# Add CORS middleware to allow requests from your Next.js app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def greet_user(name: str):
    return f"Hello {name}"

sdk = CopilotKitRemoteEndpoint(
    actions=[
        Action(
            name="greet_user",
            handler=greet_user,
            description="Greet the user",
            parameters=[
                {
                    "name": "name",
                    "type": "string",
                    "description": "The name of the user"
                }
            ]
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