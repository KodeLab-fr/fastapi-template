# FastAPI
from fastapi import FastAPI
import sys
import os
from uvicorn import run
from src import connection


sys.path.append(os.getcwd())
app = FastAPI()
app.include_router(connection.router)


@app.get("/")
async def root() -> dict:
    return {"message": "Well connected to the API"}


if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8080,  reload=True)
