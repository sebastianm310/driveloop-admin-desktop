from app.services.api_client import ApiClient

class TicketsService:
    @staticmethod
    async def listar_tickets():
        response = await ApiClient.get("/tickets")
        if isinstance(response, list):
            return response
        return response.get("data", [])