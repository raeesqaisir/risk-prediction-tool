import copy
import time
import traceback

from libs.data_preparation import prepare_data
from libs.models.model_factory import ModelFactory
from PyQt5.QtCore import QThread, pyqtSignal


class TrainingWorker(QThread):
    onTaskDone = pyqtSignal(dict)
    trainingFinished = pyqtSignal()
    onError = pyqtSignal(str)

    def __init__(self, tasks=None):
        super(TrainingWorker, self).__init__()
        if tasks is None:
            tasks = []
        self.tasks = tasks
        self.cache_data = None

    def run(self):
        self.do_shutdown = False
        self.cache_data = None
        for task in self.tasks:
            self.process_task(task)
            if self.do_shutdown:
                self.trainingFinished.emit()
                return
        self.trainingFinished.emit()

    def stop(self):
        self.do_shutdown = True

    def process_task(self, task):
        """Training worker"""
        print("Running task: ", task)
        if self.cache_data is not None:
            print("Use cached data")
            X_train, y_train, X_test, y_test, origin_X_test = self.cache_data
        else:
            print("Preparing data...")
            try:
                X_train, y_train, X_test, y_test, origin_X_test = prepare_data(
                    task["train_file"],
                    None,
                    task["addresses_file"],
                    task["latlons_file"],
                    test_ratio=task["test_ratio"],
                    output_origin_X_test=True,
                )
            except:
                self.do_shutdown = True
                self.trainingFinished.emit()
                self.onError.emit("Error while preparing data. Check your input data.")
                return
            self.cache_data = (X_train, y_train, X_test, y_test, origin_X_test)

        try:
            print("Training model:", task["model_name"])
            model = ModelFactory.get_model(task["model_name"])
            time_start = time.time()
            model.fit(X_train, y_train)
            time_end = time.time()
            print("Training time: {:.2f}s".format(time_end - time_start))
            model_report = model.get_full_report(
                X_test, y_test, origin_X_test=origin_X_test)
            print("Finished!")
        except Exception as e:
            self.do_shutdown = True
            self.trainingFinished.emit()
            self.onError.emit("Error on training: " + traceback.format_exc())
            return

        report = copy.deepcopy(task)
        report.update(model_report)
        self.onTaskDone.emit(report)
