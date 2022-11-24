from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QMessageBox)

from gui.setup.setup_dialog import SetupDialog
from gui.tab_manager import TabManager
from gui.title_bar import TitleBar


class MainWindow(QtWidgets.QFrame):
    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.m_mouse_down = False
        self.setObjectName('main_window')
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        css = """
            QFrame {
                background:  #F5F5F5;
            }
            #main_window {
                border: 1px solid #555555;
            }
            #back_button {
                width: 100px;
            }
        """
        self.setStyleSheet(css)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.titlebar = TitleBar(self)
        layout.addWidget(self.titlebar)

        content_layout = QVBoxLayout()
        self.tab_manager = TabManager(self)
        self.tab_manager.setStyleSheet(
        """
            QTabBar::tab { height: 20px; margin-bottom: 5px; background: #fff; border: 1px solid #efefef; padding-left: 10px; padding-right: 10px; }
            QTabBar::tab:selected { border-bottom: 2px solid #007bff }
        """)
        content_layout.addWidget(self.tab_manager)

        footer_layout = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.back_button.setObjectName("back_button")
        self.back_button.clicked.connect(self.back)
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        footer_layout.addWidget(self.back_button)
        footer_layout.addSpacerItem(spacer)
        content_layout.addItem(footer_layout)
        content_layout.setContentsMargins(10, 10, 10, 10)

        layout.addLayout(content_layout)
        self.setLayout(layout)

        self.resize(900, 600)

        self.setup_dialog = SetupDialog()
        self.setup_dialog.onSubmit.connect(self.runTraining)
        self.setup_dialog.beginSetup()


    def mousePressEvent(self, event):
        self.m_old_pos = event.pos()
        self.m_mouse_down = event.button() == Qt.LeftButton

    def mouseReleaseEvent(self, event):
        self.m_mouse_down = False

    def runTraining(self, params):
        train_file, addresses_file, latlons_file, selected_algorithms = params
        self.tab_manager.startTraining(train_file, addresses_file, latlons_file, selected_algorithms)
        self.setup_dialog.hide()
        self.show()

    def back(self):
        """Stop the work and back to the setup dialog"""
        if self.tab_manager.is_training:
            QMessageBox.warning(self, "Error",
                                "Could not go back. Training is in progress. You can wait until training is finished or restart the program.")
            return
        self.setup_dialog.beginSetup()
        self.hide()
