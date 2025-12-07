import asyncpg
import os

DATABASE_URL = os.getenv("NEON_DATABASE_URL")

async def get_db():
    return await asyncpg.connect(DATABASE_URL)


async def save_query(user_query: str, answer: str):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        INSERT INTO query_logs (query, answer)
        VALUES ($1, $2)
    """, user_query, answer)
    await conn.close()
