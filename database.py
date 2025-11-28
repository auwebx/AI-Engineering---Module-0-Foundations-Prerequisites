import os
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy import func

# Auto-switch: local = SQLite, Render = PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./calculations.db")

# Fix Render's URL format for psycopg2
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

engine = create_engine(DATABASE_URL, echo=False)  # echo=True if you want logs

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session