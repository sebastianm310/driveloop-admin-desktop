from qasync import asyncSlot
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFrame,
    QPushButton, QGridLayout, QMessageBox, QHBoxLayout
)
from app.services.usuarios_service import UsuariosService
from app.ui.usuario_edit_dialog import UsuarioEditDialog


class UsuarioDetalleDialog(QDialog):
    def __init__(self, usuario, parent=None):
        super().__init__(parent)
        self.usuario = usuario
        self.setWindowTitle(f"Detalle del usuario #{usuario['id']}")
        self.setMinimumWidth(560)
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        titulo = QLabel(f"Detalle del usuario #{self.usuario['id']}")
        titulo.setObjectName("pageTitle")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        card = QFrame()
        card.setObjectName("card")

        grid = QGridLayout()
        grid.setContentsMargins(18, 18, 18, 18)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(12)

        datos = [
            ("ID", self.usuario["id"]),
            ("Nombre", self.usuario["nom"] or ""),
            ("Apellido", self.usuario["ape"] or ""),
            ("Correo", self.usuario["email"] or ""),
            ("Teléfono", self.usuario["tel"] or ""),
            ("Activo", "Sí" if self.usuario.get("is_active") else "No")
        ]

        for i, (label_text, value) in enumerate(datos):
            label = QLabel(f"{label_text}:")
            label.setStyleSheet("font-weight: bold;")
            valor = QLabel(str(value))
            valor.setWordWrap(True)

            grid.addWidget(label, i, 0)
            grid.addWidget(valor, i, 1)

        card.setLayout(grid)
        layout.addWidget(card)

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)

        btn_editar = QPushButton("Editar")
        btn_editar.setStyleSheet("""
            QPushButton {
                background-color: #282828;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3f3f46;
            }
        """)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #B91C1C;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #991B1B;
            }
        """)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setStyleSheet("""
            QPushButton {
                padding: 8px 14px;
                border-radius: 8px;
                background-color: #E5E7EB;
                color: #374151;
            }
            QPushButton:hover {
                background-color: #D1D5DB;
            }
        """)

        btn_editar.clicked.connect(self.editar_usuario)
        btn_eliminar.clicked.connect(self.eliminar_usuario)
        btn_cerrar.clicked.connect(self.reject)

        botones_layout.addWidget(btn_editar)
        botones_layout.addWidget(btn_eliminar)
        botones_layout.addStretch()
        botones_layout.addWidget(btn_cerrar)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

    def editar_usuario(self):
        dialog = UsuarioEditDialog(self.usuario, self)
        if dialog.exec():
            self.accept()

    @asyncSlot()
    async def eliminar_usuario(self):
        confirm = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de eliminar este usuario?\n\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                response = await UsuariosService.eliminar_usuario(self.usuario["id"])
                
                # Check response structure to handle different API behaviors
                if isinstance(response, dict):
                    if response.get("status") == "Success":
                        QMessageBox.information(self, "Eliminado", "Usuario eliminado correctamente.")
                        self.accept()
                    else:
                        QMessageBox.warning(self, "Error", response.get("message", "Error al eliminar."))
                else:
                    QMessageBox.information(self, "Eliminado", "Usuario eliminado correctamente.")
                    self.accept()
                    
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"No fue posible eliminar el usuario.\n\n{e}"
                )
