import sys
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MultipleLocator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import psutil
from PyQt5.QtCore import QSize, Qt
class BatteryGraphWidget(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.setWindowTitle("Real-time Battery Level Graph")
        self.setMinimumSize(width, height)
        
        # Initialize layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Align the graph to the center
        
        # Initialize the figure and axis for the battery graph
        self.fig, self.ax_battery = plt.subplots(1, 1, figsize=(6, 3), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # Set up the battery graph
        self.ax_battery.set_title("Battery Level", fontsize=9,c='purple')
        self.ax_battery.set_ylim([0, 100])
        self.ax_battery.set_ylabel('Battery (%)', fontsize=8,c='purple')
        self.ax_battery.xaxis.set_major_locator(MultipleLocator(3))
        self.ax_battery.grid(axis='both', linestyle='--', color='pink', alpha=0.6)

        # Set the layout for the widget
        self.setLayout(layout)

        # Data containers
        self.time_series = []
        self.battery_data = []

        # Initialize the timer for periodic updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(60000)  # Update every minute

    def update_graph(self):
        """Update the battery graph with real data."""
        battery = psutil.sensors_battery()
        if battery:  # Check if battery data is available
            self.time_series.append(datetime.now())
            self.battery_data.append(battery.percent)
        
            # Keep the last 24 data points
            if len(self.time_series) > 24:
                self.time_series = self.time_series[-24:]
                self.battery_data = self.battery_data[-24:]

            self.ax_battery.clear()
            self.ax_battery.plot(self.time_series, self.battery_data, color='purple', marker='o')
            self.ax_battery.set_ylim([0, 100])
            self.ax_battery.set_ylabel('Battery (%)',fontsize=8,c='purple')
            self.ax_battery.xaxis.set_major_formatter(DateFormatter('%H:%M'))
            self.ax_battery.grid(axis='both', linestyle='--', color='pink', alpha=0.6)

            # Redraw the canvas
            self.canvas.draw()
        else:
            print("Battery info not available.")



