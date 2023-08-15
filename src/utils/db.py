from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import os


load_dotenv()


class databse:
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')
    HOST = os.getenv('IP')
    PORT = int(os.getenv('PORT') or 0)
    DATABASE = os.getenv('DATABASE')


# SQLALCHEMY
SQLALCHEMY_DATABASE_URL = URL.create(
    'postgresql+asyncpg',
    username=databse.USERNAME,
    password=databse.PASSWORD,
    host=databse.HOST,
    port=databse.PORT,
    database=databse.DATABASE
)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
