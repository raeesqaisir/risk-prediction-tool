import logging
import os
import sys
from argparse import ArgumentParser

from libs.data_preparation import prepare_data
from libs.models.model_factory import ModelFactory

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(message)s")


def train_model(train_file, test_file, address_file, latlons_file, test_ratio=0.2):
    """Train a model
    """

    logging.info("== Preparing data...")
    X_train, y_train, X_test, y_test = prepare_data(
        train_file, test_file, address_file, latlons_file, test_ratio)

    logging.info("== Training models...")

    logging.info("== Logistic regression model...")
    model = ModelFactory.get_model("logistic_regression")
    model.fit(X_train, y_train)
    for feature, importance in model.get_feature_importances():
        logging.info('    Feature: %s, Score: %.5f' % (feature, importance))
    print("Accuracy:", model.accuracy_score(X_test, y_test))
    print("F1:", model.f1_score(X_test, y_test))

    logging.info("== Random Forest model...")
    model = ModelFactory.get_model("random_forest")
    model.fit(X_train, y_train)
    for feature, importance in model.get_feature_importances():
        logging.info('    Feature: %s, Score: %.5f' % (feature, importance))
    print("Accuracy:", model.accuracy_score(X_test, y_test))
    print("F1:", model.f1_score(X_test, y_test))

    logging.info("== Support Vector Machines model...")
    model = ModelFactory.get_model("svm")
    model.fit(X_train, y_train)
    for feature, importance in model.get_feature_importances():
        logging.info('    Feature: %s, Score: %.5f' % (feature, importance))
    print("Accuracy:", model.accuracy_score(X_test, y_test))
    print("F1:", model.f1_score(X_test, y_test))

    logging.info("== Gradient Boosting model...")
    model = ModelFactory.get_model("gradient_boosting")
    model.fit(X_train, y_train)
    for feature, importance in model.get_feature_importances():
        logging.info('    Feature: %s, Score: %.5f' % (feature, importance))
    print("Accuracy:", model.accuracy_score(X_test, y_test))
    print("F1:", model.f1_score(X_test, y_test))


if __name__ == '__main__':

    ap = ArgumentParser('Train Fines Risk Predictor')
    ap.add_argument('--train_file', type=str, required=False,
                    default="data/train.csv", help='Path to training data: train.csv')
    ap.add_argument('--test_file', type=str, required=False,
                    default="data/test.csv", help='Path to test data: test.csv')
    ap.add_argument('--address_file', type=str, required=False,
                    default="data/addresses.csv", help='Path to address file: addresses.csv')
    ap.add_argument('--latlons_file', type=str, required=False,
                    default="data/latlons.csv", help='Path to latlons file: latlons.csv')
    ap.add_argument('--test_ratio', type=float, required=False,
                    default=0.1, help='Test set ratio. Default: 0.2')
    args = ap.parse_args()
    args = vars(args)

    assert os.path.isfile(
        args['train_file']), "Train file not found. Please input --train_file=/path/to/train.csv"
    assert os.path.isfile(
        args['test_file']), "Test file not found. Please input --test_file=/path/to/test.csv"
    assert os.path.isfile(
        args['address_file']), "Address file not found. Please input --address_file=/path/to/addresses.csv"
    assert os.path.isfile(
        args['latlons_file']), "Latlons file not found. Please input --latlons_file=/path/to/latlons.csv"
    assert args['test_ratio'] > 0 and args['test_ratio'] < 1, "Test ratio should be between 0 and 1."

    train_model(**args)
