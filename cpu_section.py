import sys
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtCore import QSize, Qt

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

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import psutil

class CPUUsagePlotWidget(QWidget):
    def __init__(self,width,height):
        super().__init__()
        self.setMinimumSize(width, height)
        # Create a figure
        self.figure, self.ax = plt.subplots(figsize=(5, 3))  # Adjust the figsize as needed
        self.canvas = FigureCanvas(self.figure)

        # Set the title and labels
        self.ax.set_title('CPU Usage (%)', fontsize=9,color = '#562680')  # Set font size for the title
        #self.ax.set_xlabel('Time (s)', fontsize=9,c='purple')      # Set font size for the x-label
        #self.ax.set_ylabel('Usage (%)', fontsize=9,c='purple')     # Set font size for the y-label

        # Initialize empty data
        self.times = []
        self.cpu_usages = []

        # Set up a timer to update the plot every second
        self.timer = self.startTimer(1000)

        # Add canvas to layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignCenter)

    def timerEvent(self, event):
        # Get current CPU usage
        cpu_usage = psutil.cpu_percent()

        # Append the current time and CPU usage to the data lists
        self.times.append(len(self.times) + 1)
        self.cpu_usages.append(cpu_usage)

        # Clear previous plot
        self.ax.clear()

        # Plot CPU usage
        self.ax.plot(self.times, self.cpu_usages, color='violet')

        # Set title and labels
        self.ax.set_title('CPU Usage (%)', fontsize=9, color = '#562680')  # Set font size for the title
       # self.ax.set_xlabel('Time (s)', fontsize=9,c='#562680')      # Set font size for the x-label
       # self.ax.set_ylabel('Usage (%)', fontsize=9,c='purple')     # Set font size for the y-label

        # Adjust y-axis to start from the minimum value of CPU usage
        min_cpu_usage = min(self.cpu_usages)
        self.ax.set_ylim(bottom=min(0, min_cpu_usage - 5))  # Set the lower limit of y-axis

        # Draw the updated plot
        self.canvas.draw()

