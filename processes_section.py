# processes_section.py
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QListWidget
import psutil
import pyqtgraph as pg

class ProcessesSection(QGroupBox):
    def __init__(self, show_detailed=True):
        super().__init__("Processes Count and Details")
        layout = QVBoxLayout()

        # Processes Count graph
        self.process_plot = pg.PlotWidget(title="Running Processes")
        self.process_plot.setYRange(0, 200)  # Adjust based on average count
        self.process_curve = self.process_plot.plot(pen=pg.mkPen('b', width=2))
        self.process_data = [0] * 60  # Last 60 seconds of process count

        layout.addWidget(self.process_plot)

        if show_detailed:
            # Detailed information
            self.process_count_label = QLabel("Current Process Count: 0")

            # Add a list widget to display the names of processes
            self.process_list = QListWidget()
            self.process_list.setFixedHeight(200)

            # Add detailed information to the layout
            details_layout = QVBoxLayout()
            details_layout.addWidget(self.process_count_label)
            details_layout.addWidget(self.process_list)

            combined_layout = QHBoxLayout()
            combined_layout.addLayout(layout)
            combined_layout.addLayout(details_layout)

            self.setLayout(combined_layout)
        else:
            # Only graph layout
            self.setLayout(layout)

    def update_processes(self, data):
        """Update the Processes graph data and optionally update the details."""
        self.process_curve.setData(data)

        # Update detailed labels only if they're visible
        try:
            current_processes = psutil.pids()
            process_count = len(current_processes)
            self.process_count_label.setText(f"Current Process Count: {process_count}")

            # Update the list of processes with names and PIDs
            self.process_list.clear()
            for pid in current_processes[:10]:  # Display only the top 10 processes
                try:
                    proc = psutil.Process(pid)
                    proc_info = f"{proc.pid}: {proc.name()}"
                    self.process_list.addItem(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except AttributeError:
            pass
