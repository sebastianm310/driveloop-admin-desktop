from app.services.api_client import ApiClient

class VehiculosService:
    @staticmethod
    async def listar_vehiculos():
        response = await ApiClient.get("/vehiculos")
        if isinstance(response, list):
            return response
        return response.get("data", [])

    @staticmethod
    async def obtener_reservas_por_vehiculo(codveh):
        response = await ApiClient.post(f"/vehiculos/{codveh}/reservas")
        if isinstance(response, list):
            return response
        return response.get("data", [])

    @staticmethod
    async def actualizar_vehiculo(cod, data):
        return await ApiClient.put(f"/vehiculos/{cod}", json_data=data)

    @staticmethod
    async def eliminar_vehiculo(cod):
        return await ApiClient.delete(f"/vehiculos/{cod}")