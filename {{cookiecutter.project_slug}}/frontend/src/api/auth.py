import httpx
from src.config import API_BASE_URL

# Authentication
async def login(username: str, password: str):
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(f"{API_BASE_URL}/auth/login",
                              params={  
                                        "username": username,
                                        "password": password
                                    }
                            )
        r.raise_for_status()
        return r.json()
    