from fastapi import FastAPI

from app.lifecycle import lifespan
from app.logging import configure_logging, LogLevels
from app.middleware.app_middleware import add_middlewares
from app.routers import (
    auth_routes,
    html_to_rss_routes,
    feed_collection_view_routes,
    get_feed_route,
    rss_playground_routes
)

configure_logging(LogLevels.info)


app = FastAPI(lifespan=lifespan)

add_middlewares(app)

app.include_router(auth_routes.router)
app.include_router(html_to_rss_routes.router)
app.include_router(feed_collection_view_routes.router)
app.include_router(rss_playground_routes.router)
app.include_router(get_feed_route.router)

@app.get("/")
async def root():
    return {
        "message": "meltwater feeds revamped by Tyrone Slothrop",
        "last committed": "Saturday 19 July 21:11:00 +0530"
    }