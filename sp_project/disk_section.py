import sys
import psutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import QTimer, QSize


class TopDiskProcessesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Top 5 Disk I/O Processes")
        self.setFixedSize(QSize(450, 200))

        # Layout and Table Widget for displaying the process information
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["PID", "Name", "Read (MB)", "Write (MB)"])
        layout.addWidget(self.table)

        # Update the process table periodically
        self.update_process_info()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_process_info)
        self.timer.start(2000)  # Update every 2 seconds

        self.setLayout(layout)

    def update_process_info(self):
        """Update the table with the top 5 processes by disk I/O."""
        def safe_get_disk_io(proc):
            try:
                io_counters = proc.info['io_counters']
                return (io_counters.read_bytes, io_counters.write_bytes) if io_counters else (0, 0)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return (0, 0)

        # Retrieve all processes with minimal necessary attributes
        processes = [proc for proc in psutil.process_iter(['pid', 'name', 'io_counters'])]

        # Sort processes by total disk I/O (read + write bytes)
        sorted_procs = sorted(processes, key=lambda p: sum(safe_get_disk_io(p)), reverse=True)

        # Clear the table and set the row count for the top 5 processes
        self.table.setRowCount(min(len(sorted_procs), 5))

        # Populate the table with the top 5 disk I/O-consuming processes
        for row, proc in enumerate(sorted_procs[:5]):
            try:
                pid = proc.info['pid']
                name = proc.info['name'] or "Unknown"
                read_bytes, write_bytes = safe_get_disk_io(proc)
                read_mb = read_bytes / (1024 * 1024)
                write_mb = write_bytes / (1024 * 1024)

                # Fill table cells
                self.table.setItem(row, 0, QTableWidgetItem(str(pid)))
                self.table.setItem(row, 1, QTableWidgetItem(name))
                self.table.setItem(row, 2, QTableWidgetItem(f"{read_mb:.2f} MB"))
                self.table.setItem(row, 3, QTableWidgetItem(f"{write_mb:.2f} MB"))

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TopDiskProcessesWidget()
    window.show()
    sys.exit(app.exec_())
