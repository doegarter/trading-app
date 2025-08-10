import pytest
from src.trading.strategy import TradingStrategy
from src.trading.market_data import MarketData
from src.trading.executor import TradeExecutor

def test_strategy_analysis():
    strategy = TradingStrategy()
    market_data = MarketData()
    signals = strategy.analyze(market_data)
    assert isinstance(signals, list)

def test_position_size_calculation():
    strategy = TradingStrategy()
    size = strategy.calculate_position_size(capital=10000, risk=1)
    assert size == 100

def test_paper_trading_execution():
    executor = TradeExecutor()
    result = executor.execute("BTC/USDT", "buy", 0.1)
    assert result["status"] == "success"
    assert result["type"] == "paper"
