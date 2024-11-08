from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException

from app import schemas
from app.core.database_manager import get_db
from app.services.model_service import ProductService, SaleService

router = APIRouter()
product_service = ProductService(get_db())
sale_service = SaleService(get_db())

@router.post("/products", response_model=schemas.ProductCreate)
async def create_product(product: schemas.ProductCreate):
    return product_service.create(obj_in=product)


@router.get("/products/{product_id}", response_model=schemas.ProductCreate)
async def get_product(product_id: int):
    db_product = product_service.get_by_id(record_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.get("/products", response_model=List[schemas.ProductCreate])
async def get_products(search_keyword: Optional[str] = None):
    if search_keyword is None:
        products = product_service.get_all()
    else:
        search_terms = {
            "name": search_keyword,
            "description": search_keyword,
            "category": search_keyword
        }
        products = product_service.get_all(search_terms=search_terms)
    if len(products) == 0:
        raise HTTPException(status_code=404, detail="Products not available")
    return products


@router.put("/products/{product_id}", response_model=schemas.ProductCreate)
async def update_product(product_id: int, product: schemas.ProductUpdate):
    db_product = product_service.get_by_id(product_id)
    if db_product:
        return product_service.update(db_obj=db_product, obj_in=product)
    raise HTTPException(status_code=404, detail="Products not available")


@router.patch("/products/{product_id}/add-inventory", response_model=schemas.ProductCreate)
async def update_product(product_id: int, quantity: int):
    db_product = product_service.get_by_id(product_id)
    if db_product:
        return product_service.update(db_obj=db_product, obj_in={
            "inventory_count": (db_product.inventory_count + quantity)
        })
    raise HTTPException(status_code=404, detail="Products not available")


@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    id_deleted = product_service.delete(record_id=product_id)
    if id_deleted:
        return {"detail": "Product deleted"}
    raise HTTPException(status_code=404, detail="Products not available")


@router.post("/products/{product_id}/sales", response_model=schemas.Sale)
async def record_sale(product_id: int, quantity: int):
    product = product_service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not available")

    if quantity > 0 and product.inventory_count < quantity:
        raise HTTPException(status_code=400, detail="Sufficient product is not available")

    sale = sale_service.create_sale(product_id=product_id, quantity=quantity)
    return sale
