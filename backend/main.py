"""
Main FastAPI application - AI Tutor Orchestrator.
This is the entry point for the orchestration service.
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import config.settings  # Load .env
from api import router

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("Starting AI Tutor Orchestrator...")
    logger.info(f"Environment: {os.getenv('APP_ENV', 'development')}")
    logger.info(f"Gemini Model: {os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')}")
    
    # Startup - Initialize database
    try:
        from database import init_db, check_db_connection
        logger.info("Initializing database connection...")
        
        if await check_db_connection():
            logger.info("✅ Database connection successful!")
            await init_db()
            logger.info("✅ Database initialized!")
        else:
            logger.error("❌ Database connection failed!")
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Tutor Orchestrator...")


# Create FastAPI app
app = FastAPI(
    title="AI Tutor Orchestrator",
    description="Intelligent middleware for autonomous educational tool orchestration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api", tags=["orchestrator"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "AI Tutor Orchestrator",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG", "true").lower() == "true" else "An error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", "8000")),
        reload=os.getenv("DEBUG", "true").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "INFO").lower()
    )
