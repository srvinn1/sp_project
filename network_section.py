import sys
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QGridLayout
from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import psutil
import matplotlib.ticker as ticker

class TopNetworkProcessesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Top 5 Network Processes")
        #self.setFixedSize(QSize(600, 250))

        # Layout and label
        layout = QVBoxLayout()

        # Table Widget for displaying the process information
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["PID", "Name", "Bytes Sent (MB)", "Bytes Received (MB)"])
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        # Update the process info periodically
        self.update_process_info()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_process_info)
        self.timer.start(2000)  # Update every 2 seconds

        self.setLayout(layout)


    def update_process_info(self):
        """Update the table with the top 5 processes by network usage."""
        process_list = []

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # Initialize counters
                bytes_sent = 0
                bytes_recv = 0

                # Get network I/O stats for all connections of this process
                connections = proc.connections(kind='inet')
                for conn in connections:
                    if conn.status == psutil.CONN_ESTABLISHED:
                        bytes_sent += conn.laddr.port
                        if conn.raddr:
                            bytes_recv += conn.raddr.port

                process_list.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'] or 'Unknown',
                    'bytes_sent': bytes_sent / (1024 * 1024),  # Convert to MB
                    'bytes_recv': bytes_recv / (1024 * 1024)   # Convert to MB
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Sort processes by total bytes sent + received in descending order
        sorted_procs = sorted(process_list, key=lambda p: p['bytes_sent'] + p['bytes_recv'], reverse=True)

        # Populate the table with the top 5 network processes
        self.table.setRowCount(min(len(sorted_procs), 5))
        for row, proc in enumerate(sorted_procs[:5]):
            self.table.setItem(row, 0, QTableWidgetItem(str(proc['pid'])))
            self.table.setItem(row, 1, QTableWidgetItem(proc['name']))
            self.table.setItem(row, 2, QTableWidgetItem(f"{proc['bytes_sent']:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{proc['bytes_recv']:.2f}"))


class NetworkMonitorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Monitor")

        # Layout
        layout = QGridLayout()

        # Labels for showing the network statistics
        self.packets_in_label = QLabel("Packets in: 0")
        self.packets_out_label = QLabel("Packets out: 0")
        self.packets_in_sec_label = QLabel("Packets in/sec: 0")
        self.packets_out_sec_label = QLabel("Packets out/sec: 0")
        self.data_received_label = QLabel("Data received: 0 MB")
        self.data_sent_label = QLabel("Data sent: 0 MB")
        self.data_received_sec_label = QLabel("Data received/sec: 0 B/s")
        self.data_sent_sec_label = QLabel("Data sent/sec: 0 B/s")

        # Add labels to layout
        layout.addWidget(self.packets_in_label, 0, 0)
        layout.addWidget(self.packets_out_label, 1, 0)
        layout.addWidget(self.packets_in_sec_label, 2, 0)
        layout.addWidget(self.packets_out_sec_label, 3, 0)
        layout.addWidget(self.data_received_label, 0, 1)
        layout.addWidget(self.data_sent_label, 1, 1)
        layout.addWidget(self.data_received_sec_label, 2, 1)
        layout.addWidget(self.data_sent_sec_label, 3, 1)

        self.setLayout(layout)

        # Timer to update stats every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)  # Update every 1 second

        # To store previous values to calculate rate
        self.previous_stats = psutil.net_io_counters()
        self.previous_time = psutil.time.time()

    def update_stats(self):
        current_stats = psutil.net_io_counters()
        current_time = psutil.time.time()

        # Calculate deltas
        delta_time = current_time - self.previous_time
        if delta_time == 0:
            return  # Prevent division by zero

        packets_in = current_stats.packets_recv - self.previous_stats.packets_recv
        packets_out = current_stats.packets_sent - self.previous_stats.packets_sent
        data_received = (current_stats.bytes_recv - self.previous_stats.bytes_recv) / (1024 * 1024)  # Convert to MB
        data_sent = (current_stats.bytes_sent - self.previous_stats.bytes_sent) / (1024 * 1024)  # Convert to MB

        # Update labels
        self.packets_in_label.setText(f"Packets in: {current_stats.packets_recv}")
        self.packets_out_label.setText(f"Packets out: {current_stats.packets_sent}")
        self.packets_in_sec_label.setText(f"Packets in/sec: {packets_in / delta_time:.2f}")
        self.packets_out_sec_label.setText(f"Packets out/sec: {packets_out / delta_time:.2f}")
        self.data_received_label.setText(f"Data received: {current_stats.bytes_recv / (1024 * 1024):.2f} MB")
        self.data_sent_label.setText(f"Data sent: {current_stats.bytes_sent / (1024 * 1024):.2f} MB")
        self.data_received_sec_label.setText(f"Data received/sec: {data_received / delta_time * 1024:.2f} B/s")
        self.data_sent_sec_label.setText(f"Data sent/sec: {data_sent / delta_time * 1024:.2f} B/s")

        # Update previous stats for next calculation
        self.previous_stats = current_stats
        self.previous_time = current_time

class NetworkUsagePlotWidget(QWidget):
    def __init__(self,width,height):
        super().__init__()
        self.setMinimumSize(width, height)
        # Create a figure
        self.figure, self.ax = plt.subplots(figsize=(5, 3))  # Adjust the figsize as needed
        self.canvas = FigureCanvas(self.figure)

        # Set the title and labels with smaller font size
        self.ax.set_title('Network Usage (KB)', fontsize=9, color = '#562680')   # Set font size for the title
        #self.ax.set_xlabel('Time (s)', fontsize=9)        # Set font size for the x-label
        #self.ax.set_ylabel('Usage (KB)', fontsize=9)       # Set font size for the y-label
        # Initialize empty data
        self.times = []
        self.network_usages = []

        # Set up a timer to update the plot every second
        self.timer = self.startTimer(1000)

        # Add canvas to layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def timerEvent(self, event):
        # Get current network usage
        network_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

        # Convert network usage to kilobytes
        network_usage_kb = network_usage / 1024

        # Append the current time and network usage to the data lists
        self.times.append(len(self.times) + 1)
        self.network_usages.append(network_usage_kb)

        # Clear previous plot
        self.ax.clear()

        # Plot network usage
        self.ax.plot(self.times, self.network_usages, color='red')

        # Set title and labels
        self.ax.set_title('Network Usage (KB)', fontsize=9, color = '#562680')    # Set font size for the title
        #self.ax.set_xlabel('Time (s)', fontsize=5)        # Set font size for the x-label
        #self.ax.set_ylabel('Usage (KB)', fontsize=5)       # Set font size for the y-label

        # Adjust y-axis to start from the minimum value of network usage
        #min_network_usage = min(self.network_usages)
        #self.ax.set_ylim(bottom=min(0, min_network_usage - 5))  # Set the lower limit of y-axis
        # Draw the updated plot
        self.canvas.draw()
