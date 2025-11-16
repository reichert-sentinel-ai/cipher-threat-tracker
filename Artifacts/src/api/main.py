"""FastAPI main application"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional
import logging

from .routers import ioc, threats, actors, campaigns, detect, timeline, network, threat_timeline, ioc_search, mitre_attack, ir_playbooks

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Cipher Threat Intelligence API",
    description="Cyber threat detection, attribution, and incident response platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - allow Vercel deployments and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cipher-threat-tracker.vercel.app",
        "https://cipher-threat-tracker-*.vercel.app",  # Preview deployments
        "http://localhost:5173",  # Local frontend dev server
        "*"  # Allow all for now - restrict in production if needed
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ioc.router, prefix="/api/v1", tags=["IOC"])
app.include_router(threats.router, prefix="/api/v1", tags=["Threats"])
app.include_router(actors.router, prefix="/api/v1", tags=["Threat Actors"])
app.include_router(campaigns.router, prefix="/api/v1", tags=["Campaigns"])
app.include_router(detect.router, prefix="/api/v1", tags=["Detection"])
app.include_router(timeline.router, prefix="/api/v1", tags=["Timeline"])
app.include_router(network.router, prefix="/api/v1", tags=["Network"])
app.include_router(threat_timeline.router, prefix="/api/threat-timeline", tags=["Threat Timeline"])
app.include_router(ioc_search.router, tags=["IOC Search"])
app.include_router(mitre_attack.router, tags=["MITRE ATT&CK"])
app.include_router(ir_playbooks.router, tags=["Incident Response"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Cipher Threat Intelligence API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "cipher-threat-intelligence"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

