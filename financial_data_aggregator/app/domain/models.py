from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class Asset:
    """Represents a financial asset like a stock or cryptocurrency"""
    symbol: str
    name: str
    asset_type: str  # stock, crypto, etc.
    latest_price: float = 0.0
    change_percent_24h: float = 0.0
    average_price_7d: float = 0.0
    historical_prices: Optional[Dict[datetime, float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "symbol": self.symbol,
            "name": self.name,
            "asset_type": self.asset_type,
            "latest_price": self.latest_price,
            "change_percent_24h": self.change_percent_24h,
            "average_price_7d": self.average_price_7d
        }

@dataclass
class MarketSummary:
    """Summary of the current market state"""
    timestamp: datetime
    summary_text: str
    top_performers: List[str]
    worst_performers: List[str]
    market_trend: str  # bullish, bearish, neutral
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "summary": self.summary_text,
            "top_performers": self.top_performers,
            "worst_performers": self.worst_performers,
            "market_trend": self.market_trend
        }