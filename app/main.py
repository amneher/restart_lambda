from contextlib import asynccontextmanager
from fastapi import FastAPI
from mangum import Mangum
from app.routes import items_router, health_router
from app.database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    close_db()


app = FastAPI(
    title="AWS Lambda FastAPI",
    description="A FastAPI application designed for AWS Lambda with SQLite",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(items_router)

handler = Mangum(app, lifespan="off")
