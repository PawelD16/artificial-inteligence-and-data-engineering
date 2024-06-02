from typing import List, Dict, Any, Callable, Tuple

import pandas as pd

from classification import (
    run_all_classifiers,
    run_all_classifier_cross_val,
    get_all_classifiers_with_hyperparameters,
)
from data_exploration import explore_dataframe
from data_split import (
    split_into_data_and_labels,
    split_data_into_training_and_test,
    get_k_fold_cross_validation,
)
from hyperparameter_sets import (
    default_hyperparameters,
    hyperparameters_1,
    hyperparameters_3,
    hyperparameters_2
)
from preprocessing import standardize_data, apply_pca
from results_carriers import ResultCrossVal, ResultTestAndPredLabels
from utils import encode_labels, print_list_newline

df = pd.read_csv("t-shirts.csv")
target_column_name = "demand"

default_classifiers = get_all_classifiers_with_hyperparameters(default_hyperparameters)
classifiers_1 = get_all_classifiers_with_hyperparameters(hyperparameters_1)
classifiers_2 = get_all_classifiers_with_hyperparameters(hyperparameters_2)
classifiers_3 = get_all_classifiers_with_hyperparameters(hyperparameters_3)


def no_preprocessing_split_to_test_and_train(
    data_frame: pd.DataFrame, classifiers: Dict[str, Any]
) -> List[ResultTestAndPredLabels]:

    return run_split_to_test_and_train_with_preprocessing_fn(
        data_frame, classifiers, lambda x, y, i: (x, y)
    )


def std_split_to_test_and_train(
    data_frame: pd.DataFrame, classifiers: Dict[str, Any]
) -> List[ResultTestAndPredLabels]:

    return run_split_to_test_and_train_with_preprocessing_fn(
        data_frame, classifiers, lambda x, y, i: standardize_data(x, y)
    )


def pca_split_to_test_and_train(
    data_frame: pd.DataFrame, classifiers: Dict[str, Any]
) -> List[ResultTestAndPredLabels]:
    return run_split_to_test_and_train_with_preprocessing_fn(data_frame, classifiers, apply_pca)


def run_split_to_test_and_train_with_preprocessing_fn(
    data_frame: pd.DataFrame,
    classifiers: Dict[str, Any],
    preprocessing_fn: Callable[[pd.DataFrame, pd.DataFrame, int], Tuple[pd.DataFrame, pd.DataFrame]]
) -> List[ResultTestAndPredLabels]:
    data, labels = split_into_data_and_labels(data_frame, target_column_name)

    data_train, data_test, train_labels, test_labels = (
        split_data_into_training_and_test(data, labels)
    )

    data_train_preprocessed, data_test_preprocessed = preprocessing_fn(data_train, data_test, 4)

    return run_all_classifiers(
        data_train_preprocessed, data_test_preprocessed, train_labels, test_labels, classifiers
    )


def no_preprocessing_k_fold(
    data_frame: pd.DataFrame, classifiers: Dict[str, Any]
) -> List[ResultCrossVal]:
    return run_k_fold_with_preprocessing_fn(data_frame, classifiers, lambda x, i: x)


def std_k_fold(
    data_frame: pd.DataFrame, classifiers: Dict[str, Any]
) -> List[ResultCrossVal]:
    return run_k_fold_with_preprocessing_fn(data_frame, classifiers, lambda x, i: standardize_data(x)[0])


def pca_k_fold(
    data_frame: pd.DataFrame, classifiers: Dict[str, Any]
) -> List[ResultCrossVal]:
    return run_k_fold_with_preprocessing_fn(data_frame, classifiers, lambda x, i: apply_pca(x, n_components=i)[0])


def run_k_fold_with_preprocessing_fn(
    data_frame: pd.DataFrame, classifiers: Dict[str, Any], preprocessing_fn: Callable[[pd.DataFrame, int], pd.DataFrame]
) -> List[ResultCrossVal]:
    data, labels = split_into_data_and_labels(data_frame, target_column_name)

    k_fold = get_k_fold_cross_validation()

    data_preprocessed = preprocessing_fn(data, 4)

    return run_all_classifier_cross_val(data_preprocessed, labels, k_fold, classifiers)


def run_with_classifier(data_frame: pd.DataFrame, classifiers: Dict[str, Any]) -> None:
    print("________________SPLIT TO TEST AND TRAIN NO PREPROCESSING________________")
    print_list_newline(no_preprocessing_split_to_test_and_train(data_frame, classifiers))

    print("________________SPLIT TO TEST AND TRAIN STD________________")
    print_list_newline(std_split_to_test_and_train(data_frame, classifiers))

    print("________________SPLIT TO TEST AND TRAIN PCA________________")
    print_list_newline(pca_split_to_test_and_train(data_frame, classifiers))

    print("________________SPLIT BY K-FOLD NO PREPROCESSING________________")
    print_list_newline(no_preprocessing_k_fold(data_frame, classifiers))

    print("________________SPLIT BY K-FOLD STD________________")
    print_list_newline(std_k_fold(data_frame, classifiers))

    print("________________SPLIT BY K-FOLD PCA________________")
    print_list_newline(pca_k_fold(data_frame, classifiers))


def main() -> None:
    print("________________DATA EXPLORATION________________")
    print(explore_dataframe(df))
    data_frame = encode_labels(df)

    print("________________HYPERPARAMETER DEFAULT SET________________")
    run_with_classifier(data_frame, default_classifiers)

    print("________________HYPERPARAMETER SET 1________________")
    run_with_classifier(data_frame, classifiers_1)

    print("________________HYPERPARAMETER SET 2________________")
    run_with_classifier(data_frame, classifiers_2)

    print("________________HYPERPARAMETER SET 3________________")
    run_with_classifier(data_frame, classifiers_3)


if __name__ == "__main__":
    main()
