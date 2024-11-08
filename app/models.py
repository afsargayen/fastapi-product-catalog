from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), index=True)
    description = Column(String(255), index=True)
    price = Column(Float)
    inventory_count = Column(Integer)
    category = Column(String(64), index=True)
    popularity_score = Column(Float, default=0.0)

    sales = relationship("Sale", back_populates="product")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    timestamp = Column(DateTime, default=func.now())

    product = relationship("Product", back_populates="sales")