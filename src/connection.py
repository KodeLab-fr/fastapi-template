from fastapi import APIRouter, Depends
import os
print(os.getcwd())
# sqlalchemy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
# Internal imports
import sys
# from utils.users import UserBase
from src.utils.models import User
from src.utils.db import get_db
from pydantic import BaseModel


router = APIRouter()


class UserBase(BaseModel):
    username: str

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
