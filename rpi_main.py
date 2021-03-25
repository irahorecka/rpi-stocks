from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from model import DB
from rpi import RPi_3BP
from stocks import Stock

app = FastAPI()


class Ticker(BaseModel):
    symbol: str
    shares: float
    cost_basis: float


@app.get("/tickers/{ticker_id}")
def read_item(ticker_id: int, q: Optional[str] = None):
    return {"ticker_id": ticker_id, "q": q}


@app.put("/tickers/{ticker_id}")
def update_item(ticker_id: int, ticker: Ticker):
    return {"ticker_symbol": ticker.symbol, "ticker_id": ticker_id}
