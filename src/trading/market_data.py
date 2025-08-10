import yfinance as yf
import pandas as pd
from typing import Dict, Any
from datetime import datetime, timedelta
import pytz

class MarketData:
    def __init__(self):
        self.cache = {}
        self.cache_timeout = timedelta(minutes=1)
        
    def get_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch current market data for a given symbol
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
            
    def get_intraday_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch intraday data for day trading analysis
        Returns 1-minute interval data for the current trading day
        """
        try:
            now = datetime.now(pytz.UTC)
            
            # Check cache
            cache_key = f"{symbol}_{now.date()}"
            if cache_key in self.cache:
                cache_time, cache_data = self.cache[cache_key]
                if now - cache_time < self.cache_timeout:
                    return cache_data
            
            # Fetch new data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            
            # Convert to dict format
            result = {
                "Open": data["Open"].tolist(),
                "High": data["High"].tolist(),
                "Low": data["Low"].tolist(),
                "Close": data["Close"].tolist(),
                "Volume": data["Volume"].tolist(),
                "Datetime": data.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
            }
            
            # Update cache
            self.cache[cache_key] = (now, result)
            
            return result
            
        except Exception as e:
            return {"error": str(e)}
