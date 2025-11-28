from utils.http_client import client

PAYMENT_SERVICE_URL = "http://localhost:8004"

async def get_payment(payments_id: int):
    response = await client.get(f"{PAYMENT_SERVICE_URL}/payments/{payments_id}")
    return response.json()
