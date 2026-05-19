"""
Main FastAPI application for Conversation Memory Module.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import init_db
from routes import router

# Initialize FastAPI app
app = FastAPI(
    title="Conversation Memory Module",
    description="A FastAPI-based service for storing and retrieving conversation context for interview sessions",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get(
    "/health",
    summary="Health check",
    tags=["health"]
)
def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {
        "status": "healthy",
        "service": "Conversation Memory Module"
    }


# Root endpoint
@app.get(
    "/",
    summary="API root",
    tags=["root"]
)
def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Conversation Memory Module API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Include routes
app.include_router(router)


# Startup event
@app.on_event("startup")
def startup_event():
    """
    Initialize database on application startup.
    """
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")


# Exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Handle general exceptions.
    """
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
