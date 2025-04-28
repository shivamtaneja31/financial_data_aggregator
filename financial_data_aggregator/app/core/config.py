from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Financial Data Aggregator"
    DEBUG: bool = True
    
    # API Settings
    API_PREFIX: str = "/api"
    
    # Asset settings
    TRACKED_ASSETS: List[str] = ["BTC-USD", "ETH-USD", "TSLA", "AAPL", "MSFT"]
    
    # Data refresh interval in seconds
    DATA_REFRESH_INTERVAL: int = 3600  # 1 hour
    
    # GenAI settings
    USE_OPENAI: bool = False  # Toggle to use OpenAI vs simple mock
    OPENAI_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings()