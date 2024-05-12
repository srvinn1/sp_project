# settings_section.py
import getpass
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QCheckBox
from PyQt5.QtCore import Qt

class SettingsSection(QGroupBox):
    def __init__(self, theme_toggle_callback):
        super().__init__("Settings")
        layout = QVBoxLayout()

        # User Information
        current_user_label = QLabel(f"Current User: {getpass.getuser()}")
        layout.addWidget(current_user_label)

        # Theme Switch
        theme_label = QLabel("Change Theme")
        layout.addWidget(theme_label)

        self.dark_theme_checkbox = QCheckBox("Dark Theme")
        self.dark_theme_checkbox.stateChanged.connect(theme_toggle_callback)
        layout.addWidget(self.dark_theme_checkbox)

        self.setLayout(layout)

    def is_dark_theme(self):
        """Return whether the dark theme checkbox is checked."""
        return self.dark_theme_checkbox.isChecked()
