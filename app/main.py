from fastapi import FastAPI
from app.core.config import settings

from app.routers import product

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json"
)


app.include_router(product.router, tags=["Product"])