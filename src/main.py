from fastapi import FastAPI
from .trading.market_data import MarketData
from .trading.strategy import TradingStrategy
from .trading.executor import TradeExecutor

app = FastAPI(title="Trading App API")
market_data = MarketData()
strategy = TradingStrategy()
executor = TradeExecutor()

@app.get("/")
async def root():
    return {"status": "running"}

@app.get("/market-data/{symbol}")
async def get_market_data(symbol: str):
    return market_data.get_data(symbol)

@app.post("/analyze")
async def analyze_market():
    signals = strategy.analyze(market_data)
    return {"signals": signals}

@app.post("/execute-trade")
async def execute_trade(symbol: str, side: str, quantity: float):
    result = executor.execute(symbol, side, quantity)
    return result
