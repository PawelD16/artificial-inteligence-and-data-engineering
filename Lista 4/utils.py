import pandas as pd
from sklearn.preprocessing import LabelEncoder


def encode_labels(df: pd.DataFrame) -> pd.DataFrame:
    label_encoders = {}
    for column in df.columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le

    return df


def get_empty_dataframe() -> pd.DataFrame:
    return pd.DataFrame([])


def print_list_newline(lst: list) -> None:
    print(*lst, sep="\n")
