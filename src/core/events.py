# src/core/events.py
from sqlmodel import SQLModel
from services.database import engine, Base
from apps.shortener import models  # register models

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("✅ Database tables created successfully on startup!")


async def startup_event_handler():
    await init_db()


async def shutdown_event_handler():
    await engine.dispose()
    print("🔴 Application is shutting down.")
