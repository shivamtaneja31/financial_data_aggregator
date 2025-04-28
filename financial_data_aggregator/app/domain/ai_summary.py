import logging
from typing import List, Optional
from datetime import datetime
from app.domain.models import Asset, MarketSummary
from app.domain.metrics import MetricsCalculator
from app.core.config import settings

logger = logging.getLogger(__name__)

class AISummaryGenerator:
    """Service for generating AI-powered market summaries"""
    
    def __init__(self):
        self.openai_client = None
        if settings.USE_OPENAI and settings.OPENAI_API_KEY:
            # Import only if needed
            import openai
            openai.api_key = settings.OPENAI_API_KEY
            self.openai_client = openai

    async def generate_summary(self, assets: List[Asset]) -> MarketSummary:
        """Generate a market summary based on asset data"""
        if settings.USE_OPENAI and self.openai_client:
            return await self._generate_openai_summary(assets)
        else:
            return self._generate_mock_summary(assets)
    
    async def _generate_openai_summary(self, assets: List[Asset]) -> MarketSummary:
        """Generate a summary using OpenAI"""
        # This would be a real implementation using OpenAI
        try:
            # Create a prompt with asset data
            prompt = self._create_summary_prompt(assets)
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial analyst providing brief market summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            
            summary_text = response.choices[0].message.content
            
            # Get other summary data
            top_performers = MetricsCalculator.get_top_performers(assets)
            worst_performers = MetricsCalculator.get_worst_performers(assets)
            market_trend = MetricsCalculator.determine_market_trend(assets)
            
            return MarketSummary(
                timestamp=datetime.now(),
                summary_text=summary_text,
                top_performers=[p[0] for p in top_performers],
                worst_performers=[p[0] for p in worst_performers],
                market_trend=market_trend
            )
            
        except Exception as e:
            logger.error(f"Error generating OpenAI summary: {str(e)}")
            # Fall back to mock summary
            return self._generate_mock_summary(assets)
    
    def _generate_mock_summary(self, assets: List[Asset]) -> MarketSummary:
        """Generate a mock summary based on asset data"""
        # Calculate summary data
        top_performers = MetricsCalculator.get_top_performers(assets)
        worst_performers = MetricsCalculator.get_worst_performers(assets)
        market_trend = MetricsCalculator.determine_market_trend(assets)
        
        # Generate summary text
        if market_trend == "bullish":
            trend_desc = "showing strong upward momentum"
        elif market_trend == "bearish":
            trend_desc = "experiencing a downturn"
        else:
            trend_desc = "relatively stable"
        
        # Find the asset with the most extreme movement
        most_volatile = max(assets, key=lambda a: abs(a.change_percent_24h))
        
        summary_text = (
            f"The market is currently {trend_desc}. "
            f"{top_performers[0][0]} leads gains with a {top_performers[0][1]:.2f}% increase over 24 hours, "
            f"while {worst_performers[0][0]} shows the largest decline at {worst_performers[0][1]:.2f}%. "
            f"{most_volatile.name} demonstrates the most volatility at {abs(most_volatile.change_percent_24h):.2f}% movement. "
            f"The 7-day average for Bitcoin stands at ${assets[0].average_price_7d:.2f}."
        )
        
        return MarketSummary(
            timestamp=datetime.now(),
            summary_text=summary_text,
            top_performers=[p[0] for p in top_performers],
            worst_performers=[p[0] for p in worst_performers],
            market_trend=market_trend
        )
    
    def _create_summary_prompt(self, assets: List[Asset]) -> str:
        """Create a prompt for the OpenAI API based on asset data"""
        prompt = "Please provide a brief market summary based on the following data:\n\n"
        
        for asset in assets:
            prompt += (
                f"{asset.name} ({asset.symbol}): "
                f"Price: ${asset.latest_price:.2f}, "
                f"24h Change: {asset.change_percent_24h:.2f}%, "
                f"7d Avg: ${asset.average_price_7d:.2f}\n"
            )
        
        prompt += "\nProvide a concise 2-3 sentence summary of the current market trends."
        return prompt

# Create singleton instance
summary_generator = AISummaryGenerator()