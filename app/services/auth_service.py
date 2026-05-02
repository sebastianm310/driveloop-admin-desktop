from app.services.api_client import ApiClient

class AuthService:
    @staticmethod
    async def login(email, password):
        response = await ApiClient.post(
            "/login", 
            json_data={
                'email': email,
                'password': password, 
                "device_name": "Desktop"
            }
        )
        
        if response.get("status") == "Success":
            user = response.get("data").get("user")
            token = user.get("token")
            
            ApiClient.set_token(token)
            
            return {
                "success": True,
                "user": {
                    "nom": user.get("name"),
                    "ape": "", # La API no devuelve apellido y mainWindow.py espera un valor
                    "email": user.get("email")
                }
            }
        else:
            return {
                "success": False,
                "message": response.get("message", "Credenciales inválidas")
            }