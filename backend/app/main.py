from fastapi import FastAPI
from app.core.config import settings
from app.routers import (
    stage0,
    stage1,
    stage2,
    stage3,
    stage4,
    stage5,
    stage6,
    stage7,
)

app = FastAPI(title=settings.app_name)

app.include_router(stage0.router)
app.include_router(stage1.router)
app.include_router(stage2.router)
app.include_router(stage3.router)
app.include_router(stage4.router)
app.include_router(stage5.router)
app.include_router(stage6.router)
app.include_router(stage7.router)


@app.get("/")
async def root():
    return {"message": "God Mode Ultra Flow API"}
