import sys
import os
import asyncio
import traceback
from dotenv import load_dotenv
from qasync import QEventLoop
from PySide6.QtWidgets import QApplication
from app.ui.login_window import LoginWindow
from app.utils.styles import APP_STYLE

# --- INICIO DE LA CONFIGURACIÓN DEL .ENV ---
def ruta_recurso(relative_path):
    """ Busca la ruta correcta ya sea en desarrollo o en el .exe compilado """
    try:
        # PyInstaller guarda la ruta de la carpeta temporal en sys._MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Cargamos las variables de entorno antes de iniciar la app
ruta_env = ruta_recurso('.env')
load_dotenv(dotenv_path=ruta_env)
# --- FIN DE LA CONFIGURACIÓN DEL .ENV ---


def main():
    print("Iniciando aplicación...")
    try:
        app = QApplication(sys.argv)
        app.setStyleSheet(APP_STYLE)
        print("QApplication creada con éxito.")

        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)
        print("Bucle de eventos configurado.")

        window = LoginWindow()
        window.show()
        print("Ventana principal mostrada.")

        with loop:
            print("Entrando en el bucle principal...")
            loop.run_forever()
            
    except Exception:
        print("Se produjo un error durante el inicio:")
        traceback.print_exc()

if __name__ == "__main__":
    main()