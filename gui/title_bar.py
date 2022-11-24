import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class TitleBar(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName('titlebar')
        css = """
            QWidget{
                background: #00c8f8;
                color: black;
                font-size: 18px;
                height: 20px;
            }
            #titlebar {
                border-bottom: 1px solid #555555;
            }
            QDialog{
                font-size: 20px;
                color: black;
                background-color: #00c8f8;
            }
            QToolButton {
                background: #00c8f8;
                font-size: 25px;
                border: 0;
                color: white;
            }
        """
        self.setAutoFillBackground(False)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.setStyleSheet(css)
        close = QtWidgets.QToolButton(self)
        close.setText("✕")
        close.setMinimumHeight(10)
        label = QtWidgets.QLabel(self)
        label.setText("Risk Prediction Tool")
        self.setWindowTitle("Risk Prediction Tool")
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(label)
        hbox.addWidget(close)
        hbox.insertStretch(1, 500)
        hbox.setSpacing(0)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Fixed)
        self.maxNormal = False
        close.clicked.connect(self.close)
        self.parent = parent

    def close(self):
        self.parent.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.moving = True
            self.parent.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.parent.moving:
            self.parent.move(event.globalPos()-self.parent.offset)
