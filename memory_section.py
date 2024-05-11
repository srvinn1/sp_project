import sys
import psutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QSizePolicy
)
from PyQt5.QtCore import QTimer, QSize

class TopMemoryProcessesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Top 5 Memory Processes")
        

        # Layout and label
        layout = QVBoxLayout()

        # Table Widget for displaying the process information
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["PID", "Name", "Memory %", "Memory (MB)"])
        layout.addWidget(self.table)

        # Update the process table periodically
        self.update_process_info()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_process_info)
        self.timer.start(2000)  # Update every 2 seconds

        self.setLayout(layout)

    def update_process_info(self):
        """Update the table with the top 5 memory processes."""
        # Retrieve all processes with minimal necessary attributes
        processes = [proc for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'memory_info'])]

        def safe_get_memory_percent(proc):
            try:
                return proc.info['memory_percent'] or 0.0  # Use 0.0 as a fallback if the value is None
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return 0.0

        # Sort processes by memory percentage, using a safe fallback
        sorted_procs = sorted(processes, key=lambda p: safe_get_memory_percent(p), reverse=True)

        # Clear the table and set the row count for the top 5 processes
        self.table.setRowCount(min(len(sorted_procs), 5))

        # Populate the table with the top 5 memory-consuming processes
        for row, proc in enumerate(sorted_procs[:5]):
            try:
                pid = proc.info['pid']
                name = proc.info['name'] or "Unknown"
                memory_percent = proc.info['memory_percent'] or 0.0
                memory_mb = proc.info['memory_info'].rss / (1024 * 1024) if proc.info['memory_info'] else 0.0

                # Fill table cells
                self.table.setItem(row, 0, QTableWidgetItem(str(pid)))
                self.table.setItem(row, 1, QTableWidgetItem(name))
                self.table.setItem(row, 2, QTableWidgetItem(f"{memory_percent:.2f}%"))
                self.table.setItem(row, 3, QTableWidgetItem(f"{memory_mb:.2f} MB"))

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

