from qasync import asyncSlot
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton,
    QHBoxLayout, QAbstractItemView
)
from app.services.usuarios_service import UsuariosService
from app.ui.usuario_detalle_dialog import UsuarioDetalleDialog
from app.ui.usuario_edit_dialog import UsuarioEditDialog


class UsuariosPage(QWidget):
    def __init__(self):
        super().__init__()
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        header_layout = QHBoxLayout()
        titulo = QLabel("Gestión de usuarios")
        titulo.setObjectName("pageTitle")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")
        
        btn_agregar = QPushButton("+ Agregar usuario de soporte")
        btn_agregar.setStyleSheet("""
            QPushButton {
                background-color: #C91843;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #9B1B39;
            }
        """)
        btn_agregar.clicked.connect(self.abrir_crear)

        header_layout.addWidget(titulo)
        header_layout.addStretch()
        header_layout.addWidget(btn_agregar)

        layout.addLayout(header_layout)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        
        columnas = ["ID", "Nombre", "Apellido", "Correo", "Teléfono", "Activo", "Acción"]
        self.table.setColumnCount(len(columnas))
        self.table.setHorizontalHeaderLabels(columnas)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.Fixed)
        self.table.setColumnWidth(6, 120)

        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_data()

    @asyncSlot()
    async def load_data(self):
        usuarios = await UsuariosService.listar_usuarios()
        if not usuarios:
            usuarios = []

        self.table.setRowCount(0)
        self.table.setRowCount(len(usuarios))

        for row, usuario in enumerate(usuarios):
            self.table.setItem(row, 0, QTableWidgetItem(str(usuario["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(usuario["nom"] or "")))
            self.table.setItem(row, 2, QTableWidgetItem(str(usuario["ape"] or "")))
            self.table.setItem(row, 3, QTableWidgetItem(str(usuario["email"] or "")))
            self.table.setItem(row, 4, QTableWidgetItem(str(usuario.get("tel") or "")))
            self.table.setItem(row, 5, QTableWidgetItem("Sí" if usuario.get("is_active") else "No"))
            
            btn_detalle = QPushButton("Ver detalle")
            btn_detalle.setStyleSheet("""
                QPushButton {
                    background-color: #C91843;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 6px 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #9B1B39;
                }
            """)
            btn_detalle.clicked.connect(
                lambda checked=False, u=usuario: self.abrir_detalle(u)
            )
            self.table.setCellWidget(row, 6, btn_detalle)
            self.table.setRowHeight(row, 42)

    def abrir_crear(self):
        dialog = UsuarioEditDialog(parent=self)
        if dialog.exec():
            self.load_data()

    def abrir_detalle(self, usuario):
        dialog = UsuarioDetalleDialog(usuario, self)
        if dialog.exec():
            self.load_data()