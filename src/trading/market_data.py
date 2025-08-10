import yfinance as yf
import pandas as pd
from typing import Dict, Any

class MarketData:
    def __init__(self):
        self.cache = {}

    def get_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch market data for a given symbol
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            latest = data.iloc[-1]
            
            return {
                "symbol": symbol,
                "price": latest["Close"],
                "volume": latest["Volume"],
                "change": (latest["Close"] - latest["Open"]) / latest["Open"] * 100
            }
        except Exception as e:
            return {"error": str(e)}
