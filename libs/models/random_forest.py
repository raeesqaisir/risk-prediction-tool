from sklearn.ensemble import RandomForestClassifier

from libs.models.model import Model


class RandomForestModel(Model):
    """Random Forest model
    """

    def __init__(self, config):
        super().__init__(config)

    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train
        self.model = RandomForestClassifier(**self.config)
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        assert self.model is not None, "Model is not fitted yet!"
        return self.model.predict(X_test)

    def predict_proba(self, X_test):
        assert self.model is not None, "Model is not fitted yet!"
        return self.model.predict_proba(X_test)[:, 1]

    @property
    def _feature_importances(self):
        assert self.model is not None, "Model is not fitted yet!"
        return self.model.feature_importances_
