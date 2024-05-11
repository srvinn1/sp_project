# menu_section.py
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QListWidget
from PyQt5.QtCore import pyqtSignal, QObject

class MenuSignals(QObject):
    """Signals for menu item clicks."""
    cpu_item_clicked = pyqtSignal()
    memory_item_clicked = pyqtSignal()
    disk_item_clicked = pyqtSignal()
    processes_item_clicked = pyqtSignal()
    network_item_clicked = pyqtSignal()

class MenuSection(QGroupBox):
    def __init__(self):
        super().__init__("Menu")
        layout = QVBoxLayout()
        self.signals = MenuSignals()
        self.menu_items = QListWidget()
        self.menu_items.addItems(["Home", "CPU", "Memory", "Disk", "Processes", "Network"])
        self.menu_items.clicked.connect(self.on_item_click)
        layout.addWidget(self.menu_items)
        self.setLayout(layout)

    def on_item_click(self, index):
        """Handle item clicks based on the selected index."""
        item_text = self.menu_items.model().data(index)
        if item_text == "CPU":
            self.signals.cpu_item_clicked.emit()
        elif item_text == "Memory":
            self.signals.memory_item_clicked.emit()
        elif item_text == "Disk":
            self.signals.disk_item_clicked.emit()
        elif item_text == "Processes":
            self.signals.processes_item_clicked.emit()
        elif item_text == "Network":
            self.signals.network_item_clicked.emit()
