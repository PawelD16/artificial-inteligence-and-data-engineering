from abc import ABC
from typing import List

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    f1_score,
    recall_score,
    # confusion_matrix,
    make_scorer,
)
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

random_state = 42

classifiers = {
    "Naive Bayes": GaussianNB(),
    "Decision Tree": DecisionTreeClassifier(random_state=random_state),
    "Random Forest": RandomForestClassifier(random_state=random_state),
    "SVM": SVC(random_state=random_state),
}


class Result(ABC):
    def __init__(
        self,
        classifier_name: str,
        accuracy: float,
        precision: float,
        recall: float,
        f1: float,
        # confusion_mtx: List,
    ) -> None:
        self.__classifier_name = classifier_name
        self.__accuracy = accuracy
        self.__precision = precision
        self.__recall = recall
        self.__f1_score = f1
        # self.__confusion_matrix = confusion_mtx

    def __str__(self) -> str:
        return (
            f"\nResults for {self.__classifier_name}: "
            f"\n\tAccuracy: {self.__accuracy} "
            f"\n\tPrecision: {self.__precision} "
            f"\n\tRecall: {self.__recall} "
            f"\n\tF1 Score: {self.__f1_score} "
            # f"\n\tConfusion Matrix:  \n\t{self.__confusion_matrix} \n"
        )


class ResultTestAndPredLabels(Result):
    def __init__(
        self, classifier_name: str, test_labels: pd.Series, pred_labels: pd.Series
    ) -> None:
        super().__init__(
            classifier_name=classifier_name,
            accuracy=accuracy_score(test_labels, pred_labels),
            precision=precision_score(test_labels, pred_labels, average="weighted"),
            recall=recall_score(test_labels, pred_labels, average="weighted"),
            f1=f1_score(test_labels, pred_labels, average="weighted"),
            # confusion_mtx=confusion_matrix(test_labels, pred_labels),
        )


def evaluate_model_cv(X, y, model, scoring, kf):
    scores = {
        metric: cross_val_score(model, X, y, scoring=scoring[metric], cv=kf)
        for metric in scoring
    }
    return {metric: scores[metric].mean() for metric in scores}


class ResultCrossVal(Result):
    def __init__(
        self,
        classifier_name: str,
        data: pd.DataFrame,
        labels: pd.Series,
        classifier,
        cross_val,
    ):
        self.__classifier = classifier
        self.__cross_val = cross_val
        self.__data = data
        self.__labels = labels

        super().__init__(
            classifier_name=classifier_name,
            accuracy=self.__run_cross_val(make_scorer(accuracy_score)),
            precision=self.__run_cross_val(
                make_scorer(precision_score, average="weighted")
            ),
            recall=self.__run_cross_val(make_scorer(recall_score, average="weighted")),
            f1=self.__run_cross_val(make_scorer(f1_score, average="weighted")),
            # confusion_mtx=[],
        )

    def __run_cross_val(self, scorer) -> float:
        return cross_val_score(
            self.__classifier,
            self.__data,
            self.__labels,
            scoring=scorer,
            cv=self.__cross_val,
        ).mean()


def run_all_classifiers(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    train_labels: pd.Series,
    test_labels: pd.Series,
) -> List[ResultTestAndPredLabels]:
    results = []
    for name, clf in classifiers.items():
        clf.fit(train_data, train_labels)
        pred_labels = clf.predict(test_data)
        results.append(ResultTestAndPredLabels(name, test_labels, pred_labels))

    return results


def run_all_classifier_cross_val(
    data: pd.DataFrame, labels: pd.Series, cross_validation
) -> List[ResultCrossVal]:
    results = []
    for name, clf in classifiers.items():
        results.append(ResultCrossVal(name, data, labels, clf, cross_validation))

    return results
