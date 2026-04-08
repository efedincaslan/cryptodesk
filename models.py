
from datetime import datetime
import uuid
from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Enum, Numeric, DateTime, func
import enum

class Base(DeclarativeBase):
    pass

# Define valid coins as a Python enum first
class CoinSymbol(enum.Enum):
    BTC = "BTC"
    ETH = "ETH"
    SOL = "SOL"
    BNB = "BNB"
    AVAX = "AVAX"

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    coin: Mapped[CoinSymbol] = mapped_column(Enum(CoinSymbol), nullable=False)
    quantity: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    order_type: Mapped[str] = mapped_column(Enum("buy", "sell", name="order_type_enum"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    coin: Mapped[CoinSymbol] = mapped_column(Enum(CoinSymbol), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())