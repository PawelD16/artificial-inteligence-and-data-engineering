from typing import List

import pandas as pd

from classification import (
    run_all_classifiers,
    run_all_classifier_cross_val,
    ResultTestAndPredLabels,
    ResultCrossVal,
)
from data_exploration import explore_dataframe
from data_split import (
    split_into_data_and_labels,
    split_data_into_training_and_test,
    get_k_fold_cross_validation,
)
from preprocessing import standardize_data, apply_pca
from utils import encode_labels, print_list_newline

df = pd.read_csv("t-shirts.csv")
target_column_name = "demand"


def std_and_pca_split_to_test_and_train(
    data_frame: pd.DataFrame,
) -> List[ResultTestAndPredLabels]:
    data, labels = split_into_data_and_labels(data_frame, target_column_name)

    data_train, data_test, train_labels, test_labels = (
        split_data_into_training_and_test(data, labels)
    )

    data_train_std, data_test_std = standardize_data(data_train, data_test)
    data_train_pca, data_test_pca = apply_pca(data_train_std, data_test_std, 4)

    return run_all_classifiers(data_train_pca, data_test_pca, train_labels, test_labels)


def std_and_pca_k_fold(data_frame: pd.DataFrame) -> List[ResultCrossVal]:
    data, labels = split_into_data_and_labels(data_frame, target_column_name)

    k_fold = get_k_fold_cross_validation()

    data_std, _ = standardize_data(data)
    data_pca, _ = apply_pca(data_std, n_components=4)

    return run_all_classifier_cross_val(data_pca, labels, k_fold)


def main() -> None:
    print("________________DATA EXPLORATION________________")
    print(explore_dataframe(df))
    data_frame = encode_labels(df)

    print("________________SPLIT TO TEST AND TRAIN________________")
    print_list_newline(std_and_pca_split_to_test_and_train(data_frame))

    print("________________SPLIT BY K-FOLD________________")
    print_list_newline(std_and_pca_k_fold(data_frame))


if __name__ == "__main__":
    main()
