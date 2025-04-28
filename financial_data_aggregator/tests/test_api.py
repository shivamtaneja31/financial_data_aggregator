import pytest
from fastapi.testclient import TestClient
from app.main import app
import json
from unittest.mock import patch, MagicMock

client = TestClient(app)

@pytest.mark.integration
def test_api_get_assets():
    """Integration test: GET /assets endpoint"""
    # Mock the data service to return predefined assets
    with patch('app.services.data_ingestion.data_service.get_all_assets') as mock_get_all_assets:
        # Create mock assets
        mock_assets = [
            MagicMock(
                symbol="BTC-USD",
                name="Bitcoin",
                asset_type="crypto",
                latest_price=65000.0,
                change_percent_24h=3.2,
                average_price_7d=63215.0,
                to_dict=lambda: {
                    "symbol": "BTC-USD",
                    "name": "Bitcoin",
                    "asset_type": "crypto",
                    "latest_price": 65000.0,
                    "change_percent_24h": 3.2,
                    "average_price_7d": 63215.0
                }
            )
        ]
        
        mock_get_all_assets.return_value = mock_assets
        
        # Make request to API
        response = client.get("/assets")
        
        # Assert response
        assert response.status_code == 200
        data = response.json()
        assert "assets" in data
        assert len(data["assets"]) == 1
        assert data["assets"][0]["symbol"] == "BTC-USD"
        assert data["assets"][0]["latest_price"] == 65000.0

@pytest.mark.integration
def test_api_get_metrics():
    """Integration test: GET /metrics/{symbol} endpoint"""
    # Mock the data service to return a predefined asset
    with patch('app.services.data_ingestion.data_service.get_asset') as mock_get_asset:
        # Create mock asset
        mock_asset = MagicMock(
            symbol="BTC-USD",
            name="Bitcoin",
            asset_type="crypto",
            latest_price=65000.0,
            change_percent_24h=3.2,
            average_price_7d=63215.0
        )
        
        mock_get_asset.return_value = mock_asset
        
        # Make request to API
        response = client.get("/metrics/BTC-USD")
        
        # Assert response
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "BTC-USD"
        assert data["latest_price"] == 65000.0
        assert data["change_percent_24h"] == 3.2
        assert data["average_price_7d"] == 63215.0

@pytest.mark.integration
def test_api_get_summary():
    """Integration test: GET /summary endpoint"""
    # Mock the necessary services
    with patch('app.services.data_ingestion.data_service.get_all_assets') as mock_get_all_assets, \
         patch('app.domain.ai_summary.summary_generator.generate_summary') as mock_generate_summary:
        
        # Create mock assets
        mock_assets = [MagicMock()]
        mock_get_all_assets.return_value = mock_assets
        
        # Create mock summary
        from datetime import datetime
        from app.domain.models import MarketSummary
        
        mock_summary = MarketSummary(
            timestamp=datetime.now(),
            summary_text="Market is doing well today.",
            top_performers=["BTC-USD", "TSLA"],
            worst_performers=["ETH-USD"],
            market_trend="bullish"
        )
        
        mock_generate_summary.return_value = mock_summary
        
        # Make request to API
        response = client.get("/summary")
        
        # Assert response
        assert response.status_code == 200
        data = response.json()
        assert data["summary"] == "Market is doing well today."
        assert data["top_performers"] == ["BTC-USD", "TSLA"]
        assert data["market_trend"] == "bullish"