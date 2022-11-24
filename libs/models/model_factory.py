from config import ID_TO_ALGO
from libs.models.logistic_regression import LogisticRegressionModel
from libs.models.random_forest import RandomForestModel
from libs.models.svm import SVMModel


class ModelFactory:

    @staticmethod
    def get_model(model_name, config=None):
        if config is None:
            config = ID_TO_ALGO[model_name].get("config", {})
        if model_name == 'logistic_regression':
            return LogisticRegressionModel(config)
        elif model_name == 'random_forest':
            return RandomForestModel(config)
        elif model_name == 'svm':
            return SVMModel(config)
        else:
            raise ValueError("Model {} is not supported.".format(model_name))
