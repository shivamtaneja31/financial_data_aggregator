from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
import logging
from app.api.models import (
    AssetResponse, AssetListResponse, MetricsResponse, 
    CompareResponse, SummaryResponse, IngestResponse
)
from app.services.data_ingestion import data_service
from app.domain.metrics import MetricsCalculator
from app.domain.ai_summary import summary_generator

# Create logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.get("/assets", response_model=AssetListResponse)
async def get_assets():
    """List all tracked assets and their metadata"""
    assets = data_service.get_all_assets()
    return {
        "assets": [AssetResponse(**asset.to_dict()) for asset in assets]
    }

@router.get("/metrics/{symbol}", response_model=MetricsResponse)
async def get_metrics(symbol: str):
    """Return metrics for a specific asset"""
    asset = data_service.get_asset(symbol)
    if not asset:
        raise HTTPException(status_code=404, detail=f"Asset with symbol {symbol} not found")
    
    metrics = MetricsCalculator.calculate_asset_metrics(asset)
    return MetricsResponse(**metrics)

@router.get("/compare", response_model=CompareResponse)
async def compare_assets(asset1: str = Query(...), asset2: str = Query(...)):
    """Compare two assets on performance metrics"""
    asset1_data = data_service.get_asset(asset1)
    asset2_data = data_service.get_asset(asset2)
    
    if not asset1_data:
        raise HTTPException(status_code=404, detail=f"Asset with symbol {asset1} not found")
    if not asset2_data:
        raise HTTPException(status_code=404, detail=f"Asset with symbol {asset2} not found")
    
    comparison = MetricsCalculator.compare_assets(asset1_data, asset2_data)
    return CompareResponse(**comparison)

@router.get("/summary", response_model=SummaryResponse)
async def get_summary():
    """Return a GenAI-generated summary of current trends"""
    assets = data_service.get_all_assets()
    summary = await summary_generator.generate_summary(assets)
    
    return SummaryResponse(
        summary=summary.summary_text,
        timestamp=summary.timestamp.isoformat(),
        top_performers=summary.top_performers,
        worst_performers=summary.worst_performers,
        market_trend=summary.market_trend
    )

@router.post("/ingest", response_model=IngestResponse)
async def trigger_ingestion():
    """Trigger manual ingestion/update of market data"""
    updated_assets = await data_service.ingest_data()
    
    return IngestResponse(
        status="success",
        assets_updated=updated_assets
    )

# Register startup event handler
@router.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    await data_service.initialize()