# --- all imports at the top, always ---
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
import uuid

from database import engine, get_db, async_session
from models import Base, Order, PriceSnapshot, CoinSymbol
from schemas import OrderRequest
import logging
from sqlalchemy import delete
from datetime import datetime, timezone, timedelta



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- constants ---
COINGECKO_BASE = "https://api.coingecko.com/api/v3"
COIN_IDS = ["bitcoin", "ethereum", "solana", "binancecoin", "avalanche-2"]
SYMBOL_TO_ID = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "AVAX": "avalanche-2",
}

# --- startup ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        await cleanup_old_snapshots(db)
    yield

# --- app created ONCE, with lifespan ---
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- routes ---
@app.get("/prices")
async def get_prices(db: AsyncSession = Depends(get_db)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{COINGECKO_BASE}/coins/markets",
                params={
                    "vs_currency": "usd",
                    "ids": ",".join(COIN_IDS),
                    "order": "market_cap_desc",
                    "price_change_percentage": "24h",
                }
            )
            data = response.json()
    


        for coin in data:
            symbol = coin["symbol"].upper()  # "btc" → "BTC"
            
            if symbol in CoinSymbol.__members__:  # only save coins we track
                snapshot = PriceSnapshot(
                    id=uuid.uuid4(),
                    coin=CoinSymbol[symbol],
                    price=coin["current_price"]
                )
                db.add(snapshot)

        logger.info(f"Fetched prices for {len(data)} coins")
        await db.commit()
        return data
        
    except Exception as e:
        raise HTTPException(status_code=503, detail="Price feed unavailable error")

@app.post("/order")
async def create_order(order: OrderRequest, db: AsyncSession = Depends(get_db)):
    if order.coin.upper() not in CoinSymbol.__members__:
        raise HTTPException(status_code=400, detail="Invalid coin symbol")

    db_order = Order(
    id=uuid.uuid4(),
    coin=CoinSymbol[order.coin],      # hint: order.coin gives "BTC" — how do you use that as a key?
    quantity=order.quantity,
    price=order.price,
    order_type=order.order_type
    )
    db.add(db_order)


    await db.commit()
    logger.info(f"Order placed: {order.order_type} {order.quantity} {order.coin} at {order.price}")
    await db.refresh(db_order)
    return {
    "status": "order placed",
    "id": str(db_order.id),
    "created_at": db_order.created_at
}

async def cleanup_old_snapshots(db: AsyncSession):
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    
    await db.execute(
    delete(PriceSnapshot).where(PriceSnapshot.captured_at < cutoff)
)
    
    await db.commit()
    logger.info(f"Cleaned up snapshots older than 7 days")