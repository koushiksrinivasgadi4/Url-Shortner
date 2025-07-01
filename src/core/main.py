import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core import events
from core.router import initialize_routes
from services.database import engine, get_session
from middlewares.response_schema import response_schema_middleware
from core.config import database_config, redis_config
from fastapi.middleware.cors import CORSMiddleware
from apps.shortener.apis import shortener_router,campaign_router


app = FastAPI()

app.add_event_handler("startup", events.startup_event_handler)
app.add_event_handler("shutdown", events.shutdown_event_handler)

app.include_router(shortener_router)
app.include_router(campaign_router)

def create_tables():
    SQLModel.metadata.create_all(engine)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )

print("DB CONFIG:")
print("  username:", database_config.username)
print("  password:", database_config.password)
print("  database:", database_config.database)
print("  host:", database_config.host)
print("  port:", database_config.port)
print("REDIS CONFIG:")
print("  host:", redis_config.host)
print("  port:", redis_config.port)
print("  database:", redis_config.database)
print("  max_connections:", redis_config.max_connections)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

response_schema_middleware(app)


@app.on_event("startup")
async def startup() -> None:
    await events.startup_event_handler()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await events.shutdown_event_handler()


@app.get("/ping")
def ping():
    return "pong!"


initialize_routes(app)
