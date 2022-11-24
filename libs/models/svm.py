from libs.models.model import Model
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import \
    LinearSVC  # use LinearSVC instead of SVC to reduce training time


class SVMModel(Model):
    """Support Vector Machines model
    """

    def __init__(self, config):
        super().__init__(config)

    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train
        # Use feature scaler to reduce the training time
        # And fit better
        self.model = Pipeline([('scaler', StandardScaler()), ('svc', CalibratedClassifierCV(base_estimator=LinearSVC(**self.config)))])
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        assert self.model is not None, "Model is not fitted yet!"
        return self.model.predict(X_test)

    def predict_proba(self, X_test):
        assert self.model is not None, "Model is not fitted yet!"
        return self.model.named_steps["svc"].predict_proba(X_test)[:, 1]

    @property
    def _feature_importances(self):
        assert self.model is not None, "Model is not fitted yet!"
        coeffs = self.model.named_steps["svc"].calibrated_classifiers_[0].base_estimator.coef_.tolist()[0]
        return coeffs
