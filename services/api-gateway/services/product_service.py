from utils.http_client import client

PRODUCT_SERVICE_URL = "http://localhost:8002"

async def get_product(product_id: int):
    response = await client.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    return response.json()
