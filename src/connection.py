from fastapi import APIRouter, Depends
# sqlalchemy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
# Internal imports
from utils.users import UserBase
from utils.models import User
from utils.db import get_db


router = APIRouter()


@router.post("/user")
async def index(user: UserBase, db: AsyncSession = Depends(get_db)):
    db_user = User(username=user.username)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.get("/user")
async def get_users(db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(User))
    users = results.scalars().all()
    return {"users": users}
