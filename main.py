import sys
import asyncio
import traceback
from qasync import QEventLoop
from PySide6.QtWidgets import QApplication
from app.ui.login_window import LoginWindow
from app.utils.styles import APP_STYLE

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