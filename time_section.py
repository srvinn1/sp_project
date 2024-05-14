from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt

class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a label to display the time
        self.timeLabel = QLabel(self)
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.timeLabel.setStyleSheet("font-size: 30pt; font-weight: 900; font-family: 'Arial';")

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.timeLabel)
        self.setLayout(layout)

        # Set up a timer to update the clock every second
        timer = QTimer(self)
        timer.timeout.connect(self.updateTime)
        timer.start(1000)  # Update every 1000 milliseconds (1 second)

        # Initial update to display the time immediately
        self.updateTime()

    def updateTime(self):
        # Get the current time
        currentTime = QTime.currentTime()
        # Format the time as a string
        formattedTime = currentTime.toString('hh:mm')
        # Set the formatted time on the label
        self.timeLabel.setText(formattedTime)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.setWindowTitle('Digital Clock')
    clock.show()
    sys.exit(app.exec_())
