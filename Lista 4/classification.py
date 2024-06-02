from typing import List, Dict, Any

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from results_carriers import ResultTestAndPredLabels, ResultCrossVal


def get_all_classifiers_with_hyperparameters(
    hyperparameters: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    return {
        "Naive Bayes": GaussianNB(
            **hyperparameters.get("Naive Bayes", {})
        ),
        "Decision Tree": DecisionTreeClassifier(
            **hyperparameters.get("Decision Tree", {})
        ),
        "Random Forest": RandomForestClassifier(
            **hyperparameters.get("Random Forest", {})
        ),
        "SVM": SVC(**hyperparameters.get("SVM", {})),
    }


def run_all_classifiers(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    train_labels: pd.Series,
    test_labels: pd.Series,
    classifiers: Dict[str, Any],
) -> List[ResultTestAndPredLabels]:
    results = []
    for name, clf in classifiers.items():
        clf.fit(train_data, train_labels)
        pred_labels = clf.predict(test_data)
        results.append(ResultTestAndPredLabels(name, test_labels, pred_labels))

    return results


def run_all_classifier_cross_val(
    data: pd.DataFrame, labels: pd.Series, cross_validation, classifiers: Dict[str, Any]
) -> List[ResultCrossVal]:
    results = []
    for name, clf in classifiers.items():
        results.append(ResultCrossVal(name, data, labels, clf, cross_validation))

    return results
