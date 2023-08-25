from fastapi import APIRouter, Depends
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from utils.db import get_db
from utils.models import User, TempUser

router = APIRouter(prefix="/table",
                   tags=["table"],
                   responses={200: {"description": "Welcome on users route"}},
                   )


@router.get("/reset")
async def reset(db: AsyncSession = Depends(get_db)):
    await db.execute(sqlalchemy.delete(User).where(User.id > 0))
    await db.commit()
    await db.execute(sqlalchemy.delete(TempUser).where(TempUser.id > 0))
    await db.commit()
    return {"message": "Database reset"}
