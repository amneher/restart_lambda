from contextlib import asynccontextmanager

from fastapi import FastAPI
from mangum import Mangum

from app.database import close_db, init_db
from app.routes import health_router, items_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    close_db()


app = FastAPI(
    title="Restart Registry API",
    description="A FastAPI application designed for AWS Lambda with SQLite",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(items_router)

handler = Mangum(app, lifespan="off")
