from typing import Tuple

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, KBinsDiscretizer

from utils import get_empty_dataframe


def run_transformation(
    transform, target_data: pd.DataFrame, train_data: pd.DataFrame = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if train_data is None:
        return transform.fit_transform(target_data), get_empty_dataframe()

    return transform.fit_transform(target_data), transform.transform(train_data)


def standardize_data(
    target_data: pd.DataFrame, train_data: pd.DataFrame = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return run_transformation(StandardScaler(), target_data, train_data)


def apply_pca(
    target_data: pd.DataFrame, train_data: pd.DataFrame = None, n_components: int = 5
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return run_transformation(PCA(n_components=n_components), target_data, train_data)


def discretize_data(
    target_data: pd.DataFrame,
    train_data: pd.DataFrame = None,
    n_bins: int = 5,
    encode: str = "ordinal",
    strategy: str = "uniform",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return run_transformation(
        KBinsDiscretizer(n_bins=n_bins, encode=encode, strategy=strategy),
        target_data,
        train_data,
    )


"""
def select_features(
    feature: pd.DataFrame, target: pd.Series, number_of_top_features: int
) -> (pd.DataFrame, pd.Series):
    return SelectKBest(score_func=f_classif, k=number_of_top_features).fit_transform(
        feature, target
    )
"""
