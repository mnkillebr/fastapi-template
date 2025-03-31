from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserCreate, UserRead, UserRegister, UserUpdate, Token
from app.core import security
from app.dependencies import get_session, get_current_user
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserRead)
async def register(user: UserRegister, session: AsyncSession = Depends(get_session)):
    query = select(User).where(User.email == user.email)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = security.hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_pw, full_name=user.full_name)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@router.get("/", response_model=List[UserRead])
async def read_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@router.get("/me", response_model=UserRead, response_model_exclude={"is_admin", "is_active"})
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: str, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: str, user_update: UserUpdate, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()