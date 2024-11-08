import pytest
from httpx import AsyncClient

from app.main import app
from app.core.database_manager import get_db


# Sample product data for testing
sample_product = {
    "name": "Test Product",
    "description": "A product for testing",
    "price": 10.99,
    "inventory_count": 100,
    "category": "Test Category"
}


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def db_session():
    # Setup the test database session here
    db = get_db()
    yield db
    # Optionally teardown/clean test database data here


# Test product creation
@pytest.mark.asyncio
async def test_create_product(async_client):
    response = await async_client.post("/products", json=sample_product)
    assert response.status_code == 200
    product_data = response.json()
    assert product_data["name"] == sample_product["name"]
    assert product_data["inventory_count"] == sample_product["inventory_count"]


# Test retrieving a product by ID
@pytest.mark.asyncio
async def test_get_product(async_client):
    # Create the product first
    create_response = await async_client.post("/products", json=sample_product)
    product_id = create_response.json()["id"]

    # Retrieve the product
    response = await async_client.get(f"/products/{product_id}")
    assert response.status_code == 200
    product_data = response.json()
    assert product_data["name"] == sample_product["name"]


# Test retrieving all products with an optional search keyword
@pytest.mark.asyncio
async def test_get_products(async_client):
    response = await async_client.get("/products")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)

    # Test search by keyword
    response = await async_client.get("/products", params={"search_keyword": "Test"})
    assert response.status_code == 200
    products = response.json()
    assert any(product["name"] == sample_product["name"] for product in products)


# Test updating a product by ID
@pytest.mark.asyncio
async def test_update_product(async_client):
    create_response = await async_client.post("/products", json=sample_product)
    product_id = create_response.json()["id"]

    update_data = {"description": "Updated Description"}
    response = await async_client.put(f"/products/{product_id}", json=update_data)
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["description"] == "Updated Description"


# Test patching inventory (adding stock)
@pytest.mark.asyncio
async def test_add_inventory(async_client):
    create_response = await async_client.post("/products", json=sample_product)
    product_id = create_response.json()["id"]

    response = await async_client.patch(f"/products/{product_id}/add-inventory", params={"quantity": 10})
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["inventory_count"] == sample_product["inventory_count"] + 10


# Test deleting a product
@pytest.mark.asyncio
async def test_delete_product(async_client):
    create_response = await async_client.post("/products", json=sample_product)
    product_id = create_response.json()["id"]

    response = await async_client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    delete_message = response.json()
    assert delete_message["detail"] == "Product deleted"

    # Confirm deletion by attempting to get the deleted product
    get_response = await async_client.get(f"/products/{product_id}")
    assert get_response.status_code == 404


# Test recording a sale for a product
@pytest.mark.asyncio
async def test_record_sale(async_client):
    create_response = await async_client.post("/products", json=sample_product)
    product_id = create_response.json()["id"]

    sale_data = {"quantity": 5}
    response = await async_client.post(f"/products/{product_id}/sales", json=sale_data)
    assert response.status_code == 200
    sale = response.json()
    assert sale["product_id"] == product_id
    assert sale["quantity"] == 5

    # Verify that popularity_score is updated (if set by your calculation)
    product_response = await async_client.get(f"/products/{product_id}")
    product_data = product_response.json()
    # Check if popularity_score calculation is correct according to your formula
    assert product_data["popularity_score"] > 0
