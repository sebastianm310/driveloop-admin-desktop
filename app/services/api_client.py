import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ApiClient:
    _instance = None
    _client = None
    _token = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApiClient, cls).__new__(cls)
            cls._instance.base_url = os.getenv("API_URL", "").rstrip("/")
            cls._client = httpx.AsyncClient(base_url=cls._instance.base_url)
        return cls._instance

    @classmethod
    def set_token(cls, token):
        cls._token = token

    @classmethod
    async def request(cls, method, endpoint, **kwargs):
        if cls._client is None:
            cls()
        
        endpoint = endpoint.lstrip("/")
        
        # Add Authorization header if token is present
        if cls._token:
            headers = kwargs.get("headers", {})
            headers["Authorization"] = f"Bearer {cls._token}"
            kwargs["headers"] = headers

        try:
            response = await cls._client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            try:
                return e.response.json()
            except:
                return {"success": False, "message": f"Error: {e.response.status_code}"}
        except Exception as e:
            print(f"Connection Error: {e}")
            return {"success": False, "message": str(e)}

    @classmethod
    async def get(cls, endpoint, params=None, **kwargs):
        return await cls.request("GET", endpoint, params=params, **kwargs)

    @classmethod
    async def post(cls, endpoint, data=None, json_data=None, **kwargs):
        return await cls.request("POST", endpoint, data=data, json=json_data, **kwargs)

    @classmethod
    async def put(cls, endpoint, data=None, json_data=None, **kwargs):
        return await cls.request("PUT", endpoint, data=data, json=json_data, **kwargs)

    @classmethod
    async def delete(cls, endpoint, **kwargs):
        return await cls.request("DELETE", endpoint, **kwargs)
