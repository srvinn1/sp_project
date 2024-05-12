import sys
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

class CombinedUsagePlotWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a figure
        self.figure, self.ax = plt.subplots(figsize=(6, 4))

        # Set title and labels
        self.ax.set_title('Combined Usage Plot')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Usage')

        # Initialize empty data lists
        self.times = []
        self.memory_usages = []
        self.network_usages = []

        # Set up a timer to update the plot every second
        self.timer = self.startTimer(1000)

        # Add canvas to layout
        layout = QVBoxLayout()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Set formatter to display numbers in scientific notation
        self.ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

    def timerEvent(self, event):
        # Get current memory usage
        memory_usage = psutil.virtual_memory().percent

        # Get current network usage
        network_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        network_usage_kb = network_usage / 1024

        # Append the current time and usage to the data lists
        self.times.append(len(self.times) + 1)
        self.memory_usages.append(memory_usage)
        self.network_usages.append(network_usage_kb)

        # Clear previous plot
        self.ax.clear()

        # Plot memory usage as a line plot
        self.ax.plot(self.times, self.memory_usages, label='Memory Usage', color='green')

        # Plot network usage as a line plot
        self.ax.plot(self.times, self.network_usages, label='Network Usage', color='orange')

        # Add legend to the plot
        self.ax.legend()

        # Fix y-axis to start from zero
        self.ax.set_ylim(bottom=0)

        # Draw the updated plot
        self.canvas.draw()

