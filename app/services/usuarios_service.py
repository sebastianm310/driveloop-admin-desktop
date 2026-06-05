from app.services.api_client import ApiClient

class UsuariosService:
    @staticmethod
    async def listar_usuarios():
        response = await ApiClient.get("/usuarios")
        if isinstance(response, list):
            return response
        return response.get("data", [])

    @staticmethod
    async def crear_usuario(data):
        return await ApiClient.post("/usuarios", json_data=data)

    @staticmethod
    async def actualizar_usuario(usuario_id, data):
        return await ApiClient.put(f"/usuarios/{usuario_id}", json_data=data)

    @staticmethod
    async def eliminar_usuario(usuario_id):
        return await ApiClient.delete(f"/usuarios/{usuario_id}")