import pytest
from app.domain.models import Asset
from app.domain.metrics import MetricsCalculator

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

def test_calculate_asset_metrics(sample_assets):
    """Test that asset metrics are calculated correctly"""
    asset = sample_assets[0]
    metrics = MetricsCalculator.calculate_asset_metrics(asset)
    
    assert metrics["symbol"] == "BTC-USD"
    assert metrics["latest_price"] == 65000.0
    assert metrics["change_percent_24h"] == 3.2
    assert metrics["average_price_7d"] == 63215.0

def test_compare_assets(sample_assets):
    """Test asset comparison functionality"""
    asset1 = sample_assets[0]  # BTC
    asset2 = sample_assets[1]  # ETH
    
    comparison = MetricsCalculator.compare_assets(asset1, asset2)
    
    assert comparison["price_difference"] == 65000.0 - 3500.0
    assert comparison["performance_difference_24h"] == 3.2 - (-1.5)
    assert comparison["asset1"]["symbol"] == "BTC-USD"
    assert comparison["asset2"]["symbol"] == "ETH-USD"

def test_get_top_performers(sample_assets):
    """Test identification of top performing assets"""
    top = MetricsCalculator.get_top_performers(sample_assets, count=2)
    
    # BTC has highest change (3.2%), followed by TSLA (1.8%)
    assert top[0][0] == "BTC-USD"
    assert top[1][0] == "TSLA"

def test_determine_market_trend(sample_assets):
    """Test market trend determination"""
    # Average change: (3.2 + (-1.5) + 1.8) / 3 = 1.17 (bullish)
    trend = MetricsCalculator.determine_market_trend(sample_assets)
    assert trend == "bullish"
    
    # Modify to get a bearish trend
    bearish_assets = sample_assets.copy()
    for asset in bearish_assets:
        asset.change_percent_24h = -2.0
    
    trend = MetricsCalculator.determine_market_trend(bearish_assets)
    assert trend == "bearish"