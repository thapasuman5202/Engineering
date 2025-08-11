from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.routers import (
    stage0,
    stage1,
    stage2,
    stage3,
    stage4,
    stage5,
    stage6,
    stage7,
    stage8,
    stage9,
    stage10,
    stage11,
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
app.include_router(stage8.router)
app.include_router(stage9.router)
app.include_router(stage10.router)
app.include_router(stage11.router)


@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": f"{settings.app_name} API"}
