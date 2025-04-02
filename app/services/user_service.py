from sqlmodel import select
from app.models.user import User, UserRead
from app.core.db import async_session
from typing import List

async def fetch_all_users() -> List[UserRead]:
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        # return [user.dict() for user in users]
        # return [user.full_name for user in users if user.full_name]
        return [{"id": str(user.id), "full_name": user.full_name} for user in users]

