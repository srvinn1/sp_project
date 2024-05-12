import sys
import psutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QSizePolicy
)
from PyQt5.QtCore import QTimer, QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

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
        self.table.verticalHeader().setVisible(False)
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

class MemoryUsagePlotWidget(QWidget):
    def __init__(self,width,height):
        super().__init__()
        self.setMinimumSize(width, height)
        # Create a figure
        self.figure, self.ax = plt.subplots(figsize=(5, 3))  # Adjust the figsize as needed
        self.canvas = FigureCanvas(self.figure)

        # Set the title and labels with smaller font size
        self.ax.set_title('Memory Usage (%)', fontsize=9, color = '#562680')  # Set font size for the title
        #self.ax.set_xlabel('Time (s)', fontsize=9)        # Set font size for the x-label
        #self.ax.set_ylabel('Usage (%)', fontsize=9)       # Set font size for the y-label

        # Initialize empty data
        self.times = []
        self.memory_usages = []

        # Set up a timer to update the plot every second
        self.timer = self.startTimer(1000)

        # Add canvas to layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def timerEvent(self, event):
        # Get current memory usage
        memory_usage = psutil.virtual_memory().percent

        # Append the current time and memory usage to the data lists
        self.times.append(len(self.times) + 1)
        self.memory_usages.append(memory_usage)

        # Clear previous plot
        self.ax.clear()

        # Plot memory usage
        self.ax.plot(self.times, self.memory_usages, color='#000080')

        # Set title and labels
        self.ax.set_title('Memory Usage (%)', fontsize=9, color = '#562680')  # Set font size for the title
        #self.ax.set_xlabel('Time (s)', fontsize=5)        # Set font size for the x-label
        #self.ax.set_ylabel('Usage (%)', fontsize=5)       # Set font size for the y-label

        # Adjust y-axis to start from the minimum value of memory usage
        #min_memory_usage = min(self.memory_usages)
        #self.ax.set_ylim(bottom=min(0, min_memory_usage - 5))  # Set the lower limit of y-axis
        self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1f}'))
        # Draw the updated plot
        self.canvas.draw()
