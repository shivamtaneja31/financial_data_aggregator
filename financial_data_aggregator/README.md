# Financial Data Aggregator & GenAI Insight Engine

A sophisticated financial data aggregator and insights engine that ingests financial data, processes it asynchronously, and exposes metrics and summaries through API endpoints, including a GenAI-powered textual summary generator.

## Features

- **Data Ingestion**: Fetches financial data for selected assets (stocks, cryptocurrencies) using yfinance
- **Asynchronous Processing**: Efficiently processes data using Python's asyncio
- **Metrics Calculation**: Computes financial metrics like price changes and averages
- **API Endpoints**: Exposes functionality through RESTful FastAPI endpoints
- **GenAI Summaries**: Generates market summaries using AI (mock or OpenAI)

## Project Structure

```
financial_data_aggregator/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints.py        # API route definitions
│   │   └── models.py           # Pydantic models for API
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration settings
│   │   └── logging.py          # Logging setup
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py           # Domain models
│   │   ├── metrics.py          # Metrics calculation logic
│   │   └── ai_summary.py       # GenAI summary generation
│   └── services/
│       ├── __init__.py
│       ├── data_ingestion.py   # Data fetching service
│       └── data_processing.py  # Data processing service
├── tests/
│   ├── __init__.py
│   ├── test_data_ingestion.py  # Unit test for data ingestion
│   ├── test_metrics.py         # Unit test for metrics calculation
│   ├── test_ai_summary.py      # Unit test for AI summaries
│   └── test_api.py             # Integration test for API
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10+
- Dependencies in requirements.txt

## Installation

1. Clone the repository
```
git clone git@github.com:shivamtaneja31/financial_data_aggregator.git
cd financial-data-aggregator
```

2. Create a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. (Optional) Create a .env file for configuration
```
APP_NAME="Financial Data Aggregator"
DEBUG=True
TRACKED_ASSETS=BTC-USD,ETH-USD,TSLA,AAPL,MSFT
DATA_REFRESH_INTERVAL=3600
USE_OPENAI=False
OPENAI_API_KEY=""  # Only if USE_OPENAI is True
```

## Usage

### Starting the Server

```
uvicorn app.main:app --reload
```

The server will be available at http://localhost:8000.

### API Endpoints

- **GET /assets**: List all tracked assets and their metadata
- **GET /metrics/{symbol}**: Return metrics for a specific asset
- **GET /compare?asset1=X&asset2=Y**: Compare two assets on performance metrics
- **GET /summary**: Return a GenAI-generated summary of current trends
- **POST /ingest**: Trigger manual ingestion/update of market data

### Interactive API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running Tests

Run all tests:
```
pytest
```

Run specific test files:
```
pytest tests/test_metrics.py
```

Run with coverage:
```
pytest --cov=app
```

## Architecture

The application follows clean architecture principles with the following layers:

1. **API Layer**: FastAPI endpoints and Pydantic models
2. **Service Layer**: Business logic and processing services
3. **Domain Layer**: Core models and metrics calculation
4. **Data Layer**: Data ingestion and storage

The application uses asyncio for efficient asynchronous processing, allowing it to handle multiple requests concurrently while performing background tasks like data ingestion.

## GenAI Summary Generation

The application can generate market summaries in two ways:

1. **Mock Summary**: Default implementation that analyzes asset data and generates a summary
2. **OpenAI Summary**: Optional integration with OpenAI's GPT models for more sophisticated summaries

To enable OpenAI, set the following environment variables:
```
USE_OPENAI=True
OPENAI_API_KEY=""
```

## License

[MIT License](LICENSE)