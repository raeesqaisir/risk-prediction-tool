import logging
import os
import sys
from argparse import ArgumentParser
from datetime import datetime
import pickle

import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTETomek
from imblearn.under_sampling import EditedNearestNeighbours

import config

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(message)s")

def time_gap(hearing_date_str, ticket_issued_date_str):
    if not hearing_date_str or type(hearing_date_str) != str:
        return 73
    hearing_date = datetime.strptime(hearing_date_str, "%Y-%m-%d %H:%M:%S")
    ticket_issued_date = datetime.strptime(
        ticket_issued_date_str, "%Y-%m-%d %H:%M:%S")
    gap = hearing_date - ticket_issued_date
    return gap.days

def prepare_data(train_file, test_file, address_file, latlons_file, test_ratio=0.2, output_origin_X_test=False):

    if test_file is None:
        test_file = train_file
        test_data = pd.read_csv(test_file, encoding='ISO-8859-1', low_memory=False)
    else:
        test_data = pd.read_csv(test_file)

    # Load and clean data
    train_data = pd.read_csv(
        train_file, encoding='ISO-8859-1', low_memory=False)
    
    address = pd.read_csv(address_file)
    latlons = pd.read_csv(latlons_file)
    address_lalo = address.set_index('address').join(latlons.set_index(
        'address'), how='left').dropna().reset_index(drop=False)
    train_data = pd.merge(train_data, address_lalo,
                          on='ticket_id').set_index('ticket_id')

    train_data['time_gap'] = train_data.apply(lambda row: time_gap(
        row['hearing_date'], row['ticket_issued_date']), axis=1)

    # Only keep data with valid "compliance"
    train_data = train_data[(train_data['compliance'] == 0)
                            | (train_data['compliance'] == 1)]
    train_data['compliance'] = train_data['compliance'].astype(int)

    origin_train_data = train_data.copy()
    origin_train_data['ticket_id'] = origin_train_data.index # Restore ticket_id

    # Remove train only columns
    trainOnly_columns = [
        'payment_amount', 'payment_date', 'payment_status', 'balance_due',
        'collection_status', 'compliance_detail'
    ]
    train_data.drop(trainOnly_columns, axis=1, inplace=True)

    # Feature used to train
    feature_columns = [
        'agency_name',
        'violation_street_name',
        'state',
        'violation_code',
        'late_fee',
        'fine_amount',
        'discount_amount',
        'judgment_amount',
        'lat',
        'lon',
        'time_gap'  # 'ticket_issued_date', 'hearing_date'
    ]

    convert_columns = {
        'agency_name': 'category',
        'violation_street_name': 'category',
        'state': 'category',
        'violation_code': 'category',
        'disposition': 'category',
    }

    for df in [train_data, test_data]:
        for col, col_type in convert_columns.items():
            if col in df:
                if col_type == 'category':
                    df[col] = df[col].astype(col_type)

    # Convert category columns to integers
    cat_columns = train_data.select_dtypes(['category']).columns
    for df in [train_data, test_data]:
        df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)

    # Split
    X = train_data[feature_columns].copy()
    y = train_data['compliance']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_ratio, random_state=42)

    # Transform the dataset
    # Deal with imbalanced data
    if config.DATA_PREPARATION["balancing_method"] == "smote":
        oversample = SMOTE(random_state=42)
        X_train, y_train = oversample.fit_resample(X_train, y_train)
    elif config.DATA_PREPARATION["balancing_method"] == "smote_tomek":
        oversample = SMOTETomek(sampling_strategy='auto', random_state=42)
        X_train, y_train = oversample.fit_resample(X_train, y_train)
    elif config.DATA_PREPARATION["balancing_method"] == "enn":
        undersample = EditedNearestNeighbours(n_neighbors=3)
        X_train, y_train = undersample.fit_resample(X_train, y_train)

    # Keep origin_X_test for calculating top risks
    if output_origin_X_test:
        _, origin_X_test, _, _ = train_test_split(
            origin_train_data, y, test_size=test_ratio, random_state=42)

    # # Only keep data with valid "compliance" (0, 1) for test set
    # X_test = X_test[(y_test == 0) | (y_test == 1)]
    # y_test.dropna(inplace=True)

    logging.info(f"Training data contains {len(X_train)} samples")
    logging.info(f"Test data contains {len(X_test)} samples")

    # test_ratio_after_dropna_compliance = len(y_test) / len(y)
    # logging.info("Test ratio after drop NaN compliance: %.2f" %
    #              test_ratio_after_dropna_compliance)

    if output_origin_X_test:
        return X_train, y_train, X_test, y_test, origin_X_test
    else:
        return X_train, y_train, X_test, y_test


if __name__ == '__main__':

    ap = ArgumentParser('Prepare Dataset')
    ap.add_argument('--train_file', type=str, required=False,
                    default="data/train.csv", help='Path to training data: train.csv')
    ap.add_argument('--test_file', type=str, required=False,
                    default="data/test.csv", help='Path to test data: test.csv')
    ap.add_argument('--address_file', type=str, required=False,
                    default="data/addresses.csv", help='Path to address file: addresses.csv')
    ap.add_argument('--latlons_file', type=str, required=False,
                    default="data/latlons.csv", help='Path to latlons file: latlons.csv')
    ap.add_argument('--test_ratio', type=float, required=False,
                    default=0.2, help='Test set ratio. Default: 0.2')
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

    prepare_data(**args)
