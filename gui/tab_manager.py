from config import ALGO_ID_TO_NAME
from PyQt5.QtWidgets import QTabWidget, QMessageBox

from gui.training_worker import TrainingWorker

from . import *


class TabManager(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.is_training = False
        self.tabs = []

        result_tab = ResultTab(self)
        self.tabs.append(result_tab)
        self.addTab(result_tab, "Unknown Tab")
        self.tasks = []


    def startTraining(self, train_file, addresses_file, latlons_file, selected_algorithms):
        """Initialize tabs and start training"""
        self.is_training = True

        # Remove all old tabs
        self.tabs = []
        self.clear()
        self.tasks = []

        # Prepare training tasks
        for i, algo in enumerate(selected_algorithms):
            self.tasks.append({
                "model_name": algo,
                "train_file": train_file,
                "addresses_file": addresses_file,
                "latlons_file": latlons_file,
                "test_ratio": 0.2,
                "tab_id": i
            })
            result_tab = ResultTab(self, tab_name=ALGO_ID_TO_NAME[algo])
            self.tabs.append(result_tab)
            self.addTab(result_tab, result_tab.name)


        # Run training
        self.worker = TrainingWorker(self.tasks)
        self.worker.onTaskDone.connect(self.updateResultTab)
        self.worker.trainingFinished.connect(self.trainingFinished)
        self.worker.onError.connect(self.onError)
        self.worker.start()
        
    
    def updateResultTab(self, result):
        """Update result tab"""
        tab_id = result["tab_id"]
        self.tabs[tab_id] = ResultTab(self, result=result, tab_name=self.tabs[tab_id].name)
        self.renderTabs()

    def renderTabs(self):
        """Re-render all tabs"""
        current_tab_index = self.currentIndex()
        self.clear()
        for tab in self.tabs:
            self.addTab(tab, tab.name)
        self.setCurrentIndex(current_tab_index)

    def trainingFinished(self):
        """Training finished"""
        self.is_training = False

    def onError(self, error):
        """Error while training"""
        QMessageBox.warning(self.parent, "Error", error)
        self.parent.back()