import pytest
from unittest.mock import patch, MagicMock
from app.domain.ai_summary import AISummaryGenerator
from app.domain.models import Asset, MarketSummary

@pytest.fixture
def sample_assets():
    """Fixture providing sample assets for testing"""
    return [
        Asset(
            symbol="BTC-USD",
            name="Bitcoin",
            asset_type="crypto",
            latest_price=65000.0,
            change_percent_24h=3.2,
            average_price_7d=63215.0
        ),
        Asset(
            symbol="ETH-USD",
            name="Ethereum",
            asset_type="crypto",
            latest_price=3500.0,
            change_percent_24h=-1.5,
            average_price_7d=3600.0
        ),
        Asset(
            symbol="TSLA",
            name="Tesla Inc.",
            asset_type="stock",
            latest_price=750.0,
            change_percent_24h=1.8,
            average_price_7d=740.0
        )
    ]

@pytest.mark.asyncio
async def test_generate_mock_summary(sample_assets):
    """Test that mock summary generation works correctly"""
    # Create summary generator
    generator = AISummaryGenerator()
    
    # Generate summary
    summary = await generator.generate_summary(sample_assets)
    
    # Verify it's a MarketSummary object
    assert isinstance(summary, MarketSummary)
    
    # Verify the contents
    assert "BTC-USD" in summary.top_performers  # BTC has highest change
    assert "ETH-USD" in summary.worst_performers  # ETH has lowest change
    assert summary.market_trend == "bullish"  # Average is positive
    
    # Check that summary text contains relevant info
    assert "BTC-USD" in summary.summary_text
    assert "bullish" in summary.summary_text.lower() or "upward" in summary.summary_text.lower()

@pytest.mark.asyncio
async def test_openai_summary_generation():
    """Test OpenAI summary generation with mocked OpenAI client"""
    # Mock the OpenAI client
    with patch('app.core.config.settings.USE_OPENAI', True), \
         patch('app.core.config.settings.OPENAI_API_KEY', 'test_key'), \
         patch('openai.chat.completions.create') as mock_create:
        
        # Set up mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is a test AI summary of the market."
        mock_create.return_value = mock_response
        
        # Create test assets
        assets = [
            Asset(
                symbol="BTC-USD",
                name="Bitcoin",
                asset_type="crypto",
                latest_price=65000.0,
                change_percent_24h=3.2,
                average_price_7d=63215.0
            )
        ]
        
        # Initialize generator and manually set OpenAI client
        generator = AISummaryGenerator()
        generator.openai_client = MagicMock()
        generator.openai_client.chat.completions.create = mock_create
        
        # Generate summary
        summary = await generator._generate_openai_summary(assets)
        
        # Verify the summary
        assert isinstance(summary, MarketSummary)
        assert summary.summary_text == "This is a test AI summary of the market."
        assert "BTC-USD" in summary.top_performers