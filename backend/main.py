"""
Main FastAPI application - AI Tutor Orchestrator.
This is the entry point for the orchestration service.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from api import router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("Starting AI Tutor Orchestrator...")
    logger.info(f"Environment: {settings.app_env}")
    logger.info(f"Gemini Model: {settings.gemini_model}")
    
    # Startup
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
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
            "detail": str(exc) if settings.debug else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
