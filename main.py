# ============================================================================
# IMPORTS SECTION
# ============================================================================

# FastAPI: Modern Python web framework for building APIs
# - FastAPI: Main application class for creating the API server
# - HTTPException: Used to raise HTTP errors with status codes (not used here but commonly imported)
from fastapi import FastAPI, HTTPException

# Pydantic: Data validation library using Python type hints
# - BaseModel: Base class for creating data models with automatic validation
from pydantic import BaseModel

# Typing: Python's type hinting module
# - Optional: Indicates a value can be of specified type or None (e.g., Optional[str] = str | None)
from typing import Optional

# Custom utility module containing calculator logic
# - Calculator: Custom class that performs math operations and tracks history
from utils.math_utils import Calculator

# ============================================================================
# GLOBAL INSTANCES
# ============================================================================

# Create a global Calculator instance that persists across all API requests
# In production applications, you would typically use:
# - A database (PostgreSQL, MongoDB, etc.) for persistent storage
# - Redis or Memcached for distributed caching across multiple server instances
# - This ensures data survives server restarts and works in multi-server deployments
calc = Calculator("FastAPI Global Calculator")

# Initialize the FastAPI application instance
# - title: Appears in auto-generated API documentation (/docs)
# - version: API version number for documentation and versioning purposes
app = FastAPI(title="AI Engineer Module 0 – FastAPI Edition", version="1.0.0")


# ============================================================================
# PYDANTIC DATA MODELS (Request/Response Schemas)
# ============================================================================

# Define the shape of incoming JSON data for the /api/calc/add endpoint
# Pydantic automatically:
# 1. Validates incoming JSON matches this structure
# 2. Converts data types (e.g., "5" string → 5 integer)
# 3. Returns detailed error messages if validation fails
# 4. Generates OpenAPI schema for automatic documentation
class AddRequest(BaseModel):
    # Required field: first number to add (must be an integer)
    a: int

    # Required field: second number to add (must be an integer)
    b: int

    # Optional field: user's name for personalized greeting
    # Default value is None if not provided in the request
    # Optional[str] means this can be a string or None
    name: Optional[str] = None


# ============================================================================
# API ROUTE HANDLERS (Endpoints)
# ============================================================================

# Root endpoint: GET request to "/"
# - @app.get(): Decorator that registers this function as a GET endpoint
# - async def: Makes this an asynchronous function (can handle concurrent requests efficiently)
# - Returns: JSON response automatically (FastAPI converts Python dict → JSON)
@app.get("/")
async def home():
    """
    Home/landing page endpoint that provides API information and navigation links.
    Accessible at: http://localhost:8000/
    """
    return {
        "message": "Welcome to AI Engineer Module 0 – FastAPI Edition!",
        # FastAPI automatically generates interactive API docs using Swagger UI
        "docs": "/docs",
        # Alternative documentation using ReDoc (different UI style)
        "redoc": "/redoc",
        "status": "running perfectly 🚀"
    }


# Simple greeting endpoint: GET request to "/api/hello"
# Query parameter example: /api/hello?name=Alice
# - name: Query parameter extracted from URL
# - Optional[str]: Can be omitted (defaults to "World")
# - = "World": Default value when name parameter is not provided
@app.get("/api/hello")
async def hello(name: Optional[str] = "World"):
    """
    Simple greeting endpoint demonstrating query parameters.
    Examples:
    - /api/hello → "Hello, World!"
    - /api/hello?name=Alice → "Hello, Alice!"
    """
    # f-string: Python formatted string literal for easy string interpolation
    return {"message": f"Hello, {name}! Welcome to FastAPI in 2025"}


# Calculator addition endpoint: POST request to "/api/calc/add"
# - @app.post(): Decorator for POST requests (typically used for data submission)
# - request: AddRequest: Pydantic automatically:
#   1. Parses JSON body
#   2. Validates data matches AddRequest model
#   3. Returns 422 error if validation fails
#   4. Converts validated data into AddRequest object
@app.post("/api/calc/add")
async def calc_add(request: AddRequest):
    """
    Performs addition of two numbers and records the operation in history.

    Request body example:
    {
        "a": 5,
        "b": 3,
        "name": "Alice"  // optional
    }

    Response example:
    {
        "result": 8,
        "operation": "5 + 3",
        "history_count": 1,
        "message": "Calculation successful, Alice!"
    }
    """
    # Call the calculator's add_and_record method
    # - Performs addition: a + b
    # - Stores operation in calculator's history list
    # - Returns the calculated result
    result = calc.add_and_record(request.a, request.b)

    # Conditional greeting: Create personalized message if name was provided
    # - Ternary expression: value_if_true if condition else value_if_false
    # - If request.name exists: ", Alice" (with comma and space prefix)
    # - If request.name is None: "" (empty string)
    greeting = f", {request.name}" if request.name else ""

    # Return response as dictionary (FastAPI converts to JSON automatically)
    return {
        # The calculated sum of a + b
        "result": result,

        # Human-readable string showing the operation performed
        "operation": f"{request.a} + {request.b}",

        # Number of operations stored in calculator's history
        # len(calc.history): Gets length of the history list
        "history_count": len(calc.history),

        # Success message with optional personalization
        # Examples: "Calculation successful!" or "Calculation successful, Alice!"
        "message": f"Calculation successful{greeting}!"
    }


# Health check endpoint: GET request to "/health"
# - Standard practice in production deployments
# - Used by load balancers, monitoring systems (Kubernetes, AWS ELB, etc.)
# - Helps determine if the service is running and ready to accept requests
# - Typically checked every few seconds by orchestration systems
@app.get("/health")
async def health():
    """
    Health check endpoint for monitoring and load balancing systems.
    Returns 200 OK status when service is operational.

    Common uses:
    - Kubernetes liveness/readiness probes
    - AWS Elastic Load Balancer health checks
    - Monitoring systems (Datadog, New Relic, etc.)
    """
    return {"status": "healthy"}

# ============================================================================
# HOW TO RUN THIS APPLICATION
# ============================================================================
# 
# 1. Install dependencies:
#    pip install fastapi uvicorn
#
# 2. Run the development server:
#    uvicorn main:app --reload
#    
#    Explanation:
#    - main: Python filename (main.py)
#    - app: FastAPI instance variable name
#    - --reload: Auto-restart server when code changes (dev only)
#
# 3. Access the application:
#    - API: http://localhost:8000
#    - Interactive docs: http://localhost:8000/docs
#    - Alternative docs: http://localhost:8000/redoc
#
# ============================================================================