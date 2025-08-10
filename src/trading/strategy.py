from typing import List, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from .market_data import MarketData

class TradingStrategy:
    def __init__(self):
        self.indicators = {}
        
    def analyze(self, symbol: str, market_data: MarketData) -> Dict[str, Any]:
        """
        Day Trading Strategy Analysis
        Uses RSI, VWAP, and Volume analysis for intraday signals
        """
        try:
            # Get market data
            data = market_data.get_intraday_data(symbol)
            if "error" in data:
                return {"error": data["error"]}
                
            df = pd.DataFrame(data)
            
            # Calculate RSI (14 periods)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]
            
            # Calculate VWAP
            df['Typical_Price'] = (df['High'] + df['Low'] + df['Close']) / 3
            df['VP'] = df['Typical_Price'] * df['Volume']
            df['Cumulative_VP'] = df['VP'].cumsum()
            df['Cumulative_Volume'] = df['Volume'].cumsum()
            vwap = df['Cumulative_VP'] / df['Cumulative_Volume']
            current_vwap = vwap.iloc[-1]
            
            # Volume analysis
            avg_volume = df['Volume'].mean()
            current_volume = df['Volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume
            
            # Current price
            current_price = df['Close'].iloc[-1]
            
            # Generate signals based on indicators
            signal = self._generate_signal(
                current_price,
                current_rsi,
                current_vwap,
                volume_ratio
            )
            
            return {
                "timestamp": datetime.now(pytz.UTC).isoformat(),
                "symbol": symbol,
                "price": current_price,
                "indicators": {
                    "rsi": current_rsi,
                    "vwap": current_vwap,
                    "volume_ratio": volume_ratio
                },
                "signal": signal
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _generate_signal(self, price: float, rsi: float, vwap: float, 
                        volume_ratio: float) -> Dict[str, Any]:
        """
        Generate trading signals based on technical indicators
        """
        signal = {
            "action": "HOLD",
            "strength": 0,
            "reasons": []
        }
        
        # RSI conditions
        if rsi < 30:
            signal["reasons"].append("RSI oversold")
            signal["strength"] += 1
        elif rsi > 70:
            signal["reasons"].append("RSI overbought")
            signal["strength"] -= 1
            
        # VWAP conditions
        if price < vwap:
            signal["reasons"].append("Price below VWAP")
            signal["strength"] += 1
        elif price > vwap:
            signal["reasons"].append("Price above VWAP")
            signal["strength"] -= 1
            
        # Volume conditions
        if volume_ratio > 1.5:
            signal["reasons"].append("High volume")
            signal["strength"] = signal["strength"] * 1.5
            
        # Determine final signal
        if signal["strength"] > 1:
            signal["action"] = "BUY"
        elif signal["strength"] < -1:
            signal["action"] = "SELL"
            
        return signal
