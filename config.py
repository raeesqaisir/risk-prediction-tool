DATA_PREPARATION = {
    "balancing_method": "smote_tomek", # "none", "smote", "smote_tomek", "enn" (EditedNearestNeighbours)
}

BASE_ALGORITHMS = ["svm", "logistic_regression", "random_forest"]
USE_EXTENDED_ALGORITHMS = False
ALGORITHMS = [
    {
        "name": "Logistic Regression",
        "id": "logistic_regression",
        "config": {
            "penalty": "l2", # "l1", "l2", "elasticnet", "none"
            "tol": 1e-4,
            "C": 1.0,
            "fit_intercept": True,
            "solver": "lbfgs", # "newton-cg", "lbfgs", "liblinear", "sag", "saga"
            "random_state": 42,
            "class_weight": None, # dict or ‘balanced’, default=None
            "max_iter": 2000,
        }
    },
    {
        "name": "Random Forest",
        "id": "random_forest",
        "config": {
            "n_estimators": 1000,
            "max_depth": None,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "max_features": "auto", # "auto", "sqrt", "log2", None
            "bootstrap": True,
            "criterion": "gini", # "gini", "entropy"
            "max_leaf_nodes": None,
            "min_impurity_decrease": 0.0,
            "random_state": 42,
            "n_jobs": -1,
            "class_weight": None, # {"balanced", "balanced_subsample"}, dict or list of dicts, default=None
        }
    },
    {
        "name": "Support Vector Machines",
        "id": "svm",
        "config": {
            "penalty": "l2", # "l1", "l2"
            "loss": "squared_hinge", # "hinge", "squared_hinge"
            "C": 1.0,
            "class_weight": None,
            "random_state": 42,
            "max_iter": 3000
        }
    },
]

ALGO_NAME_TO_ID = {
    x["name"]: x["id"] for x in ALGORITHMS
}

ALGO_ID_TO_NAME = {
    x["id"]: x["name"] for x in ALGORITHMS
}

ID_TO_ALGO = {
    x["id"]: x for x in ALGORITHMS
}