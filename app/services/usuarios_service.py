from app.services.api_client import ApiClient

class UsuariosService:
    @staticmethod
    async def listar_usuarios():
        response = await ApiClient.get("/usuarios")
        if isinstance(response, list):
            return response
        return response.get("data", [])