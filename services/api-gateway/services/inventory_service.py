from utils.http_client import client

INVENTORY_SERVICE_URL = "http://localhost:8005"

async def get_inventory(inventory_id: int):
    response = await client.get(f"{INVENTORY_SERVICE_URL}/inventory/{inventory_id}")
    return response.json()
