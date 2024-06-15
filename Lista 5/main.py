from typing import List

import pandas as pd

from utils import (
    import_jokes,
    import_ratings,
    test_over_fitting,
    test_sizes,
    test_learning_rates,
    split_dataset,
    best_mlb,
)
from sentence_transformers import SentenceTransformer

# dataset URI: https://eigentaste.berkeley.edu/dataset/

MODEL_NAME = "bert-base-cased"

LEARNING_RATES = [0.00001, 0.0001, 0.001, 0.005]
SIZES = [(20,), (100,), (100, 100), (200, 200, 200)]

OWN_JOKES = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why don't skeletons fight each other? They don't have the guts. ",
    "What do you call fake spaghetti? An impasta!",
    "How does a penguin build its house? Igloos it together.",
    "Why did the bicycle fall over? Because it was two-tired!",
]


def get_and_describe_jokes() -> List[str]:
    jokes = import_jokes()
    print(jokes)
    print(len(jokes))

    return jokes


def get_and_describe_ratings() -> pd.DataFrame:
    ratings = import_ratings()
    print(ratings)
    print(ratings.describe())

    return ratings


def test_my_jokes(
    model: SentenceTransformer,
    X_train: pd.DataFrame,
    Y_train: pd.DataFrame,
    X_test: pd.DataFrame,
    Y_test: pd.DataFrame,
) -> None:

    mlb = best_mlb(X_train, Y_train, X_test, Y_test)

    def predict_joke_rating(joke):
        _emb = model.encode([joke])
        return mlb.predict(_emb)[0]

    for own_joke in OWN_JOKES:
        print(predict_joke_rating(own_joke))


def main() -> None:
    jokes = get_and_describe_jokes()
    ratings = get_and_describe_ratings()

    model = SentenceTransformer(MODEL_NAME)
    encoded_jokes = model.encode(jokes)
    print(encoded_jokes.shape)

    x_train, y_train, x_test, y_test = split_dataset(encoded_jokes, ratings)

    test_over_fitting(x_train, y_train, x_test, y_test)
    test_learning_rates(LEARNING_RATES, x_train, y_train, x_test, y_test)
    test_sizes(SIZES, x_train, y_train, x_test, y_test)

    test_my_jokes(model, x_train, y_train, x_test, y_test)


if __name__ == "__main__":
    main()
