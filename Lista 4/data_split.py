from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split, KFold


def split_into_data_and_labels(
    df: pd.DataFrame, column_name: str
) -> Tuple[pd.DataFrame, pd.Series]:
    return df.drop(column_name, axis=1), df[column_name]


def split_data_into_training_and_test(
    data: pd.DataFrame,
    labels: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    return train_test_split(
        data, labels, test_size=test_size, random_state=random_state
    )


def get_k_fold_cross_validation(n_splits: int = 5, random_state: int = 42) -> KFold:
    return KFold(n_splits=n_splits, shuffle=True, random_state=random_state)
