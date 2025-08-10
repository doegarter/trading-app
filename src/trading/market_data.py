import yfinance as yf
import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import pytz
from zoneinfo import ZoneInfo

class MarketData:
    def __init__(self):
        self.cache = {}
        self.cache_timeout = timedelta(minutes=1)
        self.market_timezone = ZoneInfo("America/New_York")
        
    def get_current_market_time(self) -> str:
        """
        Get current market time in US Eastern Time
        """
        return datetime.now(self.market_timezone).isoformat()
        
    def is_market_open(self) -> bool:
        """
        Check if the US market is currently open
        """
        now = datetime.now(self.market_timezone)
        
        # Check if it's a weekday
        if now.weekday() > 4:  # Saturday = 5, Sunday = 6
            return False
            
        # Convert time to market hours (9:30 AM - 4:00 PM EST)
        market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
        
        return market_open <= now <= market_close
        
    def get_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch current market data for a given stock symbol
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            
            if data.empty:
                return {"error": f"No data available for symbol {symbol}"}
                
            latest = data.iloc[-1]
            
            return {
                "symbol": symbol,
                "price": round(latest["Close"], 2),
                "volume": int(latest["Volume"]),
                "change": round((latest["Close"] - latest["Open"]) / latest["Open"] * 100, 2),
                "market_open": self.is_market_open(),
                "timestamp": self.get_current_market_time()
            }
        except Exception as e:
            return {"error": str(e)}
            
    def get_intraday_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch intraday data for day trading analysis
        Returns 1-minute interval data for the current trading day
        """
        try:
            now = datetime.now(self.market_timezone)
            
            # Check cache
            cache_key = f"{symbol}_{now.date()}"
            if cache_key in self.cache:
                cache_time, cache_data = self.cache[cache_key]
                if now - cache_time < self.cache_timeout:
                    return cache_data
            
            # Fetch new data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            
            if data.empty:
                return {"error": f"No intraday data available for symbol {symbol}"}
            
            # Convert to dict format
            result = {
                "Open": data["Open"].tolist(),
                "High": data["High"].tolist(),
                "Low": data["Low"].tolist(),
                "Close": data["Close"].tolist(),
                "Volume": data["Volume"].tolist(),
                "Datetime": data.index.strftime('%Y-%m-%d %H:%M:%S').tolist(),
                "market_open": self.is_market_open(),
                "timestamp": self.get_current_market_time()
            }
            
            # Update cache
            self.cache[cache_key] = (now, result)
            
            return result
            
        except Exception as e:
            return {"error": str(e)}
