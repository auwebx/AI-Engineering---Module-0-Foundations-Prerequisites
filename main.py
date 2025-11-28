from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, Annotated
from database import create_db_and_tables, get_session
from models import Calculation
from sqlmodel import select, Session
from sqlalchemy import func
from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import joblib
import os
from ml.trainer import pipeline


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

class SpamRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Message to classify")

@app.post("/api/spam/detect")
async def detect_spam(request: SpamRequest):
    if not os.path.exists("ml/pipeline.pkl"):
        raise HTTPException(status_code=503, detail="Model is still training – try again in 10 seconds")

    prediction = pipeline.predict([request.text])[0]
    probability = pipeline.predict_proba([request.text])[0].max()

    label = "spam" if prediction == 1 else "ham"

    return {
        "label": label,
        "confidence": round(probability * 100, 2),
        "text": request.text,
        "model": "LogisticRegression + TF-IDF",
        "trained_on": "SMS Spam Collection (5,572 messages)",
        "accuracy_on_test": "~98.3%"  # from our run
    }