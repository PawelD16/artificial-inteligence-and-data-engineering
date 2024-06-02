from abc import ABC
from typing import Any

import pandas as pd
from sklearn.metrics import (
    precision_score,
    accuracy_score,
    recall_score,
    f1_score,
    make_scorer,
)
from sklearn.model_selection import cross_val_score


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
            precision=precision_score(
                test_labels, pred_labels, average="weighted", zero_division=0
            ),
            recall=recall_score(test_labels, pred_labels, average="weighted"),
            f1=f1_score(test_labels, pred_labels, average="weighted"),
            # confusion_mtx=confusion_matrix(test_labels, pred_labels),
        )


class ResultCrossVal(Result):
    def __init__(
        self,
        classifier_name: str,
        data: pd.DataFrame,
        labels: pd.Series,
        classifier: Any,
        cross_val: Any,
    ):
        self.__classifier = classifier
        self.__cross_val = cross_val
        self.__data = data
        self.__labels = labels

        super().__init__(
            classifier_name=classifier_name,
            accuracy=self.__run_cross_val(make_scorer(accuracy_score)),
            precision=self.__run_cross_val(
                make_scorer(precision_score, average="weighted", zero_division=0)
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
