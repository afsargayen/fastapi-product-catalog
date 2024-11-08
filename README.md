# FastAPI Product Catalog with Sales API

This is a product catalog API built with **FastAPI**, using **MySQL** as the database. The API supports CRUD operations for managing products, handling inventory updates, and recording sales. It also calculates the **product popularity score** based on sales data.

## Features

- **Product Management**: Create, read, update, and delete products.
- **Inventory Management**: Add or remove product inventory.
- **Sales Recording**: Record sales and update product popularity score based on sales.
- **Search**: Search products by name, description, or category.
- **Dockerized**: The application is fully containerized with Docker.
- **Test Coverage**: Automated tests are included for all endpoints.

## Prerequisites

- Docker
- Docker Compose
- Python 3.10+

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/afsargayen/fastapi-product-catalog.git
   cd fastapi-product-catalog

2. To build the project and start the services in detached mode:

    ```bash
   sudo docker compose up --build -d
   
3. To run migrations:
    
    ```bash
   sudo docker exec -ti app_container bash
    poetry run alembic upgrade head
   
4. To run the test cases:

    ```bash
   poetry run pytest tests/