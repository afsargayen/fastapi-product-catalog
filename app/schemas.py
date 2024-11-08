from pydantic import BaseModel
from datetime import datetime


class SaleBase(BaseModel):
    product_id: int
    quantity: int

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str


class ProductCreate(ProductBase):
    inventory_count: int


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    popularity_score: float

    class Config:
        orm_mode = True
