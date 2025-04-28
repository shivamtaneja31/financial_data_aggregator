from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class AssetResponse(BaseModel):
    """API response model for asset data"""
    symbol: str
    name: str
    asset_type: str
    latest_price: float
    change_percent_24h: float
    average_price_7d: float

class AssetListResponse(BaseModel):
    """API response model for list of assets"""
    assets: List[AssetResponse]

class MetricsResponse(BaseModel):
    """API response model for asset metrics"""
    symbol: str
    latest_price: float
    change_percent_24h: float
    average_price_7d: float

class CompareResponse(BaseModel):
    """API response model for asset comparison"""
    asset1: AssetResponse
    asset2: AssetResponse
    price_difference: float
    performance_difference_24h: float

class SummaryResponse(BaseModel):
    """API response model for market summary"""
    summary: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    top_performers: List[str]
    worst_performers: List[str]
    market_trend: str

class IngestResponse(BaseModel):
    """API response model for data ingestion"""
    status: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    assets_updated: List[str]

class DataIngestionService:
    def __init__(self):
        pass

data_service = DataIngestionService()  # Ensure this is properly initialized