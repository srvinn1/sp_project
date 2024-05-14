from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout, QHBoxLayout, QSizePolicy, QMainWindow
from PyQt5.QtCore import QSize, Qt, QTimer, QTime, Qt
from PyQt5.QtGui import QPalette, QColor, QPainter, QBrush, QPen, QFont
import getpass
from cpu_section import TopCPUProcessesWidget
from memory_section import TopMemoryProcessesWidget
from network_section import TopNetworkProcessesWidget, NetworkMonitorWidget
from battery_section import BatteryGraphWidget
from kill_process_section import KillerApp
from toggle_switch import ThemeSwitch
from time_section import DigitalClock
from combined_plots import CombinedUsagePlotWidget
from cpu_section import CPUUsagePlotWidget
from network_section import NetworkUsagePlotWidget
from memory_section import MemoryUsagePlotWidget
from combined_plots import CombinedUsagePlotWidget
class RectanglePlaceholder(QWidget):
    """A QWidget subclass to mimic a rectangle placeholder."""
    def __init__(self, width, height, color='#FFFFFF'):
        super().__init__()
        self.setFixedSize(QSize(width, height))
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


        # Initialize a layout to organize children inside the rectangle
        self.inner_layout = QVBoxLayout(self)
                 
        #self.inner_layout.setContentsMargins(10, 10, 10, 10)

        # Set size policy to allow resizing within the layout
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class ComplexUILayout(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Complex UI Layout with Rectangles")
        #self.setStyleSheet("color: purple;")
        self.setMinimumSize(1400, 800)

        self.width = 450
        self.height = 100

        self.light_theme()

        # Main layout to hold all sub-layouts
        main_layout = QGridLayout()
        main_layout.setSpacing(10)

        # Get the current PC user's username
        username = getpass.getuser()


        # First column of rectangles
        first_column = QVBoxLayout()
        first_column.setSpacing(10)

        # Create the rectangle placeholder
        self.welcome_rectangle = RectanglePlaceholder(self.width, 60 + self.height, '#562680')
        self.welcome_rectangle.setStyleSheet("background-color: #562680;"
                                        "border-radius: 10px;"
                                        "color: white")
        # Create a label with the welcome message
        welcome_label = QLabel(f"Welcome back, {username}!", self.welcome_rectangle)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setFont(QFont('Monaco', 25, QFont.Bold)) 
        welcome_label.setStyleSheet("font-family: 'Arial';"
                "font-size: 25pt;" 
                "font-weight: bold;"
                "color: white;") 

        # Add the welcome label to the layout within the rectangle
        self.welcome_rectangle.inner_layout.addWidget(welcome_label)
        # Add other rectangles to the first column
        first_column.addWidget(self.welcome_rectangle)

        #Rectangle with CPU Usage
        cpu_rectangle = RectanglePlaceholder(self.width, 145 + self.height)
        cpu_label = QLabel("CPU Usage")
        cpu_table = TopCPUProcessesWidget()
        cpu_rectangle.inner_layout.addWidget(cpu_label)
        cpu_rectangle.inner_layout.addWidget(cpu_table)
        first_column.addWidget(cpu_rectangle)
        network_rectangle = RectanglePlaceholder(self.width, 235 + self.height)
        network_usage_label = QLabel("Network Usage", network_rectangle)
        #network_usage_label.setStyleSheet("color: purple;")
        network_process_table = TopNetworkProcessesWidget()
        network_usage_table = NetworkMonitorWidget()
        network_rectangle.inner_layout.addWidget(network_usage_label)
        network_rectangle.inner_layout.addWidget(network_process_table)
        network_rectangle.inner_layout.addWidget(network_usage_table)
        first_column.addWidget(network_rectangle)
        # Second column of rectangles
        second_column = QVBoxLayout()
        second_column.setSpacing(10)
        right_stack_hbox = QHBoxLayout()
        right_stack_hbox.setSpacing(10)
        self.theme_switch = ThemeSwitch()

        right_stack_hbox.addWidget(self.theme_switch, 0, Qt.AlignCenter)
        self.theme_switch.toggle_button.clicked.connect(self.switch_theme)
        clock_rectangle = RectanglePlaceholder(220, 60 + self.height)
        clock_widget = DigitalClock()
        clock_rectangle.inner_layout.addWidget(clock_widget)   
        right_stack_hbox.addWidget(clock_widget)
        second_column.addLayout(right_stack_hbox)

        kill_process_rectangle = RectanglePlaceholder(self.width, 155)
        kill_process_label = QLabel("Enter the process you want to kill", kill_process_rectangle)
        kill_process = KillerApp()
        kill_process_rectangle.inner_layout.addWidget(kill_process_label)
        kill_process_rectangle.inner_layout.addWidget(kill_process)
        second_column.addWidget(kill_process_rectangle)


        memory_rectangle = RectanglePlaceholder(self.width, 145 + self.height)
        memory_label = QLabel("Memory Usage", memory_rectangle)
        memory_table = TopMemoryProcessesWidget()
        memory_rectangle.inner_layout.addWidget(memory_label)
        memory_rectangle.inner_layout.addWidget(memory_table)
        second_column.addWidget(memory_rectangle)

        battery_rectangle = RectanglePlaceholder(self.width, 145 + self.height)
        battery_label = QLabel("Battery Usage", battery_rectangle)
        #battery_label.setStyleSheet("color: purple;")
        battery_graph = BatteryGraphWidget(self.width,115+self.height)
        battery_rectangle.inner_layout.addWidget(battery_label)
        battery_rectangle.inner_layout.addWidget(battery_graph)
        second_column.addWidget(battery_rectangle)

        # Third column of rectangles
        third_column = QVBoxLayout()
        third_column.setSpacing(10)
       
        cpu_graph = RectanglePlaceholder(self.width,760,'#FFFFFF')
       
        cpu_plot = CPUUsagePlotWidget(self.width,115+self.height)
        # Add the plots to the layout within the rectangle
        cpu_graph.inner_layout.addWidget(cpu_plot)
        # Add the plot rectangle to the third column
        #third_column.addWidget(cpu_graph)
       # plot_label.setMargin(5)
        plots = CombinedUsagePlotWidget()
        memory_plot = MemoryUsagePlotWidget(self.width,115+self.height)
        network_plot = NetworkUsagePlotWidget(self.width,115+self.height)
        # Add the plots to the layout within the rectangl
        
        cpu_graph.inner_layout.addWidget(memory_plot)
        #cpu_graph.inner_layout.addWidget(QLabel("Network Usage", cpu_graph, alignment=Qt.AlignCenter))
        cpu_graph.inner_layout.addWidget(network_plot)

        # Add the plot rectangle to the third column
        third_column.addWidget(cpu_graph)

        

        # Add all columns to the grid layout
        main_layout.addLayout(first_column, 0, 0)
        main_layout.addLayout(second_column, 0, 1)
        main_layout.addLayout(third_column, 0, 2)

        # Set the main layout for the window
        self.setLayout(main_layout)


    def switch_theme(self):
        self.theme_switch.toggle_theme()
        # Toggle the theme based on the internal state of the theme switcher
        if self.theme_switch.checked:  # Assuming 'checked' is a boolean attribute of ThemeSwitch
            self.dark_theme()
            self.welcome_rectangle.setStyleSheet("background-color: #2E2E2E;"
                                        "border-radius: 10px;"
                                        "color: white")
        else:
            self.light_theme()
            self.welcome_rectangle.setStyleSheet("background-color: #562680;"
                                        "border-radius: 10px;"
                                        "color: white")
            
  

    def dark_theme(self):
        self.setStyleSheet("""
            QWidget{
                background-color: #3E3E3E;           
            }                  
            QPushButton {
                background-color: #555555;
                color: white;
                border-radius: 14px;
            }
            QTableWidget {
                background-color: transparent;
                border: none;
                color: #FFFFFF;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: rgba(255, 255, 255, 0.3);
                text-align: left;
                font-size: 13px;
                color: #E7D5F6;  
                font-weight: 500;
            }
            QTableWidget QHeaderView {
                background-color: rgba(255, 255, 255, 0.3);
                font-size: 13px;
                color: #E7D5F6;  
                border: none;
                font-weight: 500;
                text-transform: uppercase;
            }
            QTableWidget QTableWidgetItem {
                padding: 3px;
                color: #fff;
            }
            QTableWidget::item:selected {
                background: rgba(255, 255, 255, 0.5);
            }
            QLabel {
                font-family: 'Monaco'; 
                font-size: 14pt; 
                font-weight: bold;
                color: #E7D5F6;
            }
            QLineEdit {
                border: 1px solid #D9D9D9;
                border-radius: 10px;
                padding: 0 8px;
                background: #3E3E3E;
                selection-background-color: darkgray;
                font-size: 16pt;
                color: #555;         
            }

        """)


    def light_theme(self):
        self.setStyleSheet("""
            QVBoxLayout {
                background-color: blue;
            } 
            QPushButton {
                background-color: #562680;
                color: white;
                border-radius: 14px;
            }
            QLabel {
                color: black;
            }
            QTableWidget {
                background-color: transparent;
                border: none;
                color: #000000;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: rgba(255, 255, 255, 0.3);
                text-align: left;
                font-size: 13px;
                color: #562680;  
                font-weight: 500;
            }
            QTableWidget QHeaderView {
                background-color: rgba(255, 255, 255, 0.3);
                font-size: 13px;
                color: #562680;  
                border: none;
                font-weight: 500;
                text-transform: uppercase;
            }
            QTableWidget QTableWidgetItem {
                padding: 3px;
                color: #fff;
            }
            QTableWidget::item:selected {
                background: rgba(255, 255, 255, 0.5);
            }
            QLabel {
                font-family: 'Monaco'; 
                font-size: 14pt; 
                font-weight: bold;
                color: #562680;
            }
            QLineEdit {
                border: 1px solid #D9D9D9;
                border-radius: 10px;
                padding: 0 8px;
                background: white;
                selection-background-color: darkgray;
                font-size: 16pt;
                color: #555;         
            }
            """)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ComplexUILayout()
    window.show()
    sys.exit(app.exec_())