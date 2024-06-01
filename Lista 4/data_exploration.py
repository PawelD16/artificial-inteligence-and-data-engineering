import pandas as pd


def explore_dataframe(df: pd.DataFrame) -> str:
    result = [
        "First few rows of the dataset:",
        str(df.head()),
        "\nDataset Information:",
        str(df.info()),
        "\nSummary Statistics:",
        str(df.describe(include="all")),
        "\nMissing Values:",
        str(df.isnull().sum()),
        "\nUnique Values for Each Categorical Column:",
    ]

    for column in df.columns:
        result.append(f"{column}: {df[column].unique()}")

    return "\n".join(result)
