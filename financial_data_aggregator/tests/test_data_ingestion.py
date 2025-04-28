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
    # Create a service instance
    service = DataIngestionService()
    
    # Add a test asset
    service.assets = {
        "BTC-USD": MagicMock(
            symbol="BTC-USD",
            name="Bitcoin",
            asset_type="crypto",
            latest_price=0,
            change_percent_24h=0,
            average_price_7d=0,
            historical_prices={}
        )
    }
    
    # Call the fetch method
    await service._fetch_asset_data("BTC-USD")
    
    # Verify that yfinance.Ticker was called
    mock_yfinance_ticker.assert_called_once_with("BTC-USD")
    
    # Verify that the asset was updated
    asset = service.assets["BTC-USD"]
    assert asset.latest_price == 67000  # Should be the last close price
    assert asset.change_percent_24h != 0  # Should be calculated
    assert asset.average_price_7d == 64000  # Should be the average of all close prices
    assert len(asset.historical_prices) == 7  # Should have 7 days of history

@pytest.mark.asyncio
async def test_ingest_data():
    """Test that data ingestion processes all assets"""
    # Create a service instance with mock assets
    service = DataIngestionService()
    service.assets = {
        "BTC-USD": MagicMock(symbol="BTC-USD"),
        "ETH-USD": MagicMock(symbol="ETH-USD"),
        "TSLA": MagicMock(symbol="TSLA")
    }
    
    # Mock the _fetch_asset_data method
    with patch.object(service, '_fetch_asset_data') as mock_fetch:
        # Make fetch return immediately for testing
        mock_fetch.return_value = None
        
        # Call ingest_data
        updated = await service.ingest_data()
        
        # Verify that fetch was called for each asset
        assert mock_fetch.call_count == 3
        assert len(updated) == 3
        assert "BTC-USD" in updated
        assert "ETH-USD" in updated
        assert "TSLA" in updated