from utils.http_client import client

USER_SERVICE_URL = "http://localhost:8001"

async def get_user(user_id: int):
    response = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
    return response.json()
