# FastAPI
from fastapi import FastAPI
import uvicorn
import connection

app = FastAPI()
app.include_router(connection.router)


@app.get("/")
async def root() -> dict:
    return {"message": "Well connected to the API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080,  reload=True)
