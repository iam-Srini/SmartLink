from fastapi import FastAPI
from app.routers import router
from app.models.user import Base
from app.db.session import engine
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(title = "SmartLink", version="1.0")


app.include_router(router)

try:
    Base.metadata.create_all(engine)
except SQLAlchemyError as e:
    print(f"Database Initialization failed {e}")

@app.get("/")
def home():
    return {
        "message": "Welcome to SmartLink API"
    }



