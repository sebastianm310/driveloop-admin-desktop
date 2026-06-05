from qasync import asyncSlot
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QComboBox, QFrame
)
from app.services.usuarios_service import UsuariosService


class UsuarioEditDialog(QDialog):
    def __init__(self, usuario=None, parent=None):
        super().__init__(parent)
        self.usuario = usuario
        self.is_edit = usuario is not None
        
        titulo_texto = f"Editar usuario #{self.usuario['id']}" if self.is_edit else "Crear nuevo usuario"
        self.setWindowTitle(titulo_texto)
        self.setMinimumWidth(420)
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        titulo_texto = f"Editar usuario #{self.usuario['id']}" if self.is_edit else "Agregar usuario"
        titulo = QLabel(titulo_texto)
        titulo.setObjectName("pageTitle")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(12)

        # Inputs
        self.input_nombre = QLineEdit(str(self.usuario["nom"] or "") if self.is_edit else "")
        self.input_apellido = QLineEdit(str(self.usuario["ape"] or "") if self.is_edit else "")
        self.input_email = QLineEdit(str(self.usuario["email"] or "") if self.is_edit else "")
        self.input_tel = QLineEdit(str(self.usuario.get("tel") or "") if self.is_edit else "")
        
        card_layout.addWidget(QLabel("Nombre"))
        card_layout.addWidget(self.input_nombre)

        card_layout.addWidget(QLabel("Apellido"))
        card_layout.addWidget(self.input_apellido)

        card_layout.addWidget(QLabel("Correo Electrónico"))
        card_layout.addWidget(self.input_email)

        card_layout.addWidget(QLabel("Teléfono"))
        card_layout.addWidget(self.input_tel)

        if not self.is_edit:
            self.input_password = QLineEdit()
            self.input_password.setEchoMode(QLineEdit.Password)
            card_layout.addWidget(QLabel("Contraseña"))
            card_layout.addWidget(self.input_password)

        self.select_activo = QComboBox()
        self.select_activo.addItem("Sí", True)
        self.select_activo.addItem("No", False)

        if self.is_edit:
            valor_activo = bool(self.usuario.get("is_active", True))
            index = self.select_activo.findData(valor_activo)
            if index != -1:
                self.select_activo.setCurrentIndex(index)

        card_layout.addWidget(QLabel("Activo"))
        card_layout.addWidget(self.select_activo)

        btn_guardar = QPushButton("Guardar cambios" if self.is_edit else "Crear usuario")
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #282828;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3f3f46;
            }
        """)
        btn_guardar.clicked.connect(self.guardar)

        card_layout.addWidget(btn_guardar)
        card.setLayout(card_layout)

        layout.addWidget(card)
        self.setLayout(layout)

    @asyncSlot()
    async def guardar(self):
        nombre = self.input_nombre.text().strip()
        apellido = self.input_apellido.text().strip()
        email = self.input_email.text().strip()
        tel = self.input_tel.text().strip()
        activo = self.select_activo.currentData()

        if not nombre or not apellido or not email:
            QMessageBox.warning(self, "Campos requeridos", "Completa nombre, apellido y correo.")
            return

        data = {
            "name": nombre,
            "last_name": apellido,
            "email": email,
            "tel": tel,
            "is_active": activo
        }

        if not self.is_edit:
            password = self.input_password.text().strip()
            if not password:
                QMessageBox.warning(self, "Campos requeridos", "La contraseña es requerida para nuevos usuarios.")
                return
            data["password"] = password
            data["device_name"] = "Desktop"

        try:
            if self.is_edit:
                response = await UsuariosService.actualizar_usuario(self.usuario["id"], data)
            else:
                response = await UsuariosService.crear_usuario(data)
                
            if isinstance(response, dict) and response.get("status") == "Success":
                QMessageBox.information(self, "Éxito", "Usuario guardado correctamente.")
                self.accept()
            elif isinstance(response, dict) and "message" in response:
                QMessageBox.warning(self, "Error", response["message"])
            else:
                # If the API doesn't return {"status": "Success"}, we might just assume success if it didn't throw HTTP error.
                # It depends on how the API is formatted.
                # As observed in ApiClient, on error it returns {"success": False, "message": "..."}
                if isinstance(response, dict) and response.get("success") is False:
                    QMessageBox.warning(self, "Error", response.get("message", "Error desconocido"))
                else:
                    QMessageBox.information(self, "Éxito", "Usuario guardado correctamente.")
                    self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No fue posible guardar el usuario.\n\n{e}")
