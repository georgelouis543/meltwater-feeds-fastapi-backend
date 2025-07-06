from fastapi import FastAPI

from app.lifecycle import lifespan
from app.logging import configure_logging, LogLevels
from app.middleware.app_middleware import add_middlewares
from app.routers import (
    auth_routes,
    html_to_rss_routes,
    feed_collection_view_routes
)

configure_logging(LogLevels.info)


app = FastAPI(lifespan=lifespan)

add_middlewares(app)

app.include_router(auth_routes.router)
app.include_router(html_to_rss_routes.router)
app.include_router(feed_collection_view_routes.router)

@app.get("/")
async def root():
    return {
        "message": "meltwater feeds revamped by Tyrone Slothrop",
        "last committed": "Mon 23 Jun 20:29:00"
    }