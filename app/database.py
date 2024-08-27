# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os 

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()