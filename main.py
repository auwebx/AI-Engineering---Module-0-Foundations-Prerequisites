from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, Annotated
from database import create_db_and_tables, get_session
from models import Calculation
from sqlmodel import select, Session
from sqlalchemy import func
from datetime import datetime


app = FastAPI(
    title="AI Engineer Module 1 – FastAPI + PostgreSQL Edition",
    version="2.0.0"
)


class AddRequest(BaseModel):
    a: int
    b: int
    name: Optional[str] = None


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def home():
    return {
        "message": "Module 1 – Now with PostgreSQL database! 🚀",
        "docs": "/docs",
        "new_endpoint": "/api/history"
    }


@app.post("/api/calc/add")
async def calc_add(request: AddRequest, session: Annotated[Session, Depends(get_session)]):
    result = request.a + request.b

    calc = Calculation(a=request.a, b=request.b, result=result, name=request.name)
    session.add(calc)
    session.commit()
    session.refresh(calc)

    # Count total calculations
    history_count = session.exec(select(func.count()).select_from(Calculation)).one()

    greeting = f", {request.name}" if request.name else ""

    return {
        "result": result,
        "operation": f"{request.a} + {request.b}",
        "history_count": history_count,
        "message": f"Calculation saved forever{greeting}!",
        "id": calc.id,
        "timestamp": calc.timestamp.isoformat()
    }


# NEW ENDPOINT: Get full history
@app.get("/api/history")
def get_history(session: Annotated[Session, Depends(get_session)], limit: int = 50):
    calculations = session.exec(
        select(Calculation)
        .order_by(Calculation.timestamp.desc())
        .limit(limit)
    ).all()

    return calculations