import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import QtWidgets, QtGui

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('OptiWin')
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Initialize UI components here
        label = QtWidgets.QLabel('Welcome to OptiWin!', self)
        label.setGeometry(200, 200, 300, 100)
        label.setFont(QtGui.QFont('Arial', 20))

        # Theme support can go here 
        self.setStyleSheet("QMainWindow { background-color: #f0f0f0; }")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
