import logging
import asyncio
from typing import Dict, List, Optional, Tuple
from app.domain.models import Asset, MarketSummary
from app.services.data_ingestion import data_service
from app.domain.metrics import MetricsCalculator
from app.domain.ai_summary import summary_generator
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class DataProcessingService:
    """Service for processing and analyzing financial data"""
    
    def __init__(self):
        self.latest_summary: Optional[MarketSummary] = None
        self.last_summary_update: Optional[datetime] = None
        self.summary_cache_time = timedelta(minutes=15)  # Cache summary for 15 minutes
    
    async def initialize(self):
        """Initialize the service"""
        logger.info("Initializing data processing service")
        # Start background task for periodic summary updates
        asyncio.create_task(self._periodic_summary_update())
    
    async def _periodic_summary_update(self):
        """Background task for periodically updating the market summary"""
        while True:
            try:
                await asyncio.sleep(60 * 15)  # Update every 15 minutes
                logger.info("Running periodic summary update")
                await self.update_market_summary()
            except Exception as e:
                logger.error(f"Error in periodic summary update: {str(e)}")
    
    async def get_market_summary(self) -> MarketSummary:
        """Get the current market summary, updating if necessary"""
        # Check if we need to update the summary
        if (not self.latest_summary or 
            not self.last_summary_update or 
            datetime.now() - self.last_summary_update > self.summary_cache_time):
            await self.update_market_summary()
        
        return self.latest_summary
    
    async def update_market_summary(self) -> MarketSummary:
        """Update the market summary"""
        logger.info("Updating market summary")
        
        # Get all assets
        assets = data_service.get_all_assets()
        
        # Generate a new summary
        self.latest_summary = await summary_generator.generate_summary(assets)
        self.last_summary_update = datetime.now()
        
        logger.info(f"Market summary updated: {self.latest_summary.market_trend} trend")
        return self.latest_summary
    
    def get_asset_metrics(self, symbol: str) -> Dict:
        """Get metrics for a specific asset"""
        asset = data_service.get_asset(symbol)
        if not asset:
            raise ValueError(f"Asset with symbol {symbol} not found")
        
        return MetricsCalculator.calculate_asset_metrics(asset)
    
    def compare_assets(self, symbol1: str, symbol2: str) -> Dict:
        """Compare two assets"""
        asset1 = data_service.get_asset(symbol1)
        asset2 = data_service.get_asset(symbol2)
        
        if not asset1:
            raise ValueError(f"Asset with symbol {symbol1} not found")
        if not asset2:
            raise ValueError(f"Asset with symbol {symbol2} not found")
        
        return MetricsCalculator.compare_assets(asset1, asset2)
    
    def get_top_performers(self, count: int = 3) -> List[Tuple[str, float]]:
        """Get the top performing assets"""
        assets = data_service.get_all_assets()
        return MetricsCalculator.get_top_performers(assets, count)
    
    def get_worst_performers(self, count: int = 3) -> List[Tuple[str, float]]:
        """Get the worst performing assets"""
        assets = data_service.get_all_assets()
        return MetricsCalculator.get_worst_performers(assets, count)

# Create singleton instance
processing_service = DataProcessingService()