import tempfile
import os
import cv2

from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score, roc_curve)


class Model:
    """Parrent model class for all models"""

    cfm_form = cv2.imread("images/cfm_form.png")

    def __init__(self, config):
        self.config = config
        self.model = None
        self.X_train = None
        self.y_train = None

    def fit(self, X_train, y_train):
        raise NotImplementedError("Subclass must implement abstract method")

    def predict(self, X_test):
        raise NotImplementedError("Subclass must implement abstract method")

    def predict_proba(self, X_test):
        raise NotImplementedError("Subclass must implement abstract method")

    def f1_score(self, X_test, y_test):
        return f1_score(y_test, self.predict(X_test))

    def accuracy_score(self, X_test, y_test):
        return accuracy_score(y_test, self.predict(X_test))

    def get_feature_importances(self):
        assert self.model is not None, "Model is not fitted yet!"
        importances = self._feature_importances
        feature_names = self.X_train.columns.values.tolist()
        features_importances = []
        for i, v in enumerate(importances):
            features_importances.append((feature_names[i], v))
        features_importances.sort(key=lambda x: x[1], reverse=True)
        return features_importances

    def get_roc_curve(self, X_test, y_test):
        fpr, tpr, thresholds = roc_curve(y_test, self.predict_proba(X_test))
        return fpr, tpr, thresholds

    def get_full_report(self, X_test, y_test, origin_X_test=None):
        pred = self.predict(X_test)
        proba_pred = self.predict_proba(X_test)
       
        fpr, tpr, thresholds = roc_curve(y_test, proba_pred)
        tn, fp, fn, tp = confusion_matrix(pred, y_test).ravel()
        plot_confusion_matrix_cv2 = self.plot_cfm(tn, fp, fn, tp)
        top_risks = []
        if origin_X_test is not None:
            origin_X_test["prediction"] = proba_pred
            top_risks = origin_X_test.nlargest(5, "prediction")
        report = {
            "accuracy": accuracy_score(y_test, pred),
            "f1": f1_score(y_test, pred),
            "roc_curve": (fpr, tpr, thresholds),
            "confusion_matrix": (tn, fp, fn, tp),
            "plot_confusion_matrix": plot_confusion_matrix_cv2,
            "feature_importances": self.get_feature_importances(),
            "top_risks": top_risks.to_dict(orient="records")
        }
        return report


    def plot_cfm(self, tn, fp, fn, tp):
        """Plot confusion matrix to OpenCV image"""
        cfm_plot = Model.cfm_form.copy()
        cv2.putText(cfm_plot, "{}".format(tn), (396, 280), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)
        cv2.putText(cfm_plot, "{}".format(fp), (750, 280), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)
        cv2.putText(cfm_plot, "{}".format(fn), (396, 420), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)
        cv2.putText(cfm_plot, "{}".format(tp), (750, 420), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)
        return cfm_plot

