import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout


class QtExample(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.resize(250, 150)
        self.move(300, 300)
        self.setWindowTitle('2 Click btn')

        self.print1button = QPushButton('Print once!', self)
        self.print1button.clicked.connect(self.print_once)
        self.print5button = QPushButton('Print five times!', self)
        self.print5button.clicked.connect(self.print_five)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.print1button)
        self.vbox.addWidget(self.print5button)
        self.setLayout(self.vbox)
        self.show()

    def print_once(self):
        print('Hello one!')

    def print_five(self):
        print('Hello five!')


app = QApplication(sys.argv)
w = QtExample()

w.resize(250, 150)
w.move(500, 500)
w.setWindowTitle('Simple Oskar')
w.show()
sys.exit(app.exec_())
