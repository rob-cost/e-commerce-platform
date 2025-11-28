from utils.http_client import client

ORDER_SERVICE_URL = "http://localhost:8003"

async def get_order(order_id: int):
    response = await client.get(f"{ORDER_SERVICE_URL}/orders/{order_id}")
    return response.json()
