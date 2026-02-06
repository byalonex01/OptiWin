import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('System Stats and Actions')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # System Stats
        self.stats_group = QGroupBox('System Stats', self)
        self.stats_layout = QVBoxLayout()
        self.stats_layout.addWidget(QLabel('CPU Usage: 20%'))
        self.stats_layout.addWidget(QLabel('Memory Usage: 50%'))
        self.stats_group.setLayout(self.stats_layout)
        self.layout.addWidget(self.stats_group)

        # Mode Selection
        self.mode_group = QGroupBox('Select Mode', self)
        self.mode_layout = QHBoxLayout()
        self.mode_layout.addWidget(QPushButton('Normal Mode'))
        self.mode_layout.addWidget(QPushButton('Advanced Mode'))
        self.mode_group.setLayout(self.mode_layout)
        self.layout.addWidget(self.mode_group)

        # Quick Actions
        self.actions_group = QGroupBox('Quick Actions', self)
        self.actions_layout = QVBoxLayout()
        self.actions_layout.addWidget(QPushButton('Action 1'))
        self.actions_layout.addWidget(QPushButton('Action 2'))
        self.actions_group.setLayout(self.actions_layout)
        self.layout.addWidget(self.actions_group)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())