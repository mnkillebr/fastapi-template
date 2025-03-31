from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Any
from app.models.user import Token, UserCreate, User
from app.core import security
from app.dependencies import get_session

router = APIRouter(prefix="/login", tags=["login"])

@router.post("/access-token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_session)):
    query = select(User).where(User.email == form_data.username)
    result = await session.execute(query)
    db_user = result.scalar_one_or_none()
    if not db_user or not security.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token_data = {"sub": str(db_user.id)}
    access_token = security.create_access_token(token_data)
    return {"access_token": access_token}