from app.services.api_client import ApiClient

class DashboardService:
    @staticmethod
    async def get_metrics():
        response = await ApiClient.get("/metricas")
        
        if isinstance(response, list):
            return response
        return response.get("data", [])