from fastapi import FastAPI
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import os


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def create_table(conn):
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS counter (
            id SERIAL PRIMARY KEY,
            count INTEGER
        )
        """
    )


async def initialize_count(conn):
    count = await conn.fetchval("SELECT count FROM counter WHERE id=1")
    if count is None:
        await conn.execute("INSERT INTO counter (count) VALUES (0)")


async def get_connection():
    conn = await asyncpg.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, database=DB_NAME)
    return conn


async def on_startup():
    conn = await get_connection()
    await create_table(conn)
    await initialize_count(conn)
    await conn.close()


@app.on_event("startup")
async def startup():
    await on_startup()


@app.get("/get_count")
async def show_count(conn: asyncpg.Connection = Depends(get_connection)):
    count = await conn.fetchval("SELECT count FROM counter WHERE id=1")
    return {"count": count}


@app.post("/increase_count")
async def increase_count_by_one(conn: asyncpg.Connection = Depends(get_connection)):
    await conn.execute("UPDATE counter SET count = count + 1 WHERE id=1")
    return {"message": "Count increased by 1"}
