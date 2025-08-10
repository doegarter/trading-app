from fastapi import FastAPI, HTTPException
from .trading.market_data import MarketData
from .trading.strategy import TradingStrategy
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Day Trading Signals API")
market_data = MarketData()
strategy = TradingStrategy()

@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "Day Trading Signals API",
        "version": "2.0"
    }

@app.get("/market-data/{symbol}")
async def get_market_data(symbol: str):
    """
    Get current market data for a symbol
    """
    data = market_data.get_data(symbol)
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"])
    return data

@app.get("/analyze/{symbol}")
async def analyze_symbol(symbol: str):
    """
    Generate day trading signals for a symbol
    """
    try:
        signals = strategy.analyze(symbol, market_data)
        if "error" in signals:
            raise HTTPException(status_code=400, detail=signals["error"])
            
        logger.info(f"Generated signals for {symbol}: {signals['signal']['action']}")
        return signals
        
    except Exception as e:
        logger.error(f"Error analyzing {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
