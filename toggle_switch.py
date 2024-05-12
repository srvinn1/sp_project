import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont, QPen, QPixmap, QImage, QIcon
from PyQt5.QtCore import QRectF, Qt, QTimer, QSize



class ThemeSwitch(QWidget):
    def __init__(self):
        super().__init__()
        self.checked = False  # Toggle state 
        self.toggle_button = QPushButton("", self)
        self.init_ui()
        self.setFixedSize(100, 50)

    def init_ui(self):
        self.setWindowTitle('Advanced Theme Switch')
        self.setStyleSheet("background-color: white;") 
        
        self.moon_icon = QIcon(QPixmap("/Users/kamilla/Desktop/ML/sp_project/assets/moon_grey.png"))
        self.sun_icon = QIcon(QPixmap("/Users/kamilla/Desktop/ML/sp_project/assets/sun_purple.png")) # Set default background to a neutral color

        self.toggle_button.setFixedSize(40, 40)
        self.toggle_button.setStyleSheet("QPushButton {"
                                         "border: none;"
                                         "background-color: white;"
                                         "border-radius: 16px;"
                                         "}")  # Ensure button has no border or unwanted background
        self.toggle_button.move(5, 5)  # Initial position
        self.toggle_button.setIcon(self.sun_icon)
        self.toggle_button.setIconSize(QSize(20, 20))

        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_transition)
        self.animation_timer.start(10)

    def toggled(self):
        self.toggle_button

    def toggle_theme(self):
        self.checked = not self.checked
        self.animation_timer.start(10)  # Start or restart the animation timer

    def dark_theme(self):
        self.moon_icon = QIcon(QPixmap("/Users/kamilla/Desktop/ML/sp_project/assets/moon_purple.png"))
        self.sun_icon = QIcon(QPixmap("/Users/kamilla/Desktop/ML/sp_project/assets/sun_grey.png"))
        self.toggle_button.setStyleSheet("QPushButton {"
                                         "border: none;"
                                         "background-color: #3E3E3E;"
                                         "border-radius: 16px;"
                                         "}")
        self.toggle_button.setIcon(self.moon_icon)
    
    def light_theme(self):
        self.moon_icon = QIcon(QPixmap("/Users/kamilla/Desktop/ML/sp_project/assets/moon_grey.png"))
        self.sun_icon = QIcon(QPixmap("/Users/kamilla/Desktop/ML/sp_project/assets/sun_purple.png"))
        self.toggle_button.setStyleSheet("QPushButton {"
                                         "border: none;"
                                         "background-color: white;"
                                         "border-radius: 16px;"
                                         "}")
        self.toggle_button.setIcon(self.sun_icon)
        

    def animate_transition(self):
        step = 5  # Control the speed of the animation
        max_position = 55  # End position for the toggle
        if self.checked and self.toggle_button.x() < max_position:
            self.toggle_button.move(self.toggle_button.x() + step, 5)
            self.dark_theme()
            
        elif not self.checked and self.toggle_button.x() > 5:
            self.toggle_button.move(self.toggle_button.x() - step, 5)
            self.light_theme()
        else:
            self.animation_timer.stop()  # Stop the timer when the end position is reached
        self.update()  # Request a repaint


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)
        # Draw the container
        background_color = QColor("#646464") if self.checked else QColor("#DFD6E7")
        painter.setBrush(QBrush(background_color))

        painter.drawRoundedRect(0, 0, self.width(), self.height(), 18, 18)

        painter.drawPixmap(15, 15, self.sun_icon.pixmap(17, 17))
        painter.drawPixmap(65, 15, self.moon_icon.pixmap(17, 17))


