from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import chat, documents, session
from app.db.session import engine
from app.db.base import Base
# Ensure models are imported so they are registered with Base
from app.db import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database directory exists
    import os
    db_path = settings.SQLITE_URL.replace("sqlite+aiosqlite:///", "")
    if db_path.startswith("./"):
        db_path = db_path[2:]
    
    # Handle the case where it might be a file path
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        print(f"[BACKEND] Creating database directory: {db_dir}", flush=True)
        os.makedirs(db_dir, exist_ok=True)
    
    print(f"[BACKEND] Database path: {db_path}", flush=True)
    print(f"[BACKEND] Current working directory: {os.getcwd()}", flush=True)

    # Create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Include routers (commented out until implemented)
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"])
app.include_router(session.router, prefix=f"{settings.API_V1_STR}/session", tags=["session"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

@app.get("/")
async def root():
    return {"message": "Welcome to Research RAG Assistant API"}
