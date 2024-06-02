# It's the ultimate answer to the great question of life, the universe and everything.
random_state = 42

default_hyperparameters = {
    "Naive Bayes": {},
    "Decision Tree": {},
    "Random Forest": {},
    "SVM": {}
}

hyperparameters_1 = {
    "Naive Bayes": {
        "var_smoothing": 1e-9
    },
    "Decision Tree": {
        "random_state": random_state,
        "max_depth": 3
    },
    "Random Forest": {
        "random_state": random_state,
        "n_estimators": 50
    },
    "SVM": {
        "random_state": random_state,
        "kernel": "rbf",
        "C": 1.0
    },
}

hyperparameters_2 = {
    "Naive Bayes": {
        "var_smoothing": 1e-8
    },
    "Decision Tree": {
        "random_state": random_state,
        "max_depth": 5,
        "min_samples_split": 4,
    },
    "Random Forest": {
        "random_state": random_state,
        "n_estimators": 100,
        "max_features": "sqrt",
    },
    "SVM": {
        "random_state": random_state,
        "kernel": "linear",
        "C": 0.5
    },
}

hyperparameters_3 = {
    "Naive Bayes": {
        "var_smoothing": 1e-7
    },
    "Decision Tree": {
        "random_state": random_state,
        "max_depth": 7,
        "min_samples_split": 2,
        "criterion": "entropy",
    },
    "Random Forest": {
        "random_state": random_state,
        "n_estimators": 200,
        "max_depth": 10,
    },
    "SVM": {
        "random_state": random_state,
        "kernel": "poly",
        "C": 1.0,
        "degree": 3
    },
}
