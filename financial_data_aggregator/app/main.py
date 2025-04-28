import logging
from fastapi import FastAPI, Depends
from app.api.endpoints import router
from app.core.config import settings
from app.core.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Financial Data Aggregator & GenAI Insight Engine",
    description="A system to ingest financial data and provide insights via API",
    version="1.0.0",
)

# Include API routes
app.include_router(router)

@app.on_event("startup")
async def startup():
    logger.info("Starting Financial Data Aggregator & GenAI Insight Engine")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)