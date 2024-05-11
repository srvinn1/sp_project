# dashboard_section.py
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QGridLayout
import pyqtgraph as pg

class DashboardSection(QGroupBox):
    def __init__(self):
        super().__init__("Dashboard")
        layout = QGridLayout()

        # CPU Graph
        cpu_box = QGroupBox("CPU Usage")
        cpu_layout = QVBoxLayout()
        self.cpu_plot = pg.PlotWidget(title="CPU Usage (%)")
        self.cpu_plot.setYRange(0, 100)
        self.cpu_curve = self.cpu_plot.plot(pen=pg.mkPen('y', width=2))
        self.cpu_data = [0] * 60  # Last 60 seconds for CPU usage
        cpu_layout.addWidget(self.cpu_plot)
        cpu_box.setLayout(cpu_layout)
        layout.addWidget(cpu_box, 0, 0)

        # Memory Graph
        memory_box = QGroupBox("Memory Usage")
        memory_layout = QVBoxLayout()
        self.memory_plot = pg.PlotWidget(title="Memory Usage (%)")
        self.memory_plot.setYRange(0, 100)
        self.memory_curve = self.memory_plot.plot(pen=pg.mkPen('b', width=2))
        self.memory_data = [0] * 60  # Last 60 seconds for memory usage
        memory_layout.addWidget(self.memory_plot)
        memory_box.setLayout(memory_layout)
        layout.addWidget(memory_box, 1, 0)

        # Disk Graph
        disk_box = QGroupBox("Disk Usage")
        disk_layout = QVBoxLayout()
        self.disk_plot = pg.PlotWidget(title="Disk Usage (%)")
        self.disk_plot.setYRange(0, 100)
        self.disk_curve = self.disk_plot.plot(pen=pg.mkPen('g', width=2))
        self.disk_data = [0] * 60  # Last 60 seconds for disk usage
        disk_layout.addWidget(self.disk_plot)
        disk_box.setLayout(disk_layout)
        layout.addWidget(disk_box, 0, 1)

        # Processes Graph
        process_box = QGroupBox("Process Count")
        process_layout = QVBoxLayout()
        self.process_plot = pg.PlotWidget(title="Process Count")
        self.process_plot.setYRange(0, 200)  # Adjust as per your average process count
        self.process_curve = self.process_plot.plot(pen=pg.mkPen('r', width=2))
        self.process_data = [0] * 60  # Last 60 seconds for process count
        process_layout.addWidget(self.process_plot)
        process_box.setLayout(process_layout)
        layout.addWidget(process_box, 1, 1)

        self.setLayout(layout)

    def update_graphs(self, cpu_data, memory_data, disk_data, process_data):
        """Update the graph data."""
        self.cpu_curve.setData(cpu_data)
        self.memory_curve.setData(memory_data)
        self.disk_curve.setData(disk_data)
        self.process_curve.setData(process_data)
