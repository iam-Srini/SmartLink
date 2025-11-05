from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from app.routers import router
from app.models.user import Base
from app.db.session import engine

# Initialize FastAPI app
app = FastAPI(title="SmartLink", version="1.0")

# Include all API routes
app.include_router(router)

# Initialize database tables
try:
    Base.metadata.create_all(engine)
except SQLAlchemyError as e:
    print(f"Database initialization failed: {e}")


@app.get("/")
def home() -> dict:
    """Root endpoint returning a welcome message."""
    return {"message": "Welcome to SmartLink API"}
