from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    """
    Provide a database session for dependency injection.
    Ensures proper commit, rollback, and close handling.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
