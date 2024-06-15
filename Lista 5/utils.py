import re
from typing import List, Tuple, Any

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor

CLEANR = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")

_JOKE_BEGIN_ = "<!--begin of joke -->"
_JOKE_END_ = "<!--end of joke -->"

_BASEPATH = "./jokes/"

TEST_SIZE_RATIO = 0.3


def clean_html(raw_html: str) -> str:
    return re.sub(CLEANR, "", raw_html)


def import_jokes() -> List[str]:
    jokes = []

    for j in range(1, 101):
        with open(f"{_BASEPATH}init{j}.html") as f:
            # concat every line into one string
            joke = "".join(f.readlines())

            # substring the joke
            _start = joke.find(_JOKE_BEGIN_) + len(_JOKE_BEGIN_)
            _end = joke.find(_JOKE_END_)
            joke = joke[_start:_end]

            # cleanup
            joke = joke.replace("\n", "")
            joke = joke.replace("\t", "")
            joke = clean_html(joke)
            jokes.append(joke)

    return jokes


def import_ratings() -> pd.DataFrame:
    ratings = pd.concat(
        pd.read_excel(f"./jester-data-{i}.xls", header=None) for i in range(1, 4)
    )
    ratings = ratings.iloc[:, 1:].replace(99, float("NaN"))
    ratings = ratings.mean()

    return ratings


def split_dataset(
    X: Any, Y: Any, test_size: float = TEST_SIZE_RATIO
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=test_size)

    return x_train, y_train, x_test, y_test


def perform_test(
    X_train: pd.DataFrame,
    Y_train: pd.DataFrame,
    X_test: pd.DataFrame,
    Y_test: pd.DataFrame,
    epochs: int = 1000,
    hidden_layer_sizes: Tuple[int] = (100,),
    learning_rate: float = 0.001,
) -> Tuple[list, list]:
    _mlp = MLPRegressor(
        solver="sgd",
        alpha=0.0,
        learning_rate="constant",
        hidden_layer_sizes=hidden_layer_sizes,
        learning_rate_init=learning_rate,
        random_state=0,
    )

    _train_loss = []
    _test_loss = []

    for e in range(epochs):
        _mlp.partial_fit(X_train, Y_train)
        _train_loss.append(mean_squared_error(Y_train, _mlp.predict(X_train)))
        _test_loss.append(mean_squared_error(Y_test, _mlp.predict(X_test)))

    return _train_loss, _test_loss


def test_over_fitting(
    x_train: pd.DataFrame,
    y_train: pd.DataFrame,
    x_test: pd.DataFrame,
    y_test: pd.DataFrame,
) -> None:
    tl, vl = perform_test(x_train, y_train, x_test, y_test)
    plt.plot(range(len(tl)), tl, label=f"Train Loss")
    plt.plot(range(len(vl)), vl, label=f"Test Loss")
    plt.legend()
    plt.show()


def test_learning_rates(
    learning_rates: List[float],
    X_train: pd.DataFrame,
    Y_train: pd.DataFrame,
    X_test: pd.DataFrame,
    Y_test: pd.DataFrame,
) -> None:
    run_test(
        lambda r: perform_test(
            X_train, Y_train, X_test, Y_test, epochs=2000, learning_rate=r
        ),
        learning_rates,
    )


def test_sizes(
    sizes: List[tuple],
    x_train: pd.DataFrame,
    y_train: pd.DataFrame,
    x_test: pd.DataFrame,
    y_test: pd.DataFrame,
) -> None:
    run_test(
        lambda s: perform_test(
            x_train, y_train, x_test, y_test, epochs=2000, hidden_layer_sizes=s
        ),
        sizes,
    )


def run_test(elem_fn: Any, iter_list: list) -> None:
    p1 = plt.figure()
    p2 = plt.figure()

    for elem in iter_list:
        tl, vl = elem_fn(elem)
        plt.figure(p1.number)
        plt.plot(range(len(tl)), tl, label=f"Train Loss {elem}")
        plt.figure(p2.number)
        plt.plot(range(len(vl)), vl, label=f"Test Loss {elem}")
    plt.legend()
    plt.figure(p1.number)
    plt.legend()
    plt.show()


def best_mlb(
    X_train: pd.DataFrame,
    Y_train: pd.DataFrame,
    X_test: pd.DataFrame,
    Y_test: pd.DataFrame,
) -> MLPRegressor:
    best_mlp = MLPRegressor(
        solver="sgd",
        alpha=0.0,
        learning_rate="constant",
        hidden_layer_sizes=(100,),
        learning_rate_init=0.0002,
        random_state=0,
        max_iter=3000,
    )

    best_mlp.fit(X_train, Y_train)
    best_mlp.score(X_test, Y_test)

    return best_mlp
