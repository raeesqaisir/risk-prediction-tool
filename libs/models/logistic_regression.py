from sklearn.linear_model import LogisticRegression

from libs.models.model import Model


class LogisticRegressionModel(Model):
    """Logistic regression model
    """

    def __init__(self, config):
        super().__init__(config)

    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train
        self.model = LogisticRegression(**self.config).fit(X_train, y_train)

    def predict(self, X_test):
        assert self.model is not None, "Model is not fitted yet!"
        return self.model.predict(X_test)

    def predict_proba(self, X_test):
        assert self.model is not None, "Model is not fitted yet!"
        return self.model.predict_proba(X_test)[:, 1]

    @property
    def _feature_importances(self):
        assert self.model is not None, "Model is not fitted yet!"
        return self.model.coef_[0]
