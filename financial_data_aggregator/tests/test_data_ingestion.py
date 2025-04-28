import pytest
import asyncio
from unittest.mock import patch, MagicMock
from app.services.data_ingestion import DataIngestionService
import pandas as pd
from datetime import datetime, timedelta

@pytest.fixture
def mock_yfinance_ticker():
    """Fixture to mock the yfinance.Ticker class"""
    with patch('yfinance.Ticker') as mock_ticker:
        # Create a mock history DataFrame
        dates = pd.date_range(start=datetime.now() - timedelta(days=7), periods=7, freq='D')
        mock_history = pd.DataFrame(
            {
                'Open': [60000, 61000, 62000, 63000, 64000, 65000, 66000],
                'High': [61000, 62000, 63000, 64000, 65000, 66000, 67000],
                'Low': [59000, 60000, 61000, 62000, 63000, 64000, 65000],
                'Close': [61000, 62000, 63000, 64000, 65000, 66000, 67000],
                'Volume': [1000000] * 7
            },
            index=dates
        )
        
        # Set up the mock to return our DataFrame when history is called
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.history.return_value = mock_history
        mock_ticker.return_value = mock_ticker_instance
        
        yield mock_ticker

@pytest.mark.asyncio
async def test_fetch_asset_data(mock_yfinance_ticker):
    """Test that asset data is fetched and processed correctly"""
    service = DataIngestionService()
    service.assets = {"BTC-USD": MagicMock()}
    
    # Call the fetch method
    await service._fetch_asset_data("BTC-USD")
    
    # Verify that yfinance.Ticker was called
    mock_yfinance_ticker.assert_called_once_with("BTC-USD")

@pytest.mark.asyncio
async def test_ingest_data():
    """Test that data ingestion processes all assets"""
    service = DataIngestionService()
    service.assets = {
        "BTC-USD": MagicMock(symbol="BTC-USD"),
        "ETH-USD": MagicMock(symbol="ETH-USD"),
        "TSLA": MagicMock(symbol="TSLA")
    }
    
    with patch.object(service, '_fetch_asset_data') as mock_fetch:
        mock_fetch.return_value = None
        
        # Call ingest_data with a mock source
        updated = await service.ingest_data(source="mock_source")
        
        # Assert that assets were processed
        assert updated == ["BTC-USD", "ETH-USD", "TSLA"]

@pytest.mark.asyncio
async def test_openai_summary_generation():
    """Test OpenAI summary generation with mocked OpenAI client"""
    with patch('app.core.config.settings.USE_OPENAI', True), \
         patch('app.core.config.settings.OPENAI_API_KEY', 'test_key'), \
         patch('openai.ChatCompletion.create') as mock_create:
        mock_create.return_value = {"choices": [{"message": {"content": "Test summary"}}]}
        
        # Call the function being tested
        result = await generate_summary("Test input")
        
        # Assert the result
        assert result == "Test summary"

async def _fetch_asset_data(self, symbol):
    import yfinance as yf
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="7d")
    self.assets[symbol].historical_prices = data.to_dict()