import sys
import os
import signal
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QLabel, QSpacerItem, QSizePolicy)

class KillerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Layout
        layout = QVBoxLayout()

        # QLineEdit for PID input
        self.pidInput = QLineEdit(self)
        layout.addWidget(self.pidInput)

        # QPushButton to kill the process
        self.killButton = QPushButton('Kill Process', self)
        self.killButton.setStyleSheet("color: purple;")
        self.killButton.setFixedSize(150, 50)
        self.killButton.clicked.connect(self.killProcess)
        layout.addWidget(self.killButton)

        self.setLayout(layout)
        self.setWindowTitle('Process Killer')

    def killProcess(self):
        pid = self.pidInput.text()
        try:
            os.kill(int(pid), signal.SIGTERM)  # Send SIGTERM signal
            self.label.setText(f"Process {pid} has been terminated.")
        except Exception as e:
            self.label.setText(f"Error: {str(e)}")

