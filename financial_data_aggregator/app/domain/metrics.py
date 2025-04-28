from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from app.domain.models import Asset, MarketSummary
import logging

logger = logging.getLogger(__name__)

class MetricsCalculator:
    """Service for calculating financial metrics from asset data"""
    
    @staticmethod
    def calculate_asset_metrics(asset: Asset) -> Dict:
        """Calculate and return all metrics for a given asset"""
        return {
            "symbol": asset.symbol,
            "latest_price": asset.latest_price,
            "change_percent_24h": asset.change_percent_24h,
            "average_price_7d": asset.average_price_7d
        }
    
    @staticmethod
    def compare_assets(asset1: Asset, asset2: Asset) -> Dict:
        """Compare two assets and return comparison metrics"""
        price_difference = asset1.latest_price - asset2.latest_price
        perf_difference = asset1.change_percent_24h - asset2.change_percent_24h
        
        return {
            "asset1": asset1.to_dict(),
            "asset2": asset2.to_dict(),
            "price_difference": price_difference,
            "performance_difference_24h": perf_difference
        }
    
    @staticmethod
    def get_top_performers(assets: List[Asset], count: int = 3) -> List[Tuple[str, float]]:
        """Get the top performing assets based on 24h change"""
        sorted_assets = sorted(assets, key=lambda a: a.change_percent_24h, reverse=True)
        return [(a.symbol, a.change_percent_24h) for a in sorted_assets[:count]]
    
    @staticmethod
    def get_worst_performers(assets: List[Asset], count: int = 3) -> List[Tuple[str, float]]:
        """Get the worst performing assets based on 24h change"""
        sorted_assets = sorted(assets, key=lambda a: a.change_percent_24h)
        return [(a.symbol, a.change_percent_24h) for a in sorted_assets[:count]]
    
    @staticmethod
    def determine_market_trend(assets: List[Asset]) -> str:
        """Determine overall market trend based on asset performance"""
        avg_change = sum(a.change_percent_24h for a in assets) / len(assets)
        
        if avg_change > 1.0:
            return "bullish"
        elif avg_change < -1.0:
            return "bearish"
        else:
            return "neutral"