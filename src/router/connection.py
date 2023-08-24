# fastapi
from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# sqlalchemy
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

# internal imports
from utils.db import get_db
from utils.models import User
from utils.users import UserCreation
from utils.email_utils import check_email

# scrypting
import argon2
from argon2 import PasswordHasher
import jwt

# utils
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
# typing
from typing import Annotated


router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={200: {"description": "Welcome on users route"}},
                   )
security = HTTPBasic()
load_dotenv()


@router.post("/login")
async def read_current_user(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        db: AsyncSession = Depends(get_db),
        response: Response = Response()):
    results = await db.execute(
            select(User.password)
            .filter(or_(User.username == credentials.username,
                        User.email == credentials.username)))
    password = str(results.scalar())
    ph = PasswordHasher()
    try:
        if ph.verify(password, credentials.password):
            response.status_code = status.HTTP_202_ACCEPTED
            print(datetime.now().timestamp())
            try:
                exp = datetime.now(timezone.utc)+timedelta(hours=24)
                encoded = jwt.encode({"username": str(credentials.username),
                                      "exp": exp, },
                                     os.getenv("JWT_SECRET"),
                                     algorithm="HS256")
            except jwt.exceptions.InvalidKeyError as e:
                print(e)
                return {"code": 500,
                        "message": "Internal server error"}
            return {"code": "0",
                    "message": encoded}
            # print(datetime.fromtimestamp())

    except argon2.exceptions.VerifyMismatchError as e:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"code": 401,
                "message": e.args[0]}


@router.post("/user")
async def index(user: UserCreation,
                db: AsyncSession = Depends(get_db),
                response: Response = Response()):
    if check_email(user.email):
        ph = argon2.PasswordHasher(hash_len=64,
                                   parallelism=8,
                                   memory_cost=4096,
                                   time_cost=192)
        hash = ph.hash(user.password)
        db_user = User(username=user.username,
                       email=user.email,
                       password=hash)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return {"code": 0, "message": "User created successfully"}
    else:
        response.status_code = status.HTTP_409_CONFLICT
        return {"code": 409,
                "message": "Incorrect email format"}


@router.get("/test_token")
async def test_token(token: str):
    try:
        decode = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        if decode.get("exp") > datetime.now().timestamp():
            print(datetime.now())
            print(datetime.fromtimestamp(decode.get("exp")))
            return {"code": 0,
                    "message": "Token is valid"}
    except jwt.exceptions.DecodeError as e:
        return {"code": 401,
                "message": e.args[0]}
    except jwt.exceptions.ExpiredSignatureError as e:
        return {"code": 401,
                "message": e.args[0]}
