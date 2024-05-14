import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtCore import QSize, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import collections


class TopCPUProcessesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Top 5 CPU Processes")
        self.setFixedSize(QSize(450, 245))

        # Layout and label
        layout = QVBoxLayout()

        # Table Widget for displaying the process information
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["PID", "Name", "% CPU", "Threads"])
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)

        # Update the process table periodically
        self.update_process_info()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_process_info)
        self.timer.start(2000)  # Update every 2 seconds
        self.setLayout(layout)

        
    def update_process_info(self):
        """Update the table with the top 5 CPU processes."""
        # Retrieve all processes with minimal necessary attributes
        processes = [proc for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'num_threads'])]

        # Calculate the current CPU usage without delays
        for proc in processes:
            try:
                # Retrieve the latest CPU percentage with no interval delay
                proc.info['cpu_percent'] = proc.cpu_percent(interval=0.0)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                proc.info['cpu_percent'] = 0.0

        # Sort the processes by CPU percentage
        sorted_procs = sorted(processes, key=lambda p: p.info['cpu_percent'], reverse=True)

        # Clear the table and set the row count for the top 5 processes
        self.table.setRowCount(min(len(sorted_procs), 5))

        # Populate the table with the top 5 processes
        for row, proc in enumerate(sorted_procs[:5]):
            try:
                pid = proc.info['pid']
                name = proc.info['name'] or "Unknown"
                cpu_percent = proc.info['cpu_percent']
                num_threads = proc.info['num_threads']

                # Fill table cells
                self.table.setItem(row, 0, QTableWidgetItem(str(pid)))
                self.table.setItem(row, 1, QTableWidgetItem(name))
                self.table.setItem(row, 2, QTableWidgetItem(f"{cpu_percent:.2f}"))
                self.table.setItem(row, 3, QTableWidgetItem(str(num_threads)))

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue



class CPUUsagePlotWidget(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.setMinimumSize(width, height)

        # Create a figure and set initial plot properties
        self.figure, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.ax.set_title('CPU Usage (%)', fontsize=9, color='#562680')

        # Initialize data storage with a fixed window size of 60 seconds
        self.times = collections.deque(maxlen=60)  # Time in seconds
        self.cpu_usages = collections.deque(maxlen=60)  # CPU usages in percent

        # Set up a timer to update the plot every second
        self.timer = self.startTimer(1000)

        # Layout settings
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignCenter)

class CPUUsagePlotWidget(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.setMinimumSize(width, height)
        self.figure, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.ax.set_title('CPU Usage (%)', fontsize=9, color='#562680')
        self.times = collections.deque(maxlen=60)  # Time in seconds
        self.cpu_usages = collections.deque(maxlen=60)  # CPU usages in percent
        self.timer = self.startTimer(1000)  # Update every second
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignCenter)
        self.start_time = 0  # Start a counter from 0

    def timerEvent(self, event):
        cpu_usage = psutil.cpu_percent()
        self.start_time += 1  # Increment the start time
        self.times.append(self.start_time)
        self.cpu_usages.append(cpu_usage)
        self.ax.clear()
        self.ax.plot(list(self.times), list(self.cpu_usages), color='violet')
        self.ax.set_title('CPU Usage (%)', fontsize=9, color='#562680')
        self.ax.set_ylim(0, 100)  # Set fixed y-axis for percentage
        self.ax.xaxis.set_visible(False)
        #self.ax.set_xlim(max(0, self.start_time - 60), self.start_time)  # Adjust x-axis to show last 60 seconds
        self.canvas.draw()
