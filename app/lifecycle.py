import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.database import get_async_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.mongodb_client = get_async_client()
    app.database = app.mongodb_client.get_default_database()
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        logging.info("Connected to database cluster.")

    yield
    # Shutdown
    await app.mongodb_client.close()
    logging.info("MongoDB connection closed")