from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QGridLayout
from qasync import asyncSlot
from app.services.dashboard_service import DashboardService


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.labels = {}
        self.build_ui()
        self.load_data()

    def build_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        titulo = QLabel("Dashboard administrativo")
        titulo.setObjectName("pageTitle")
        main_layout.addWidget(titulo)

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(16)

        titulos = [
            "Total usuarios",
            "Total vehículos",
            "Vehículos disponibles",
            "Tickets abiertos",
            "Total reservas",
        ]
        keys = ["usuarios", "vehiculos", "vehiculos_disponibles", "tickets_abiertos", "reservas"]

        positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]

        for titulo_texto, key, (row, col) in zip(titulos, keys, positions):
            card = QFrame()
            card.setObjectName("card")
            card.setMinimumHeight(120)

            card_layout = QVBoxLayout()
            card_layout.setContentsMargins(18, 18, 18, 18)
            card_layout.setSpacing(8)

            label_title = QLabel(titulo_texto)
            label_title.setObjectName("sectionTitle")

            label_value = QLabel("0")
            label_value.setObjectName("metricValue")
            self.labels[key] = label_value

            card_layout.addWidget(label_title)
            card_layout.addWidget(label_value)
            card_layout.addStretch()

            card.setLayout(card_layout)
            grid.addWidget(card, row, col)

        main_layout.addLayout(grid)
        main_layout.addStretch()
        self.setLayout(main_layout)

    @asyncSlot()
    async def load_data(self):
        metrics = await DashboardService.get_metrics()
        for key, value in metrics.items():
            if key in self.labels:
                self.labels[key].setText(str(value))