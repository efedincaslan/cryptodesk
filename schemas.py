from pydantic import BaseModel, field_validator

class OrderRequest(BaseModel):
    coin: str
    quantity: float
    price: float
    order_type: str

    @field_validator("quantity")
    def quantity_positive(cls, v):
        if v <= 0:
            raise ValueError("quantity must be greater than 0")
        return v
    @field_validator("price")
    def price_positive(cls, v):
        if v <= 0:
            raise ValueError('price must be greater than 0')
        return v
    @field_validator("order_type")
    def order_type_valid(cls, v):
        if v != 'buy' and v != 'sell':
            raise ValueError('must be a valid execution command')
        return v