from fastapi import FastAPI, HTTPException
from .trading.market_data import MarketData
from .trading.strategy import TradingStrategy
from typing import List, Dict, Any
import logging
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define supported stocks
class StockSymbol(str, Enum):
    MICROSOFT = "MSFT"
    GOOGLE = "GOOGL"
    APPLE = "AAPL"
    CLOUDFLARE = "NET"
    DWAVE = "QBTS"
    META = "META"

SUPPORTED_STOCKS = {
    "microsoft": "MSFT",
    "google": "GOOGL",
    "apple": "AAPL",
    "cloudflare": "NET",
    "d-wave": "QBTS",
    "meta": "META"
}

app = FastAPI(title="Tech Stocks Trading Signals API")
market_data = MarketData()
strategy = TradingStrategy()

@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "Tech Stocks Trading Signals API",
        "version": "2.1",
        "supported_stocks": SUPPORTED_STOCKS
    }

@app.get("/market-data/{symbol}")
async def get_market_data(symbol: StockSymbol):
    """
    Get current market data for a supported tech stock
    """
    try:
        data = market_data.get_data(symbol)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        return data
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid symbol. Supported symbols: {list(SUPPORTED_STOCKS.values())}")

@app.get("/analyze/{symbol}")
async def analyze_symbol(symbol: StockSymbol):
    """
    Generate day trading signals for a supported tech stock
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

@app.get("/analyze-all")
async def analyze_all_stocks() -> Dict[str, Any]:
    """
    Generate trading signals for all supported tech stocks
    """
    try:
        results = {}
        for company, symbol in SUPPORTED_STOCKS.items():
            signals = strategy.analyze(symbol, market_data)
            if "error" not in signals:
                results[company] = {
                    "symbol": symbol,
                    "signal": signals["signal"],
                    "price": signals["price"],
                    "indicators": signals["indicators"]
                }
            else:
                results[company] = {"error": signals["error"]}
                
        return {
            "timestamp": market_data.get_current_market_time(),
            "signals": results
        }
        
    except Exception as e:
        logger.error(f"Error in batch analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
