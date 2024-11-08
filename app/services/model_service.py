from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import *
from .base_service import BaseService


class ProductService(BaseService[Product]):
    def __init__(self, db: Session):
        super().__init__(Product, db)

    def update_popularity_score(self, product_id: int, quantity: int, total_sales_quantity: int):
        weight = 1.5
        popularity_score = total_sales_quantity * weight

        product = self.get_by_id(product_id)
        if product:
            self.update(db_obj=product, obj_in={
                "popularity_score": float(popularity_score),
                "inventory_count": (product.inventory_count - quantity)
            })


class SaleService(BaseService[Sale]):
    def __init__(self, db: Session):
        super().__init__(Sale, db)

    def create_sale(self, product_id: int, quantity: int):
        sale = self.create({
            "product_id": product_id,
            "quantity": quantity
        })

        total_sales_quantity = self.db.query(func.sum(self.model.quantity)).filter(
            self.model.product_id == product_id).scalar() or 0

        product_service = ProductService(self.db)
        product_service.update_popularity_score(product_id, quantity, int(total_sales_quantity))
        return sale

