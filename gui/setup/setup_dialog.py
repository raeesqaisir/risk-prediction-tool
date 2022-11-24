import os

from PyQt5.QtCore import Qt
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QCheckBox, QVBoxLayout

from gui.title_bar import TitleBar
from config import ALGORITHMS, ALGO_NAME_TO_ID, BASE_ALGORITHMS
import config

class SetupDialog(QtWidgets.QFrame):

    onSubmit = pyqtSignal(list)

    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.parent = parent

        self.m_mouse_down = False
        self.setObjectName('setup_window')
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        css = """
            QFrame {
                background:  #F5F5F5;
            }
            #setup_window {
                border: 1px solid #555555;
            }
        """
        self.setStyleSheet(css)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.titlebar = TitleBar(self)
        layout.addWidget(self.titlebar)
        self.main_widget = QtWidgets.QWidget(self)
        uic.loadUi('gui/setup/setup_dialog.ui', self.main_widget)
        layout.addWidget(self.main_widget)
        self.setLayout(layout)

        self.main_widget.uploadTrainButton.clicked.connect(self.uploadTrain)
        self.main_widget.uploadAddressesButton.clicked.connect(
            self.uploadAddresses)
        self.main_widget.uploadLatlonsButton.clicked.connect(
            self.uploadLatlons)
        self.main_widget.submitButton.clicked.connect(self.submit)

        # Remove default algo checkboxes
        for i in reversed(range(self.main_widget.algoLayout.count())):
            self.main_widget.algoLayout.itemAt(i).widget().setParent(None)

        # Add algorithms from config files
        self.listAlgoCheck = []
        for algo in ALGORITHMS:
            # Skip extended algorithms if not specify --extendedss
            if not config.USE_EXTENDED_ALGORITHMS and algo["id"] not in BASE_ALGORITHMS:
                continue

            check = QCheckBox(algo["name"], self)
            check.setChecked(True)
            check.stateChanged.connect(self.algoCheck)
            self.listAlgoCheck.append(check)
            self.main_widget.algoLayout.addWidget(check)
        check = QCheckBox("All", self)
        check.setChecked(True)
        self.listAlgoCheck.append(check)
        self.main_widget.algoLayout.addWidget(check)
        check.stateChanged.connect(self.algoCheckAll)

        self.train_file = None
        self.addresses_file = None
        self.latlons_file = None
        self.selected_algorithms = []

    def algoCheckAll(self):
        """Check all agorithms"""
        for check in self.listAlgoCheck[:-1]:
            check.stateChanged.disconnect()
            check.setChecked(self.listAlgoCheck[-1].isChecked())
            check.stateChanged.connect(self.algoCheck)

    def algoCheck(self):
        """Check single algorithm"""
        is_checked_all = True
        for check in self.listAlgoCheck[:-1]:
            if not check.isChecked():
                is_checked_all = False
                break

        # Sync "All" checkbox
        all_checkbox = self.listAlgoCheck[-1]
        if is_checked_all != all_checkbox.isChecked():
            all_checkbox.stateChanged.disconnect()
            all_checkbox.setChecked(is_checked_all)
            all_checkbox.stateChanged.connect(self.algoCheckAll)

    def getCheckedAlgorithms(self):
        """List checked algorithms"""
        selected_algorithms = []
        for check in self.listAlgoCheck[:-1]:
            if check.isChecked():
                selected_algorithms.append(ALGO_NAME_TO_ID[check.text()])
        return selected_algorithms

    def beginSetup(self):
        """Begin setup algorithms"""
        self.train_file = None
        self.addresses_file = None
        self.latlons_file = None
        self.main_widget.checkTrain.setChecked(False)
        self.main_widget.checkAddresses.setChecked(False)
        self.main_widget.checkLatlons.setChecked(False)
        self.main_widget.checkTrain.stateChanged.connect(
            self.restoreStateFiles)
        self.main_widget.checkAddresses.stateChanged.connect(
            self.restoreStateFiles)
        self.main_widget.checkLatlons.stateChanged.connect(
            self.restoreStateFiles)
        self.main_widget.checkTrain.clicked.connect(self.restoreStateFiles)
        self.main_widget.checkAddresses.clicked.connect(self.restoreStateFiles)
        self.main_widget.checkLatlons.clicked.connect(self.restoreStateFiles)
        self.selected_algorithms = self.getCheckedAlgorithms()
        self.show()

    def restoreStateFiles(self):
        """Restore file states to prevent manually clicking"""
        self.main_widget.checkTrain.stateChanged.disconnect()
        self.main_widget.checkAddresses.stateChanged.disconnect()
        self.main_widget.checkLatlons.stateChanged.disconnect()
        self.main_widget.checkTrain.setChecked(self.train_file is not None)
        self.main_widget.checkAddresses.setChecked(
            self.addresses_file is not None)
        self.main_widget.checkLatlons.setChecked(self.latlons_file is not None)
        self.main_widget.checkTrain.stateChanged.connect(
            self.restoreStateFiles)
        self.main_widget.checkAddresses.stateChanged.connect(
            self.restoreStateFiles)
        self.main_widget.checkLatlons.stateChanged.connect(
            self.restoreStateFiles)

    def uploadTrain(self):
        path = QFileDialog.getOpenFileName(
            self, "Browse for train.csv", "", "Train file (*.csv)")
        if path:
            path = path[0]
            path = os.path.normpath(path)
            if not os.path.isfile(path):
                self.handleError("Selected item is not a file.")
                self.train_file = None
                self.main_widget.checkTrain.setChecked(False)
                return
            if not path.endswith(".csv"):
                self.handleError("You must select a csv file.")
                self.train_file = None
                self.main_widget.checkTrain.setChecked(False)
                return
            self.train_file = path
            self.main_widget.checkTrain.setChecked(True)

    def uploadAddresses(self):
        path = QFileDialog.getOpenFileName(
            self, "Browse for addresses.csv", "", "Addresses file (*.csv)")
        if path:
            path = path[0]
            path = os.path.normpath(path)
            if not os.path.isfile(path):
                self.handleError("Selected item is not a file.")
                self.addresses_file = None
                self.main_widget.checkAddresses.setChecked(False)
                return
            if not path.endswith(".csv"):
                self.handleError("You must select a csv file.")
                self.addresses_file = None
                self.main_widget.checkAddresses.setChecked(False)
                return
            self.addresses_file = path
            self.main_widget.checkAddresses.setChecked(True)

    def uploadLatlons(self):
        path = QFileDialog.getOpenFileName(
            self, "Browse for latlons.csv", "", "Latlons file (*.csv)")
        if path:
            path = path[0]
            path = os.path.normpath(path)
            if not os.path.isfile(path):
                self.handleError("Selected item is not a file.")
                self.latlons_file = None
                self.main_widget.checkLatlons.setChecked(False)
                return
            if not path.endswith(".csv"):
                self.handleError("You must select a csv file.")
                self.latlons_file = None
                self.main_widget.checkLatlons.setChecked(False)
                return
            self.latlons_file = path
            self.main_widget.checkLatlons.setChecked(True)

    def submit(self):
        if self.train_file is None:
            QMessageBox.warning(self.parent, "Error",
                                "You have not selected a train file.")
            return
        if self.addresses_file is None:
            QMessageBox.warning(self.parent, "Error",
                                "You have not selected an addresses file.")
            return
        if self.latlons_file is None:
            QMessageBox.warning(self.parent, "Error",
                                "You have not selected a latlons file.")
            return
        self.selected_algorithms = self.getCheckedAlgorithms()
        if len(self.selected_algorithms) == 0:
            QMessageBox.warning(self.parent, "Error",
                                "You have not selected any algorithms.")
            return
        self.onSubmit.emit([self.train_file, self.addresses_file,
                           self.latlons_file, self.selected_algorithms])

    def mousePressEvent(self, event):
        self.m_old_pos = event.pos()
        self.m_mouse_down = event.button() == Qt.LeftButton

    def mouseReleaseEvent(self, event):
        self.m_mouse_down = False

    def handleError(self, message):
        QMessageBox.warning(self.parent, "Error", message)
