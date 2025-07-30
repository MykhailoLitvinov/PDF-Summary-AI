import logging

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes.documents import router as documents_router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="PDF Summary AI", description="API for processing PDF documents and generating AI summaries", version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(documents_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "PDF Summary AI Backend", "version": "1.0.0", "status": "running"}


# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error: {str(exc)}")
    return JSONResponse(
        status_code=500, content={"success": False, "message": "Internal server error", "detail": str(exc)}
    )
