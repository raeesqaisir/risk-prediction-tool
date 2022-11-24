import pyqtgraph as pg

from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QSizePolicy, QWidget

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class ResultTab(QWidget):
    def __init__(self, parent=None, result=None, tab_name="Result Tabs"):
        super().__init__()
        self.parent = parent
        self.name = tab_name

        if result is None:
            uic.loadUi('gui/loading.ui', self)
            self.movie = QMovie("images/loading.gif")
            self.loadingIconLabel.setMovie(self.movie)
            self.movie.start()
            self.setSizePolicy(QSizePolicy.Expanding,
                               QSizePolicy.Expanding)
        else:
            # Load result layout
            uic.loadUi('gui/result.ui', self)
            self.accuracyLabel.setText(
                "{:.2f}%".format(result["accuracy"] * 100))
            self.f1Label.setText("{:.2f}".format(result["f1"]))

            # Draw ROC curve
            self.rocCurveGraph.setFixedSize(400, 300)
            self.rocCurveGraph.clear()
            plt = self.rocCurveGraph.getPlotItem()
            plt.showGrid(x=True, y=True)
            plt.setLabel("bottom", "FPR")
            plt.setLabel("left", "TPR")
            plt.addLegend()
            fpr, tpr, thresholds = result["roc_curve"]
            plt.plot(fpr, tpr, pen=pg.mkPen(
                {'color': "green", 'width': 2}), symbolPen='green', symbol="o", symbolSize=5, symbolBrush=(0, 255, 0), name='ROC')

            # Draw confusion matrix
            cfm = result["plot_confusion_matrix"]
            cfm = QtGui.QImage(cfm.data, cfm.shape[1], cfm.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.confusionMatrixLabel.setPixmap(QtGui.QPixmap.fromImage(cfm).scaled(400, 207, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

            # Feature ranking
            feature_importances = result["feature_importances"]
            html = ""
            for feature, value in feature_importances:
                html += "<li>{} : {:.2f}</li>".format(feature, value)
            html = "<ol>" + html + "</ol>"
            self.featureImportanceEdit.setText(html)

            # Top risks
            top_risks = result["top_risks"]
            html = ""
            for item in top_risks:
                html += "<li>Ticket ID {} : {}</li>".format(item["ticket_id"], item["prediction"])
            html = "<ol>" + html + "</ol>"
            self.topRiskEdit.setText(html)

            
