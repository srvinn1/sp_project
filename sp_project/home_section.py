# home_section.py
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel

class HomeSection(QGroupBox):
    def __init__(self):
        super().__init__("Overall System Information")
        layout = QVBoxLayout()

        # Placeholder labels for overall data
        self.cpu_label = QLabel("Average CPU Usage: 0%")
        self.memory_label = QLabel("Average Memory Usage: 0%")
        self.disk_label = QLabel("Disk Usage: 0%")
        self.processes_label = QLabel("Number of Processes: 0")
        self.network_label = QLabel("Network Traffic (Placeholder)")

        # Add the labels to the layout
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.memory_label)
        layout.addWidget(self.disk_label)
        layout.addWidget(self.processes_label)
        layout.addWidget(self.network_label)

        self.setLayout(layout)

    def update_overall_info(self, avg_cpu, avg_memory, disk_usage, process_count):
        """Update the overall system information labels."""
        self.cpu_label.setText(f"Average CPU Usage: {avg_cpu}%")
        self.memory_label.setText(f"Average Memory Usage: {avg_memory}%")
        self.disk_label.setText(f"Disk Usage: {disk_usage}%")
        self.processes_label.setText(f"Number of Processes: {process_count}")
