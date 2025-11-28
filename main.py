from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from utils.math_utils import Calculator

# Global calculator instance (in real apps → database/redis)
calc = Calculator("FastAPI Global Calculator")

app = FastAPI(title="AI Engineer Module 0 – FastAPI Edition", version="1.0.0")


# Pydantic model for request validation (this is the modern way)
class AddRequest(BaseModel):
    a: int
    b: int
    name: Optional[str] = None  # optional greeting name


@app.get("/")
async def home():
    return {
        "message": "Welcome to AI Engineer Module 0 – FastAPI Edition!",
        "docs": "/docs",  # ← automatic interactive docs
        "redoc": "/redoc",
        "status": "running perfectly 🚀"
    }


@app.get("/api/hello")
async def hello(name: Optional[str] = "World"):
    return {"message": f"Hello, {name}! Welcome to FastAPI in 2025"}


@app.post("/api/calc/add")
async def calc_add(request: AddRequest):
    result = calc.add_and_record(request.a, request.b)

    greeting = f", {request.name}" if request.name else ""

    return {
        "result": result,
        "operation": f"{request.a} + {request.b}",
        "history_count": len(calc.history),
        "message": f"Calculation successful{greeting}!"
    }


# Health check endpoint (standard in production)
@app.get("/health")
async def health():
    return {"status": "healthy"}