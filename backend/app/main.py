from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import router
from app.database import engine
from app.models import Base
from app.seed import seed_if_empty


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    if settings.demo_seed:
        seed_if_empty()
    yield


app = FastAPI(
    title="Veridian Corp IT Internal Service Agent",
    description="Production-grade IT Support AI Agent for AIONOS Assignment 2",
    version="2.0.0",
    lifespan=lifespan,
)

cors_list = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]

if "*" in cors_list or settings.cors_origins.strip() == "*":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_list,
        allow_origin_regex=r"https://.*\.vercel\.app|https://.*\.onrender\.com|http://localhost(:\d+)?|http://127\.0\.0\.1(:\d+)?",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(router)
